import pandas as pd
from tabulate import tabulate
from datetime import datetime, time
import random # <--- IMPORT BARU

# --- KONFIGURASI --- (Sama seperti kode Anda, tidak ada perubahan)
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
    'TI': {'floors': [3, 4]}, 'SI': {'floors': [3, 4]}, 'DK': {'floors': [4, 5]},
    'SD': {'floors': [2, 3]}, 'HK': {'floors': [3, 4]}, 'ME': {'floors': [4, 5]},
    'EL': {'floors': [4, 5]}, 'AKT': {'floors': [2, 3]}, 'MJN': {'floors': [2, 3]},
}

ALLOWED_DAYS = ['SENIN', 'SELASA', 'RABU', 'KAMIS', 'JUMAT']
BREAKS = [
    (datetime.strptime("12:00", "%H:%M").time(), datetime.strptime("13:00", "%H:%M").time()),
    (datetime.strptime("18:00", "%H:%M").time(), datetime.strptime("19:00", "%H:%M").time())
]

JAM_KULIAH = [
    ("08:00", "10:00"), ("10:00", "12:00"), ("13:00", "15:00"),
    ("15:00", "17:00"), ("19:00", "21:00")
]

# --- FUNGSI-FUNGSI ---

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

# <--- FUNGSI BARU YANG KRUSIAL UNTUK MENCEGAH DOSEN BENTROK --->
def is_dosen_available(df, dosen, day, start_str, end_str):
    start_t = datetime.strptime(start_str, "%H:%M").time()
    end_t = datetime.strptime(end_str, "%H:%M").time()
    bookings = df[(df['HARI'] == day) & (df['DOSEN'] == dosen)]
    for _, row in bookings.iterrows():
        booked_start = datetime.strptime(row['MULAI'], "%H:%M").time()
        booked_end = datetime.strptime(row['SELESAI'], "%H:%M").time()
        if max(start_t, booked_start) < min(end_t, booked_end):
            return False
    return True

def add_schedule_entry(df, entry):
    """Fungsi pembantu untuk menambahkan entri jadwal."""
    return pd.concat([df, pd.DataFrame([entry])], ignore_index=True)

