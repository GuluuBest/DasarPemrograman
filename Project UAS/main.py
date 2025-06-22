import pandas as pd
import re

def normalisasi_nama_dosen(nama):
    nama = nama.split("//")[0].strip()
    nama = re.sub(r"\s+", " ", nama)
    nama = nama.replace(" ,", ",").replace(" .", ".").replace(",", ", ")
    nama = nama.lower()

    gelar_map = {
        "s.sit": "S.Si.T.",
        "s.si.t": "S.Si.T.",
        "s.kom": "S.Kom.",
        "m.kom": "M.Kom.",
        "m.t": "M.T.",
        "mt": "M.T.",
        "m.stat": "M.Stat.",
        "m.mat": "M.Mat.",
        "ph.d": "Ph.D.",
        "drs.": "Drs.",
        "dr.": "Dr.",
        "st.": "S.T.",
        "s.t": "S.T."
    }

    for k, v in gelar_map.items():
        nama = re.sub(rf"\b{k}\b", v.lower(), nama)

    kata = []
    for w in nama.split():
        if w.endswith('.'):
            kata.append(w.upper())
        else:
            kata.append(w.capitalize())

    return ' '.join(kata)

def load_kelas_dari_excel(file_excel):
    xls = pd.ExcelFile(file_excel)
    sheets = ['angkatan 2022', 'angkatan 2023', 'angkatan 2024']
    semua_kelas = {}

    for sheet in sheets:
        df = xls.parse(sheet)
        kelas_data = extract_kelas_dan_jadwal(df)
        semua_kelas.update(kelas_data)

    return semua_kelas, sheets

def extract_kelas_dan_jadwal(df):
    kelas_dict = {}
    kelas_nama = None
    for i, row in df.iterrows():
        if isinstance(row.iloc[0], str) and "Kelas" in row.iloc[0]:
            kelas_nama = row.iloc[0].split(":")[1].strip().split(" ")[0]
            if kelas_nama not in kelas_dict:
                kelas_dict[kelas_nama] = []
        elif isinstance(row.iloc[2], str):
            if kelas_nama:
                kelas_dict[kelas_nama].append({
                    "mata_kuliah": row.iloc[2],
                    "hari": row.iloc[4] if pd.notna(row.iloc[4]) else "",
                    "jam": row.iloc[5] if pd.notna(row.iloc[5]) else "",
                    "dosen": row.iloc[7] if pd.notna(row.iloc[7]) else ""
                })
    return kelas_dict

daftar_ruangan = [
    {"gedung": "A", "lantai": 4, "ruangan": "Lab Software"},
    {"gedung": "A", "lantai": 4, "ruangan": "Lab Hardware"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4A"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4B"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4C"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4D"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4E"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4F"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4G"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4H"},
]

jadwal_terisi = []
jam_istirahat = ["12:00 - 13:00", "18:00 - 19:00"]

def validasi_jam_istirahat(hari, jam):
    waktu_istirahat = [
        ("12:00", "13:00"),  
        ("18:00", "19:00") 
    ]
    
    waktu_jumat = [("11:30", "13:30")]  

    mulai, selesai = jam.split(" - ")

    
    if hari.lower() == "jumat":
        for istirahat_mulai, istirahat_selesai in waktu_jumat:
            if (mulai < istirahat_selesai and selesai > istirahat_mulai):
                return False  

    
    for istirahat_mulai, istirahat_selesai in waktu_istirahat:
        if (mulai < istirahat_selesai and selesai > istirahat_mulai):
            return False  

    return True

def validasi_kelas_jadwal(kelas, hari, jam):
    if kelas.startswith("TI22M") or kelas.startswith("TI23M") or kelas.startswith("TI24M"):
        
        mulai, selesai = jam.split(" - ")
        if not ("18:00" <= mulai < "21:00" and "18:00" < selesai <= "21:00"):
            return False
    elif kelas.startswith("TI22B") or kelas.startswith("TI23B") or kelas.startswith("TI24B"):
        
        if hari.lower() != "sabtu":
            return False
    elif kelas.startswith("TI22C") or kelas.startswith("TI23C") or kelas.startswith("TI24C"):
        
        if hari.lower() != "minggu":
            return False
    return True

def ruangan_tersedia(hari, jam):
    if jam in jam_istirahat:
        return []

    tersedia = []
    for r in daftar_ruangan:
        bentrok = False
        for j in jadwal_terisi:
            if (j["gedung"] == r["gedung"] and j["lantai"] == r["lantai"] and j["ruangan"] == r["ruangan"] and j["hari"].lower() == hari.lower() and j["jam"] == jam):
                bentrok = True
                break
        if not bentrok:
            tersedia.append(r)
    return tersedia

