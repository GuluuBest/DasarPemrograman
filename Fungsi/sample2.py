def listnama(nama):
    print("Halo", nama, "Selamat Datang")

def namalist(name):
    for nama in name :
        print("Halo",nama, "Selamat Datang")

name = ["Dodo","Panjul","Ucheng","Tomi"]
for nama in name :
    listnama(nama)

namalist(name)