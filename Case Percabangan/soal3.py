nilai = float(input("Masukan nilai siswa: "))
grade = "E"
if nilai >=90:
    grade = "A"
    predikat = "Dengan Pujian"
elif nilai >=80:
    grade = "B"
    predikat = "Sangat Memuaskan"
elif nilai >=70:
    grade = "C"
    predikat = "Memuaskan"
elif nilai >=60:
    grade = "D"
    predikat = "Tidak Memuaskan"
elif nilai >=0:
    grade = "D"
    predikat = "Tidak LULUS"

print ("Nilai Huruf: ",grade)
print ("Dengan Predikat: ",predikat)