def input_booking(jadwal_kelas_excel):
    print("\n=== Booking Jadwal Kuliah Dosen ===")

    angkatan_map = {}
    for kls in jadwal_kelas_excel.keys():
        prefix = kls[:5]
        angkatan = prefix[:4]
        angkatan_map.setdefault(angkatan, []).append(kls)

    angkatan_list = sorted(angkatan_map.keys())
    print("\nDaftar Angkatan:")
    for i, ang in enumerate(angkatan_list, 1):
        print(f"{i}. {ang}")

    while True:
        try:
            pilihan = int(input("Pilih nomor angkatan: ")) - 1
            angkatan_pilih = angkatan_list[pilihan]
            break
        except (ValueError, IndexError):
            print("Input salah! Masukkan angka sesuai daftar.")

    kelas_list = sorted(angkatan_map[angkatan_pilih])
    print(f"\nDaftar Kelas Angkatan {angkatan_pilih}:")
    for i, kls in enumerate(kelas_list, 1):
        print(f"{i}. {kls}")
    kelas = kelas_list[int(input("Pilih nomor kelas: ")) - 1]

    mata_kuliah_list = sorted(set(mk['mata_kuliah'] for mk in jadwal_kelas_excel[kelas] if mk['mata_kuliah'].lower() != "mata kuliah"))
    print(f"\nMata Kuliah untuk {kelas}:")
    for i, mk in enumerate(mata_kuliah_list, 1):
        print(f"{i}. {mk}")
    mata_kuliah = mata_kuliah_list[int(input("Pilih nomor mata kuliah: ")) - 1]

    print("\nMasukkan Hari dan Jam untuk kuliah:")
    hari = input("Hari (Senin - Minggu): ").strip()
    jam = input("Jam (contoh: 08:00 - 21:00): ").strip()

    
    if not validasi_jam_istirahat(hari, jam):
        print("Jadwal tidak valid karena melintasi waktu istirahat.")
        return

    if not validasi_kelas_jadwal(kelas, hari, jam):
        print(f"Jadwal tidak valid untuk kelas karyawan {kelas} pada hari {hari} dan jam {jam}.")
        return

    dosen_set = set()
    for kelas_data in jadwal_kelas_excel.values():
        for mk in kelas_data:
            if mk['mata_kuliah'] and mata_kuliah.strip().lower() in mk['mata_kuliah'].strip().lower():
                if mk['dosen']:
                    nama_bersih = normalisasi_nama_dosen(mk['dosen'])
                    dosen_set.add(nama_bersih)

    dosen_list = sorted(dosen_set)
    print(f"\nPilih Dosen Pengampu {mata_kuliah}:")
    for i, d in enumerate(dosen_list, 1):
        print(f"{i}. {d}")
    dosen = dosen_list[int(input("Pilih dosen: ")) - 1]

    for jadwal in jadwal_terisi:
        if (
            (jadwal['gedung'] == r['gedung'] and
             jadwal['lantai'] == r['lantai'] and
             jadwal['ruangan'] == r['ruangan'] and
             jadwal['hari'].lower() == hari.lower() and
             jadwal['jam'] == jam)
            or
            (jadwal['dosen'].lower() == dosen.lower() and jadwal['hari'].lower() == hari.lower() and jadwal['jam'] == jam)
        ):
            print("Jadwal bentrok! Ruangan atau dosen sudah terpakai pada waktu tersebut.")
            return

    ruangan_opsi = ruangan_tersedia(hari, jam)
    if not ruangan_opsi:
        print("Tidak ada ruangan tersedia pada waktu tersebut.")
        return

    print("\nRuangan Tersedia:")
    for idx, r in enumerate(ruangan_opsi, 1):
        print(f"{idx}. Gedung {r['gedung']} - Lantai {r['lantai']} - Ruangan {r['ruangan']}")

    pilihan = int(input("Pilih nomor ruangan: ")) - 1
    ruangan_pilih = ruangan_opsi[pilihan]

    jadwal_baru = {
        "kelas": kelas,
        "mata_kuliah": mata_kuliah,
        "dosen": dosen,
        "gedung": ruangan_pilih["gedung"],
        "lantai": ruangan_pilih["lantai"],
        "ruangan": ruangan_pilih["ruangan"],
        "hari": hari,
        "jam": jam
    }

    jadwal_terisi.append(jadwal_baru)
    print("\nJadwal berhasil dibooking!")

def tampilkan_jadwal():
    print("\n=== Daftar Jadwal Kuliah Terbooking ===")
    if not jadwal_terisi:
        print("(Kosong)")
    for i, j in enumerate(jadwal_terisi, 1):
        print(f"{i}. {j['dosen']} - {j['mata_kuliah']} ({j['kelas']}) di Gedung {j['gedung']} Lt.{j['lantai']} R.{j['ruangan']}, {j['hari']} {j['jam']}")

def export_jadwal(nama_file="booking_jadwal.xlsx"):
    if not jadwal_terisi:
        print("Belum ada data jadwal untuk diekspor.")
        return

    try:
        existing_df = pd.read_excel(nama_file)
    except FileNotFoundError:
        existing_df = pd.DataFrame()

    new_df = pd.DataFrame(jadwal_terisi)
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df = combined_df.drop_duplicates()

    combined_df.to_excel(nama_file, index=False)
    jadwal_terisi.clear()

    print(f"Jadwal berhasil diekspor {nama_file}")

def menu():
    file_excel = "jadwal.xlsx"  
    try:
        jadwal_kelas_excel, _ = load_kelas_dari_excel(file_excel)
    except Exception as e:
        print(f"Gagal memuat file Excel: {e}")
        return

    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Booking Jadwal")
        print("2. Tampilkan Jadwal")
        print("3. Export Jadwal")
        print("4. Keluar")

        pilihan = input("Pilih menu (1/2/3/4): ")

        if pilihan == "1":
            input_booking(jadwal_kelas_excel)
        elif pilihan == "2":
            tampilkan_jadwal()
        elif pilihan == "3":
            export_jadwal()
        elif pilihan == "4":
            print("Keluar dari aplikasi.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    menu()