def jadwal_otomatis_prioritas(df_pengajaran, df_request):
    df_jadwal = pd.DataFrame(columns=['HARI', 'DOSEN', 'MATAKULIAH', 'KELAS', 'PRODI', 'GEDUNG', 'LANTAI', 'RUANG', 'MULAI', 'SELESAI'])
    gagal = []

    for _, row in df_pengajaran.iterrows():
        dosen, matkul, kelas, prodi = row['DOSEN'], row['MATAKULIAH'], row['KELAS'], row['PRODI']
        preferensi_lantai = ROOM_PREFERENCES.get(prodi, {'floors': list(range(2, 6))})['floors']
        jadwal_ditemukan = False

        request = df_request[(df_request['DOSEN'] == dosen) & (df_request['MATAKULIAH'] == matkul) & (df_request['KELAS'] == kelas)]

        if not request.empty:
            for _, r in request.iterrows():
                hari = r['HARI']
                mulai = r['MULAI'].strftime('%H:%M') if isinstance(r['MULAI'], (datetime, time)) else str(r['MULAI'])
                selesai = r['SELESAI'].strftime('%H:%M') if isinstance(r['SELESAI'], (datetime, time)) else str(r['SELESAI'])
                
                # Cek ketersediaan dosen dan validitas waktu request
                if not is_dosen_available(df_jadwal, dosen, hari, mulai, selesai) or not is_time_slot_valid(mulai, selesai):
                    continue

                gedung_req = r.get('GEDUNG')
                lantai_req = r.get('LANTAI')
                ruang_req = r.get('RUANG')

                # Prioritas 1: Request Lengkap (Gedung, Lantai, Ruang)
                if pd.notna(gedung_req) and pd.notna(lantai_req) and pd.notna(ruang_req):
                    lantai_req = int(lantai_req)
                    if is_room_available(df_jadwal, hari, mulai, selesai, gedung_req, lantai_req, ruang_req):
                        entry = {'HARI': hari, 'DOSEN': dosen, 'MATAKULIAH': matkul, 'KELAS': kelas, 'PRODI': prodi,
                                 'GEDUNG': gedung_req, 'LANTAI': lantai_req, 'RUANG': ruang_req, 'MULAI': mulai, 'SELESAI': selesai}
                        df_jadwal = add_schedule_entry(df_jadwal, entry)
                        jadwal_ditemukan = True
                        break
                
                # Prioritas 2: Request Sebagian (Gedung, Lantai)
                elif pd.notna(gedung_req) and pd.notna(lantai_req):
                    lantai_req = int(lantai_req)
                    ruang_list = AVAILABLE_ROOMS.get(gedung_req, {}).get(lantai_req, [])
                    random.shuffle(ruang_list) # Acak urutan ruangan
                    for ruang in ruang_list:
                        if is_room_available(df_jadwal, hari, mulai, selesai, gedung_req, lantai_req, ruang):
                            entry = {'HARI': hari, 'DOSEN': dosen, 'MATAKULIAH': matkul, 'KELAS': kelas, 'PRODI': prodi,
                                     'GEDUNG': gedung_req, 'LANTAI': lantai_req, 'RUANG': ruang, 'MULAI': mulai, 'SELESAI': selesai}
                            df_jadwal = add_schedule_entry(df_jadwal, entry)
                            jadwal_ditemukan = True
                            break
                    if jadwal_ditemukan: break
                
                # <--- PENINGKATAN: Prioritas 3: Request Hanya Waktu (Hari, Jam) --->
                elif pd.notna(hari) and pd.notna(mulai):
                    gedung_list = list(AVAILABLE_ROOMS.keys())
                    random.shuffle(gedung_list)
                    for gedung in gedung_list:
                        lantai_list = preferensi_lantai[:]
                        random.shuffle(lantai_list)
                        for lantai in lantai_list:
                            ruang_list = AVAILABLE_ROOMS[gedung].get(lantai, [])
                            random.shuffle(ruang_list)
                            for ruang in ruang_list:
                                if is_room_available(df_jadwal, hari, mulai, selesai, gedung, lantai, ruang):
                                    entry = {'HARI': hari, 'DOSEN': dosen, 'MATAKULIAH': matkul, 'KELAS': kelas, 'PRODI': prodi,
                                             'GEDUNG': gedung, 'LANTAI': lantai, 'RUANG': ruang, 'MULAI': mulai, 'SELESAI': selesai}
                                    df_jadwal = add_schedule_entry(df_jadwal, entry)
                                    jadwal_ditemukan = True
                                    break
                            if jadwal_ditemukan: break
                        if jadwal_ditemukan: break
                    if jadwal_ditemukan: break


        # Jika tidak ada request atau request tidak bisa dipenuhi, cari jadwal kosong
        if not jadwal_ditemukan:
            # <--- PENINGKATAN: Mengacak urutan pencarian agar jadwal lebih merata --->
            shuffled_days = ALLOWED_DAYS[:]
            random.shuffle(shuffled_days)
            shuffled_jam = JAM_KULIAH[:]
            random.shuffle(shuffled_jam)

            for hari in shuffled_days:
                for mulai, selesai in shuffled_jam:
                    if not is_time_slot_valid(mulai, selesai): continue
                    
                    # Cek ketersediaan dosen terlebih dahulu di slot waktu ini
                    if not is_dosen_available(df_jadwal, dosen, hari, mulai, selesai):
                        continue

                    shuffled_gedung = list(AVAILABLE_ROOMS.keys())
                    random.shuffle(shuffled_gedung)
                    for gedung in shuffled_gedung:
                        shuffled_lantai = preferensi_lantai[:]
                        random.shuffle(shuffled_lantai)
                        for lantai in shuffled_lantai:
                            ruang_list = AVAILABLE_ROOMS[gedung].get(lantai, [])
                            shuffled_ruang = ruang_list[:]
                            random.shuffle(shuffled_ruang)
                            for ruang in shuffled_ruang:
                                if is_room_available(df_jadwal, hari, mulai, selesai, gedung, lantai, ruang):
                                    entry = {'HARI': hari, 'DOSEN': dosen, 'MATAKULIAH': matkul, 'KELAS': kelas, 'PRODI': prodi,
                                             'GEDUNG': gedung, 'LANTAI': lantai, 'RUANG': ruang, 'MULAI': mulai, 'SELESAI': selesai}
                                    df_jadwal = add_schedule_entry(df_jadwal, entry)
                                    jadwal_ditemukan = True
                                    break
                            if jadwal_ditemukan: break
                        if jadwal_ditemukan: break
                    if jadwal_ditemukan: break
                if jadwal_ditemukan: break

        if not jadwal_ditemukan:
            gagal.append(row.to_dict())

    # --- Bagian output (tidak ada perubahan signifikan) ---
    if gagal:
        print("\nGagal dijadwalkan:")
        # <--- PENINGKATAN: Membuat DataFrame agar tabulate lebih stabil --->
        df_gagal = pd.DataFrame(gagal)
        print(tabulate(df_gagal, headers='keys', tablefmt='grid'))
    else:
        print("\nSemua pengajaran berhasil dijadwalkan.")
        
    print("\nJadwal Per Hari:")
    for day in ALLOWED_DAYS:
        if day in df_jadwal['HARI'].unique():
            print(f"\n--- {day} ---")
            df_day = df_jadwal[df_jadwal['HARI'] == day].sort_values(by=['MULAI', 'GEDUNG', 'LANTAI', 'RUANG'])
            print(tabulate(df_day, headers='keys', tablefmt='grid', showindex=False))

    print("\n\nJadwal Per Dosen:")
    for dosen in df_jadwal['DOSEN'].unique():
        print(f"\n--- Dosen: {dosen} ---")
        df_dosen = df_jadwal[df_jadwal['DOSEN'] == dosen].sort_values(by=['HARI', 'MULAI'])
        print(tabulate(df_dosen, headers='keys', tablefmt='grid', showindex=False))

    return df_jadwal

def main():
    try:
        df_pengajaran = pd.read_excel('data_pengajaran.xlsx')
        df_pengajaran.columns = [col.strip().upper() for col in df_pengajaran.columns]
    except FileNotFoundError:
        print("Error: File 'data_pengajaran.xlsx' tidak ditemukan! Program tidak bisa berjalan.")
        return

    try:
        df_request = pd.read_excel('request_dosen.xlsx')
        df_request.columns = [col.strip().upper() for col in df_request.columns]
    except FileNotFoundError:
        print("Info: File 'request_dosen.xlsx' tidak ditemukan. Melanjutkan tanpa data request.")
        df_request = pd.DataFrame(columns=['DOSEN', 'MATAKULIAH', 'KELAS', 'HARI', 'MULAI', 'SELESAI', 'GEDUNG', 'LANTAI', 'RUANG'])

    print("\nMenjalankan penjadwalan otomatis...")
    df_jadwal = jadwal_otomatis_prioritas(df_pengajaran, df_request)
    
    if not df_jadwal.empty:
        df_jadwal.to_excel('reservasi_ruangan.xlsx', index=False)
        print("\nJadwal disimpan di 'reservasi_ruangan.xlsx'.")
    else:
        print("\nTidak ada jadwal yang berhasil dibuat.")

if __name__ == '__main__':
    main()