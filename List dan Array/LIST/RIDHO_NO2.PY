data_mahasiswa = {}

def tambah_data():
    NAMA = input("Masukan nama anda: ")
    NIM = input("Masukan nim anda: ")
    JURUSAN = input("Masukan jurusan anda: ")
    IPK = input("Masukan IPK anda: ")

    data_mahasiswa[NIM] = {
        "NAMA":NAMA ,
        "JURUSAN":JURUSAN,
        "IPK":IPK
    }

    print("Data Mahasiswa Berhasil Ditambahkan")

def tampilkan_semua():
    if not data_mahasiswa:
        print("Belum ada data mahasiswa.\n")
    else:
        print("Data Seluruh Mahasiswa:")
        for nim, info in data_mahasiswa.items():
            print(f"NIM: {nim}")
            print(f"  Nama    : {info['NAMA']}")
            print(f"  Jurusan : {info['JURUSAN']}")
            print(f"  IPK     : {info['IPK']}")
            print()

def cari_data():
    nim = input("Masukkan NIM yang ingin dicari: ")
    if nim in data_mahasiswa:
        info = data_mahasiswa[nim]
        print("Data Mahasiswa Ditemukan:")
        print(f"Nama    : {info['NAMA']}")
        print(f"Jurusan : {info['JURUSAN']}")
        print(f"IPK     : {info['IPK']}\n")
    else:
        print("Data mahasiswa dengan NIM tersebut tidak ditemukan.\n")

def hapus_data():
    nim = input("Masukkan NIM yang ingin dihapus: ")
    if nim in data_mahasiswa:
        del data_mahasiswa[nim]
        print("Data berhasil dihapus.\n")
    else:
        print("Data tidak ditemukan.\n")

while True:
    print("Menu Data Mahasiswa")
    print("A. Tambah data mahasiswa baru")
    print("B. Tampilkan semua data mahasiswa")
    print("C. Cari data mahasiswa berdasarkan NIM")
    print("D. Hapus data mahasiswa berdasarkan NIM")
    print("E. Keluar")
    pilihan = input("Pilih menu (A-E) gunakan huruf kapital: ")

    if pilihan == "A":
        tambah_data()
    elif pilihan == "B":
        tampilkan_semua()
    elif pilihan == "C":
        cari_data()
    elif pilihan == "D":
        hapus_data()
    elif pilihan == "E":
        print("Terima kasih, program selesai.")
        break
    else:
        print("Pilihan tidak valid. Silakan coba lagi.\n")