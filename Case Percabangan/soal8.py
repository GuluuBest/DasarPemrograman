def jenis_segitiga (a,b,c):
    if a + b > c and a + c > b and b + c > a :
        if a == b == c :
            return "Segitiga sama sisi"
        elif a == b or a == c or b == c:
            return "Segitiga sama kaki"
        else:
            return "Segitiga sembarang"
    return "Bukan segitiga"

a = float(input("Masukan sisi pertama: "))
b = float(input("Masukan sisi kedua: "))
c = float(input("Masukan sisi ketiga: "))

print(jenis_segitiga(a, b, c))