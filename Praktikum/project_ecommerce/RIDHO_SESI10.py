from ecommerce.pricing import hitung_diskon, hitung_pajak, hitung_total
from ecommerce.order import generate_order_id

def main():
    nama_pelanggan = input("Masukan nama pelanggan: ")
    nama_produk = input("Masukan nama produk: ")
    harga_asli = float(input("Masukan harga asli: "))
    persentase_diskon = float(input("Masukan persentase diskon: "))
    persentase_pajak = float(input("Masukan persentase pajak: "))

    diskon = hitung_diskon(harga_asli, persentase_diskon)
    total = hitung_total(harga_asli, persentase_diskon, persentase_pajak)
    order_id = generate_order_id()

    print("="*40)
    print("=====RINCIAN PEMBELIAN=====")
    print("="*40)
    print(f"{'ID PESANAN':20}: {order_id}")
    print(f"{'Nama Pelanggan':20}: {nama_pelanggan}")
    print(f"{'Nama Produk':20}: {nama_produk}")
    print(f"{'Harga Asli':20}: {harga_asli:,.2f}")
    print(f"{'Diskon':20}: {diskon:,.2f}")
    print(f"{'Pajak':20}: {hitung_pajak(harga_asli - diskon, persentase_pajak):,.2f}")
    print("-"*40)
    print(f"{'Total Belanja':20}: Rp {total:,.2f}")
    print("="*40)

if __name__ == "__main__":
    main()