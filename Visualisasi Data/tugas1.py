import pandas as pd
import matplotlib.pyplot as plt

file_excel = 'Data_Penduduk.xlsx'
df = pd.read_excel(file_excel)
profesi_counts = df['Profesi'].value_counts()

plt.figure(figsize=(10, 6))
bars = plt.barh(profesi_counts.index, profesi_counts.values, color='skyblue')
plt.xlabel('Jumlah Warga')
plt.title('Jumlah Profesi Warga Desa Cibodas (Bar Chart)')
plt.tight_layout()
plt.show()

