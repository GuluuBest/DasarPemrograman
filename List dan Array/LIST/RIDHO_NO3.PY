data_barang = {}

def tambah_data():
    nama = input("Masukan nama anda: ")
    harga = input("Masukan nim anda: ")
    stok = input("Masukan jurusan anda: ")

    data_barang[nama] = {
        "HARGA":harga ,
        "STOK":stok,
    }

    print("Data Barang Berhasil Ditambahkan")

def tampilkan_semua():
    if not data_barang:
        print("Belum ada data barang.\n")
    else:
        print("{:<20} {:>10} {:>10}".format("Nama Barang", "Harga", "Stok"))
        print("-" * 42)
        for nama, (harga, stok) in data_barang.items():
            print("{:<20} {:>10} {:>10}".format(nama, harga, stok))
        print()

def cari_barang():
    nama = input("Masukkan nama barang yang dicari: ")
    if nama in data_barang:
        harga, stok = data_barang[nama]
        print(f"Nama Barang : {nama}")
        print(f"Harga       : {harga}")
        print(f"Stok        : {stok}\n")
    else:
        print("Barang tidak ditemukan.\n")

def perbarui_stok():
    nama = input("Masukkan nama barang yang ingin diperbarui: ")
    if nama in data_barang:
            stok_baru = int(input("Masukkan jumlah stok baru: "))
            harga_lama = data_barang[nama][0]
            data_barang[nama] = (harga_lama, stok_baru)
            print("Stok berhasil diperbarui.\n")
    else:
        print("Barang tidak ditemukan.\n")

def hapus_barang():
    nama = input("Masukkan nama barang yang ingin dihapus: ")
    if nama in data_barang:
        del data_barang[nama]
        print("Barang berhasil dihapus.\n")
    else:
        print("Barang tidak ditemukan.\n")

def analisis_data():
    if not data_barang:
        print("Belum ada data untuk dianalisis.\n")
        return

    harga_tertinggi = max(data_barang.items(), key=lambda x: x[1][0])
    harga_terendah = min(data_barang.items(), key=lambda x: x[1][0])
    total_nilai_stok = sum(harga * stok for harga, stok in data_barang.values())

    print(f"Barang dengan harga tertinggi: {harga_tertinggi[0]} (Rp{harga_tertinggi[1][0]})")
    print(f"Barang dengan harga terendah: {harga_terendah[0]} (Rp{harga_terendah[1][0]})")
    print(f"Total nilai stok: Rp{total_nilai_stok}\n")

def menu():
    while True:
        print("MENU MANAJEMEN DATA BARANG")
        print("1. Tambah Barang Baru")
        print("2. Tampilkan Semua Barang")
        print("3. Cari Barang")
        print("4. Perbarui Stok Barang")
        print("5. Hapus Barang")
        print("6. Analisis Data")
        print("7. Keluar Program")
        pilihan = input("Pilih menu (1-7): ")

        if pilihan == "1":
            tambah_data()
        elif pilihan == "2":
            tampilkan_semua()
        elif pilihan == "3":
            cari_barang()
        elif pilihan == "4":
            perbarui_stok()
        elif pilihan == "5":
            hapus_barang()
        elif pilihan == "6":
            analisis_data()
        elif pilihan == "7":
            print("Terima kasih, program selesai.")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.\n")

menu()