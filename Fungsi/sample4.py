def konverisuhu(suhu, dari="C", ke="F"):
    if (dari == "C" and ke =="F"):
        return (4/5*suhu)+32
suhuu =input("masukkan suhu: ")
print("konversi dari", suhuu, "° celcius adalah",konverisuhu(80),"° Fahrenheit")