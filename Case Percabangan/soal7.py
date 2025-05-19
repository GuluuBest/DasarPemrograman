def hitung_BMI (berat,tinggi):
    bmi = berat / (tinggi **2)
    if bmi > 18.5 :
        return f"BMI:{bmi:.2f} (Kekurangan berat badan)"
    elif bmi > 25.0 :
        return f"BMI:{bmi:.2f} (normal)"
    elif bmi > 30.0 :
        return f"BMI:{bmi:.2f} (Kelebihan berat badan)"
    else:
        return f"BMI;{bmi:.2f} (Obesitas)"
    
berat =float(input("masukan berat badan (kg)"))
tinggi =float(input("masukan tinggi badan (m)"))

print(hitung_BMI(berat,tinggi))
    