import streamlit as st
import pandas as pd
import re
from data import DAFTAR_RUANGAN

st.set_page_config(
    page_title="Sistem Booking Jadwal",
    layout="wide"
)

FILE_JADWAL_SUMBER = "data_jadwal.xlsx"
FILE_BOOKING_HASIL = "booking_jadwal.xlsx"

@st.cache_data
def load_data_from_mapping_sheet(file_path):
    TARGET_SHEET = "Mapping mata kuliah"
    try:
        xls = pd.ExcelFile(file_path)
        sheet_name = next((s_name for s_name in xls.sheet_names if TARGET_SHEET.lower() in s_name.lower()), None)
        if sheet_name is None:
            st.warning(f"Info: Tidak dapat menemukan sheet '{TARGET_SHEET}' di file `{file_path}`.")
            return pd.DataFrame(columns=['kelas', 'dosen'])
        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=2)
        required_columns = ['Kelas', 'Nama Dosen']
        if not all(col in df.columns for col in required_columns):
            st.error(f"GAGAL: Kolom yang dibutuhkan '{required_columns}' tidak ditemukan.")
            return None
        df = df[required_columns].rename(columns={'Kelas': 'kelas', 'Nama Dosen': 'dosen'})
        df.dropna(subset=['kelas', 'dosen'], inplace=True)
        return df
    except FileNotFoundError:
        st.info(f"File sumber `{file_path}` belum ditemukan. Data akan kosong.")
        return pd.DataFrame(columns=['kelas', 'dosen'])
    except Exception as e:
        st.error(f"Terjadi error saat membaca file Excel: {e}")
        return None

def load_booked_schedules():
    try:
        return pd.read_excel(FILE_BOOKING_HASIL)
    except FileNotFoundError:
        return pd.DataFrame()

def save_booked_schedules(df_booking):
    df_booking.to_excel(FILE_BOOKING_HASIL, index=False)

def cek_bentrok_jadwal(booking_baru, jadwal_tersimpan):
    if jadwal_tersimpan.empty:
        return None
    jadwal_list = jadwal_tersimpan.to_dict('records')
    mulai_baru_str, selesai_baru_str = booking_baru['Jam'].split(' - ')
    for jadwal_lama in jadwal_list:
        if 'Jam' not in jadwal_lama or not isinstance(jadwal_lama['Jam'], str):
            continue
        mulai_lama_str, selesai_lama_str = jadwal_lama['Jam'].split(' - ')
        if max(mulai_baru_str, mulai_lama_str) < min(selesai_baru_str, selesai_lama_str) and booking_baru['Hari'] == jadwal_lama['Hari']:
            if booking_baru['Ruangan'] == jadwal_lama['Ruangan'] and booking_baru['Gedung'] == jadwal_lama['Gedung']:
                return f"BENTROK: Ruangan {booking_baru['Ruangan']} sudah dipakai oleh {jadwal_lama['Dosen']} di jam tersebut."
            if booking_baru['Dosen'] == jadwal_lama['Dosen']:
                return f"BENTROK: Dosen {booking_baru['Dosen']} sudah ada jadwal di Ruangan {jadwal_lama['Ruangan']} pada jam tersebut."
    return None

master_df = load_data_from_mapping_sheet(FILE_JADWAL_SUMBER)
df_booking = load_booked_schedules()

st.title("Sistem Booking Jadwal Dosen")
st.write("Selamat datang di aplikasi penjadwalan. Klik panel di bawah untuk membuat booking baru.")

st.divider()
total_booking = len(df_booking)
total_kelas = master_df['kelas'].nunique() if master_df is not None and not master_df.empty else 0
col1_metric, col2_metric, col3_metric = st.columns(3)
col1_metric.metric(label="Total Jadwal di-Booking", value=total_booking)
col2_metric.metric(label="Total Kelas Terdaftar", value=total_kelas)
st.divider()

