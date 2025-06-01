import pandas as pd

data = pd.read_excel('data_penjualan.xlsx')

print("Data 5 baris pertama:")
print(data.head())

data ['Total Harga'] = data['Jumlah'] * data['Harga Satuan']

print("\nData dengan kolom Total Harga:")
print(data.head())

data_elektronik = data[data['Kategori'] == 'Elektronik']

data_elektronik.to_excel("elektronik.xlsx", index=False)

print("\nData Elektronik berhasil disimpan")

rekap = data.groupby('Kategori')['Total Harga'].sum().reset_index()

rekap.columns = ['Kategori','Total Pendapatan']

print("\nRekap Penjualan per Kategori")
print(rekap)

data_sorted = data.sort_values(by='Total Harga', ascending=False)

data_sorted.to_excel("penjualan_terurut.xlsx", index=False)

print("\nData berhasil disimpan ke file penjualan_terurut.xlsx")