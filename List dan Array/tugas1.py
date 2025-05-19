list = []
for i in range(10):
    angka = int(input(f"Angka ke-{i+1}: "))
    list.append(angka)
    
jumlah =sum(list)

print("list angka :",list)
print("jumlah semua elemen :", jumlah)