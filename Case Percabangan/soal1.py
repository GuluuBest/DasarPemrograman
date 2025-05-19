angka = float(input("Masukan angka: "))
if angka > 0 :
    category = "Positif"
elif angka <0 :
    category = "Negatif"

print ("angka %s, termasuk ke dalam kategori %s" % 
       (angka,category))