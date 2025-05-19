list = []
for i in range(2):
    angka = int(input(f"Angka ke-{i+1}:"))
    list.append(angka)

jumlah=sum(list)

rata_rata = jumlah / 2

maksimum = list[0]
minimum = list[0]

for angka in list:
    if angka > maksimum:
        maksimum = angka
    if angka < minimum:
        minimum = angka

print("list angka: ",list)
print("jumlah total: ",jumlah)
print("rata ratanya: ",rata_rata)
print("Nilai terbesar: ",maksimum)
print("Nilai terkecil: ",minimum)