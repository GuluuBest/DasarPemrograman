import pandas as pd
from data import (
    DAFTAR_RUANGAN,
    load_kelas_dari_excel,
    normalisasi_nama_dosen,
    validasi_jam_istirahat,
    validasi_kelas_jadwal
)

jadwal_terisi = [] 

def ruangan_tersedia(hari, jam):
    """Mencari ruangan yang kosong pada hari dan jam tertentu."""
    tersedia = []
    for r in DAFTAR_RUANGAN:
        bentrok = False
        for j in jadwal_terisi:
            if (j["ruangan"] == r["ruangan"] and 
                j["gedung"] == r["gedung"] and 
                j["hari"].lower() == hari.lower() and 
                j["jam"] == jam):
                bentrok = True
                break
        if not bentrok:
            tersedia.append(r)
    return tersedia


def input_booking(jadwal_kelas_excel):
    """Fungsi untuk menangani alur proses booking dari pengguna."""
    print("\n=== Booking Jadwal Kuliah Dosen ===")

    angkatan_map = {kls[:4]: [] for kls in jadwal_kelas_excel.keys()}
    for kls in jadwal_kelas_excel.keys():
        angkatan_map[kls[:4]].append(kls)

    kelas = input("Masukkan nama kelas (contoh: TI23A): ").upper()
    if kelas not in jadwal_kelas_excel:
        print("Kelas tidak ditemukan.")
        return

    mata_kuliah = input("Masukkan nama mata kuliah: ")
    hari = input("Masukkan Hari (Senin - Minggu): ").strip().capitalize()
    jam = input("Masukkan Jam (contoh: 08:00-10:00): ").strip()
    dosen = input("Masukkan nama dosen pengampu: ")

    if not validasi_jam_istirahat(hari, jam):
        print("Jadwal tidak valid karena bertabrakan dengan waktu istirahat.")
        return
    if not validasi_kelas_jadwal(kelas, hari, jam):
        print(f"Jadwal tidak valid untuk tipe kelas {kelas} pada hari dan jam tersebut.")
        return

    for jadwal in jadwal_terisi:
        if (jadwal['dosen'].lower() == dosen.lower() and 
            jadwal['hari'].lower() == hari.lower() and 
            jadwal['jam'] == jam):
            print("Jadwal bentrok! Dosen sudah terpakai pada waktu tersebut.")
            return

    opsi_ruangan = ruangan_tersedia(hari, jam)
    if not opsi_ruangan:
        print("Tidak ada ruangan tersedia pada waktu tersebut.")
        return

    print("\nRuangan Tersedia:")
    for idx, r in enumerate(opsi_ruangan, 1):
        print(f"{idx}. Gedung {r['gedung']} - Lt {r['lantai']} - R. {r['ruangan']}")

    try:
        pilihan_ruangan_idx = int(input("Pilih nomor ruangan: ")) - 1
        ruangan_pilih = opsi_ruangan[pilihan_ruangan_idx]
    except (ValueError, IndexError):
        print("Pilihan tidak valid.")
        return

    jadwal_baru = {
        "kelas": kelas, "mata_kuliah": mata_kuliah, "dosen": dosen,
        "gedung": ruangan_pilih["gedung"], "lantai": ruangan_pilih["lantai"],
        "ruangan": ruangan_pilih["ruangan"], "hari": hari, "jam": jam
    }
    
    jadwal_terisi.append(jadwal_baru)
    print("\nJadwal berhasil dibooking!")


def tampilkan_jadwal():
    """Menampilkan semua jadwal yang sudah dibooking pada sesi ini."""
    print("\n=== Daftar Jadwal Kuliah Terbooking ===")
    if not jadwal_terisi:
        print("(Kosong)")
        return
    
    df = pd.DataFrame(jadwal_terisi)
    print(df.to_string(index=False))


def export_jadwal(nama_file="booking_jadwal.xlsx"):
    """Menyimpan jadwal yang dibooking ke file Excel."""
    if not jadwal_terisi:
        print("Belum ada data jadwal untuk diekspor.")
        return

    try:
        existing_df = pd.read_excel(nama_file)
        new_df = pd.DataFrame(jadwal_terisi)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True).drop_duplicates()
    except FileNotFoundError:
        combined_df = pd.DataFrame(jadwal_terisi)

    combined_df.to_excel(nama_file, index=False)
    jadwal_terisi.clear()
    print(f"Jadwal berhasil diekspor dan ditambahkan ke '{nama_file}'")


def menu():
    """Fungsi utama untuk menampilkan menu dan menjalankan aplikasi."""
    file_excel = "data_jadwal.xlsx"
    jadwal_kelas_excel = load_kelas_dari_excel(file_excel)
    if jadwal_kelas_excel is None:
        return
    while True:
        print("\n===== MENU UTAMA APLIKASI BOOKING =====")
        print("1. Booking Jadwal Baru")
        print("2. Tampilkan Jadwal (Sesi Ini)")
        print("3. Simpan Jadwal ke Excel")
        print("4. Keluar")

        pilihan = input("Pilih menu (1-4): ")

        if pilihan == "1":
            input_booking(jadwal_kelas_excel)
        elif pilihan == "2":
            tampilkan_jadwal()
        elif pilihan == "3":
            export_jadwal()
        elif pilihan == "4":
            print("Terima kasih telah menggunakan aplikasi.")
            break
        else:
            print("Pilihan tidak valid.")
        
        input("\nTekan Enter untuk melanjutkan...")


if __name__ == "__main__":
    menu()