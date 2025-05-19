def cek_tipe(input1, input2, input3):
    if isinstance(input1, str) and isinstance(input2, int) and isinstance(input3,float):
        return "Tipe input valid!!"
    else:
        return "Tipe input tidak valid!!"
    
print(cek_tipe("Ridho", 20, 2.25))
print(cek_tipe(123, 10, 2.25))
print(cek_tipe("Ridho", 20, 2.25))
print(cek_tipe(2025, 10, "3.14"))
print(cek_tipe("Ridho", -5, 2.25))
