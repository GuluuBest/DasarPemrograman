def hitung_diskon(harga, persentase_diskon):
    diskon = harga * (persentase_diskon / 100)
    return max(harga - diskon, 0)

def hitung_pajak(harga, persentase_pajak):
    return harga * (persentase_pajak / 100)

def hitung_total(harga, persentase_diskon, persentase_pajak):
    harga_setelah_diskon = hitung_diskon(harga, persentase_diskon)
    pajak = hitung_pajak(harga_setelah_diskon, persentase_pajak)
    return harga_setelah_diskon + pajak