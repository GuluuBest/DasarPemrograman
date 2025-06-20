
import pandas as pd
from tabulate import tabulate
from datetime import datetime, time

# --- KONFIGURASI ---
AVAILABLE_ROOMS = {
    'GD A': {
        2: [f"A2-{i}" for i in range(1, 9)],
        3: [f"A3-{i}" for i in range(1, 9)],
        4: [f"A4-{i}" for i in range(1, 9)],
        5: [f"A5-{i}" for i in range(1, 9)],
    },
    'GD B': {
        3: [f"B3-{i}" for i in range(1, 6)],
        4: [f"B4-{i}" for i in range(1, 6)],
        5: [f"B5-{i}" for i in range(1, 6)],
    }
}

ROOM_PREFERENCES = {
    'TI': {'floors': [3, 4]},
    'SI': {'floors': [3, 4]},
    'DK': {'floors': [4, 5]},
    'SD': {'floors': [2, 3]},
    'HK': {'floors': [3, 4]},
    'ME': {'floors': [4, 5]},
    'EL': {'floors': [4, 5]},
    'AKT': {'floors': [2, 3]},
    'MJN': {'floors': [2, 3]},
}

ALLOWED_DAYS = ['SENIN', 'SELASA', 'RABU', 'KAMIS', 'JUMAT']
BREAKS = [
    (datetime.strptime("12:00", "%H:%M").time(), datetime.strptime("13:00", "%H:%M").time()),
    (datetime.strptime("18:00", "%H:%M").time(), datetime.strptime("19:00", "%H:%M").time())
]

JAM_KULIAH = [
    ("08:00", "10:00"),
    ("10:00", "12:00"),
    ("13:00", "15:00"),
    ("15:00", "17:00"),
    ("19:00", "21:00")
]

def is_time_slot_valid(start_str, end_str):
    try:
        start_t = datetime.strptime(start_str, "%H:%M").time()
        end_t = datetime.strptime(end_str, "%H:%M").time()
    except ValueError:
        return False
    if not (start_t < end_t):
        return False
    for break_start, break_end in BREAKS:
        if max(start_t, break_start) < min(end_t, break_end):
            return False
    return True

def is_room_available(df, day, start_str, end_str, gedung, lantai, ruang):
    start_t = datetime.strptime(start_str, "%H:%M").time()
    end_t = datetime.strptime(end_str, "%H:%M").time()
    bookings = df[(df['HARI'] == day) & (df['GEDUNG'] == gedung) & (df['LANTAI'] == lantai) & (df['RUANG'] == ruang)]
    for _, row in bookings.iterrows():
        booked_start = datetime.strptime(row['MULAI'], "%H:%M").time()
        booked_end = datetime.strptime(row['SELESAI'], "%H:%M").time()
        if max(start_t, booked_start) < min(end_t, booked_end):
            return False
    return True