with st.expander("Klik di sini untuk membuat booking baru"):
    if master_df is not None:
        semua_kelas_unik = set(kls.strip().upper() for k_list in master_df['kelas'].dropna() for kls in str(k_list).split(','))
        angkatan_set = set(match.group(1) + match.group(2) for kls in semua_kelas_unik if (match := re.match(r'([a-zA-Z]+)(\d{2})', kls)))
        angkatan_options = sorted(list(angkatan_set))
        
        col1_form, col2_form = st.columns(2)

        with col1_form:
            angkatan_pilihan = st.selectbox("Pilih Angkatan", options=angkatan_options, index=None, placeholder="Pilih angkatan...")
            kelas_pilihan = None
            if angkatan_pilihan:
                options_kelas = sorted([kls for kls in semua_kelas_unik if kls.startswith(angkatan_pilihan)])
                kelas_pilihan = st.selectbox("Pilih Kelas", options=options_kelas, index=None, placeholder="Pilih kelas...")
            
            matkul_manual = st.text_input("Masukkan Mata Kuliah")
            all_dosen_options = sorted(master_df['dosen'].unique())
            dosen_pilihan = st.selectbox("Pilih Dosen", options=all_dosen_options, index=None, placeholder="Pilih dari semua dosen...")

        with col2_form:
            hari = st.selectbox("Pilih Hari", options=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=None)
            jam_manual = st.text_input("Masukkan Jam", placeholder="Contoh: 08:00 - 10:00")
            
            st.divider() 
            
            gedung_options = sorted(list(set(r['gedung'] for r in DAFTAR_RUANGAN)))
            gedung_pilihan = st.selectbox("Pilih Gedung", options=gedung_options, index=None, placeholder="Pilih gedung...")
            lantai_pilihan = None
            if gedung_pilihan:
                lantai_options = sorted(list(set(r['lantai'] for r in DAFTAR_RUANGAN if r['gedung'] == gedung_pilihan)))
                lantai_pilihan = st.selectbox("Pilih Lantai", options=lantai_options, index=None, placeholder="Pilih lantai...")
            ruangan_pilihan = None
            if gedung_pilihan and lantai_pilihan:
                ruangan_options = sorted([r['ruangan'] for r in DAFTAR_RUANGAN if r['gedung'] == gedung_pilihan and r['lantai'] == lantai_pilihan])
                ruangan_pilihan = st.selectbox("Pilih Ruangan", options=ruangan_options, index=None, placeholder="Pilih ruangan...")

        if st.button("Simpan Jadwal Booking", type="primary", use_container_width=True):
            if not all([angkatan_pilihan, kelas_pilihan, matkul_manual, dosen_pilihan, hari, jam_manual, gedung_pilihan, lantai_pilihan, ruangan_pilihan]):
                st.error("Semua field harus diisi dengan benar sebelum booking!")
            else:
                booking_baru = {
                    "Angkatan": angkatan_pilihan, "Kelas": kelas_pilihan, 
                    "Mata Kuliah": matkul_manual, "Dosen": dosen_pilihan, "Hari": hari, 
                    "Jam": jam_manual, "Gedung": gedung_pilihan, 
                    "Lantai": lantai_pilihan, "Ruangan": ruangan_pilihan
                }
                
                pesan_bentrok = cek_bentrok_jadwal(booking_baru, df_booking)
                
                if pesan_bentrok:
                    st.error(pesan_bentrok)
                else:
                    booking_baru_df = pd.DataFrame([booking_baru])
                    df_updated_booking = pd.concat([df_booking, booking_baru_df], ignore_index=True)
                    try:
                        save_booked_schedules(df_updated_booking)
                        st.success(f"Jadwal untuk {dosen_pilihan} di kelas {kelas_pilihan} berhasil dibooking!")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menyimpan booking: {e}")
    else:
        st.warning("Data sumber tidak dapat dimuat. Silakan periksa file data_jadwal.xlsx.")

st.divider()
st.header("Jadwal yang Sudah Terisi")
if df_booking.empty:
    st.info("Belum ada jadwal yang dibooking.")
else:
    st.dataframe(df_booking, use_container_width=True, hide_index=True)