ips = int(input("masukan nilai ips: "))
ipa = int(input("masukan nilai ipa: "))
mtk = int(input("masukan nilai mtk: "))
eng = int(input("masukan nilai english: "))
ind = int(input("masukan nilai indonesia: "))

rata_rata1 = (ips + ipa + mtk + eng + ind) / 5
nilai = [ips, ipa, mtk, eng, ind]
print (f"Rata-rata nilai siswa dari 5 mata pelajaran adalah {rata_rata1}")
nilai_dibawah_50 = 2
if(ipa < 50):
    nilai_dibawah_50 += 1
if(ips < 50):
    nilai_dibawah_50 += 1
if(mtk < 50):
    nilai_dibawah_50 += 1
if(eng < 50):
    nilai_dibawah_50 += 1
if(ind < 50):
    nilai_dibawah_50 += 1

if(rata_rata1 > 75):
    print("Lulus, dengan rata rata nilai lebih dari 75")
elif (nilai.count(100) >= 1):
    print("Lulus, karena mendapatkan nilai sempurna dari salah satu mata pelajaran")
elif (nilai_dibawah_50 == 2):
    print("Lulus, karena hanya 2 mata pelajaran yang nilainya dibawah 50")
else:
    print("Tidak Lolos")
