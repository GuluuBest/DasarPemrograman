alas = float(input("masukan alas segitiga: "))
tinggi = float(input("masukan tinggi segitiga: "))
luas = 0.5 * alas * tinggi
sisi_miring = (alas * 2 + tinggi * 2) * 0.5
keliling = alas + tinggi + sisi_miring
print(f"luas segitiga: {luas}")
print(f"keliling segitiga: {keliling}")