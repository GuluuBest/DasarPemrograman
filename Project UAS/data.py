import pandas as pd
import re


DAFTAR_RUANGAN = [
    {"gedung": "A", "lantai": 4, "ruangan": "Lab Software"},
    {"gedung": "A", "lantai": 4, "ruangan": "Lab Hardware"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4A"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4B"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4C"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4D"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4E"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4F"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4G"},
    {"gedung": "B", "lantai": 4, "ruangan": "B4H"},
]

JAM_ISTIRAHAT_NORMAL = [("12:00", "13:00"), ("18:00", "19:00")]
JAM_ISTIRAHAT_JUMAT = [("11:30", "13:30")]


def normalisasi_nama_dosen(nama):
    """Membersihkan dan menstandarisasi format nama dosen."""
    nama = str(nama).split("//")[0].strip()
    nama = re.sub(r"\s+", " ", nama).lower()
    
    gelar_map = {
        "s.sit": "S.Si.T.", "s.si.t": "S.Si.T.", "s.kom": "S.Kom.",
        "m.kom": "M.Kom.", "m.t": "M.T.", "mt": "M.T.", "m.stat": "M.Stat.",
        "m.mat": "M.Mat.", "ph.d": "Ph.D.", "drs.": "Drs.", "dr.": "Dr.",
        "st.": "S.T.", "s.t": "S.T."
    }

    for k, v in gelar_map.items():
        nama = re.sub(rf"\b{k}\b", v.lower(), nama)

    kata = [w.upper() if w.endswith('.') else w.capitalize() for w in nama.split()]
    return ' '.join(kata)


def extract_kelas_dan_jadwal(df):
    """Mengekstrak data kelas dan jadwal dari sebuah DataFrame pandas."""
    kelas_dict = {}
    kelas_nama = None
    for i, row in df.iterrows():
        if isinstance(row.iloc[0], str) and "Kelas" in row.iloc[0]:
            kelas_nama = row.iloc[0].split(":")[1].strip().split(" ")[0]
            if kelas_nama not in kelas_dict:
                kelas_dict[kelas_nama] = []
        elif kelas_nama and isinstance(row.iloc[2], str) and "Mata Kuliah" not in row.iloc[2]:
            kelas_dict[kelas_nama].append({
                "mata_kuliah": row.iloc[2],
                "hari": row.iloc[4] if pd.notna(row.iloc[4]) else "",
                "jam": row.iloc[5] if pd.notna(row.iloc[5]) else "",
                "dosen": row.iloc[7] if pd.notna(row.iloc[7]) else ""
            })
    return kelas_dict


def load_kelas_dari_excel(file_excel):
    """Memuat data jadwal dari semua sheet yang relevan di file Excel."""
    try:
        xls = pd.ExcelFile(file_excel)
        sheets_to_load = [sheet for sheet in xls.sheet_names if "angkatan" in sheet.lower()]
        semua_kelas = {}

        for sheet in sheets_to_load:
            df = xls.parse(sheet)
            kelas_data = extract_kelas_dan_jadwal(df)
            semua_kelas.update(kelas_data)
        
        return semua_kelas
    except FileNotFoundError:
        print(f"Error: File '{file_excel}' tidak ditemukan.")
        return None
    except Exception as e:
        print(f"Gagal memuat file Excel: {e}")
        return None



def validasi_jam_istirahat(hari, jam):
    """Memvalidasi apakah jam booking bentrok dengan waktu istirahat."""
    try:
        mulai, selesai = jam.split(" - ")
    except ValueError:
        print("Format jam salah. Harap gunakan format 'HH:MM - HH:MM'.")
        return False
        
    waktu_istirahat = JAM_ISTIRAHAT_JUMAT if hari.lower() == "jumat" else JAM_ISTIRAHAT_NORMAL

    for istirahat_mulai, istirahat_selesai in waktu_istirahat:
        if max(mulai, istirahat_mulai) < min(selesai, istirahat_selesai):
            return False
    return True


def validasi_kelas_jadwal(kelas, hari, jam):
    """Memvalidasi aturan khusus untuk kelas karyawan (malam, sabtu, minggu)."""
    try:
        mulai, selesai = jam.split(" - ")
    except ValueError:
        return False

    if kelas.upper().endswith("M"):  # Kelas Malam
        if not ("18:00" <= mulai and selesai <= "21:30"):
            return False
    elif kelas.upper().endswith("B"):  # Kelas Sabtu
        if hari.lower() != "sabtu":
            return False
    elif kelas.upper().endswith("C"):  # Kelas Minggu
        if hari.lower() != "minggu":
            return False
            
    return True