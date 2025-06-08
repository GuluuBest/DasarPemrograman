import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_excel = 'Data_Penduduk.xlsx'
df = pd.read_excel(file_excel)

grouped = df.groupby(['Pendidikan_Terakhir', 'Jenis_Kelamin']).size().unstack(fill_value=0)

labels = grouped.index
laki = grouped.get('Laki-laki', 0)
perempuan = grouped.get('Perempuan', 0)

x = np.arange(len(labels))
width = 0.35

plt.figure(figsize=(10, 6))
plt.barh(x - width/2, grouped['Laki-laki'], height=width, label='Laki-laki', color='#4a90e2')
plt.barh(x + width/2, grouped['Perempuan'], height=width, label='Perempuan', color='#f45b69')

plt.yticks(x, labels)
plt.xlabel('Jumlah Warga')
plt.title('Perbandingan Pendidikan dan Jenis Kelamin Warga (Horizontal)')
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
