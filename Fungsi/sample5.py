def konverisuhu(suhu, dari="C", ke="K"):
    if (dari == "C" and ke =="K"):
        return 273+suhu
suhuu =input("masukkan suhu: ")
print("konversi dari", suhuu, "° celcius adalah",konverisuhu(80),"° kelvin")