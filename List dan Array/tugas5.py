belanjaan = []
for i in range(5):
    item = input(f"Masukan item belanja {i+1}: ")
    belanjaan.append(item)

hapus = input("Masukan nama item yang sudah di bayar: ")
if hapus in belanjaan:
    belanjaan.remove(hapus)
    print("daftar belanjaan yang belum di bayar: ")
else:
    print("item tidak ditemukan di daftar belanjaan")

print("list daftar belanja: ",belanjaan)