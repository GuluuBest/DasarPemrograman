import pandas as pd
import matplotlib.pyplot as plt

file_path = 'Data_Penduduk.xlsx'
df =  pd.read_excel(file_path)

def kategori_penghasilan(penghasilan):
    if penghasilan < 2500000:
        return'Sangat Rendah'
    elif penghasilan < 5000000:
        return'Rendah'
    elif penghasilan < 10000000:
        return'Menengah'
    else:
        return'Sangat Tinggi'
    
df['Kategori_Penghasilan'] = df ['Penghasilan_Per_Bulan'].apply(kategori_penghasilan)

kategori_counts=df['Kategori_Penghasilan'].value_counts()

plt.figure(figsize=(8, 6))
plt.pie(
    kategori_counts,
    labels=kategori_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Paired.colors
)
plt.title('Distribusi Kategori Penghasilan Warga')
plt.axis('equal')
plt.tight_layout()
plt.show()