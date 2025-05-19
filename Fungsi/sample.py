from datetime import datetime

def hitungumur(tahunlahir):
    tahunini = datetime.now().year
    umur = tahunini - tahunlahir
    ##print("Umur",umur)
    return umur


tahunlahir = int(input("Masukan tahun lahir: "))
umur = hitungumur(tahunlahir)
print("Umur",umur, "Tahun")