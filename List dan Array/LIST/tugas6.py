data = (1, 2, 3, 4, 5, 6)
jumlah_ganjil = 0

for angka in data:
    if angka % 2 == 1:
        jumlah_ganjil += 1

print("Jumlah angka ganjil:", jumlah_ganjil)
