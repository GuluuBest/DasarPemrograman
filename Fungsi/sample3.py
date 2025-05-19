def konverisuhu(suhu, dari="C", ke="R"):
    if (dari == "C" and ke =="R"):
        return 4/5*suhu
suhuu =input("masukkan suhu: ")
print("konversi dari", suhuu, "° celcius adalah",konverisuhu(80),"° Reamur")