def jadwal_otomatis_prioritas(df_pengajaran, df_request):
    df_jadwal = pd.DataFrame(columns=['HARI', 'DOSEN', 'MATAKULIAH', 'KELAS', 'PRODI', 'GEDUNG', 'LANTAI', 'RUANG', 'MULAI', 'SELESAI'])
    gagal = []

    for _, row in df_pengajaran.iterrows():
        dosen, matkul, kelas, prodi = row['DOSEN'], row['MATAKULIAH'], row['KELAS'], row['PRODI']
        preferensi = ROOM_PREFERENCES.get(prodi, {'floors': [2, 3, 4, 5]})['floors']
        jadwal_ditemukan = False

        request = df_request[(df_request['DOSEN'] == dosen) & (df_request['MATAKULIAH'] == matkul) & (df_request['KELAS'] == kelas)]

        for _, r in request.iterrows():
            hari = r['HARI']
            mulai = r['MULAI'].strftime('%H:%M') if isinstance(r['MULAI'], (datetime, time)) else str(r['MULAI'])
            selesai = r['SELESAI'].strftime('%H:%M') if isinstance(r['SELESAI'], (datetime, time)) else str(r['SELESAI'])
            gedung_req = r.get('GEDUNG')
            lantai_req = r.get('LANTAI')
            ruang_req = r.get('RUANG')

            if pd.notna(gedung_req) and pd.notna(lantai_req) and pd.notna(ruang_req):
                lantai_req = int(lantai_req)
                if gedung_req in AVAILABLE_ROOMS and                 lantai_req in AVAILABLE_ROOMS[gedung_req] and                 ruang_req in AVAILABLE_ROOMS[gedung_req][lantai_req]:
                    if is_room_available(df_jadwal, hari, mulai, selesai, gedung_req, lantai_req, ruang_req):
                        df_jadwal = pd.concat([df_jadwal, pd.DataFrame([{
                            'HARI': hari, 'DOSEN': dosen, 'MATAKULIAH': matkul, 'KELAS': kelas, 'PRODI': prodi,
                            'GEDUNG': gedung_req, 'LANTAI': lantai_req, 'RUANG': ruang_req, 'MULAI': mulai, 'SELESAI': selesai
                        }])], ignore_index=True)
                        jadwal_ditemukan = True
                        break
            elif pd.notna(gedung_req) and pd.notna(lantai_req):
                lantai_req = int(lantai_req)
                ruang_list = AVAILABLE_ROOMS.get(gedung_req, {}).get(lantai_req, [])
                for ruang in ruang_list:
                    if is_room_available(df_jadwal, hari, mulai, selesai, gedung_req, lantai_req, ruang):
                        df_jadwal = pd.concat([df_jadwal, pd.DataFrame([{
                            'HARI': hari, 'DOSEN': dosen, 'MATAKULIAH': matkul, 'KELAS': kelas, 'PRODI': prodi,
                            'GEDUNG': gedung_req, 'LANTAI': lantai_req, 'RUANG': ruang, 'MULAI': mulai, 'SELESAI': selesai
                        }])], ignore_index=True)
                        jadwal_ditemukan = True
                        break
                if jadwal_ditemukan:
                    break

        if not jadwal_ditemukan:
            for hari in ALLOWED_DAYS:
                for mulai, selesai in JAM_KULIAH:
                    if not is_time_slot_valid(mulai, selesai): continue
                    for gedung in AVAILABLE_ROOMS:
                        for lantai in preferensi:
                            ruang_list = AVAILABLE_ROOMS[gedung].get(lantai, [])
                            for ruang in ruang_list:
                                if is_room_available(df_jadwal, hari, mulai, selesai, gedung, lantai, ruang):
                                    df_jadwal = pd.concat([df_jadwal, pd.DataFrame([{
                                        'HARI': hari, 'DOSEN': dosen, 'MATAKULIAH': matkul, 'KELAS': kelas, 'PRODI': prodi,
                                        'GEDUNG': gedung, 'LANTAI': lantai, 'RUANG': ruang, 'MULAI': mulai, 'SELESAI': selesai
                                    }])], ignore_index=True)
                                    jadwal_ditemukan = True
                                    break
                            if jadwal_ditemukan: break
                        if jadwal_ditemukan: break
                    if jadwal_ditemukan: break
                if jadwal_ditemukan: break

        if not jadwal_ditemukan:
            gagal.append(row)

    return df_jadwal

def main():
    df_pengajaran = pd.read_excel('data_pengajaran.xlsx')
    df_pengajaran.columns = [col.strip().upper() for col in df_pengajaran.columns]

    try:
        df_request = pd.read_excel('request_dosen.xlsx')
        df_request.columns = [col.strip().upper() for col in df_request.columns]
    except FileNotFoundError:
        df_request = pd.DataFrame(columns=['DOSEN', 'MATAKULIAH', 'KELAS', 'HARI', 'MULAI', 'SELESAI', 'GEDUNG', 'LANTAI', 'RUANG'])

    print("\nMenjalankan penjadwalan otomatis...")
    df_jadwal = jadwal_otomatis_prioritas(df_pengajaran, df_request)

    # Simpan jadwal utama
    df_jadwal.to_excel('reservasi_ruangan.xlsx', index=False)
    print("\nJadwal utama disimpan di 'reservasi_ruangan.xlsx'.")

    # Simpan jadwal per HARI dan per DOSEN
    with pd.ExcelWriter('jadwal_perhari_perdosen.xlsx') as writer:
        for day in df_jadwal['HARI'].unique():
            df_jadwal[df_jadwal['HARI'] == day].to_excel(writer, sheet_name=f"HARI_{day}", index=False)

        for dosen in df_jadwal['DOSEN'].unique():
            sheet_name = f"DOSEN_{dosen[:25]}"
            df_jadwal[df_jadwal['DOSEN'] == dosen].to_excel(writer, sheet_name=sheet_name, index=False)

    print("Jadwal per hari dan per dosen disimpan di 'jadwal_perhari_perdosen.xlsx'.")

if __name__ == '__main__':
    main()