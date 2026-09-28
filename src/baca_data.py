from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "BI7DRR.csv"

KOLOM_TANGGAL = "Tanggal"
KOLOM_RATE = "BI-7Day-RR"

# Kamus bulan: nama lengkap Indonesia dan singkatan Inggris/Indonesia
BULAN = {
    "januari": 1, "jan": 1,
    "februari": 2, "feb": 2, "pebruari": 2,
    "maret": 3, "mar": 3,
    "april": 4, "apr": 4,
    "mei": 5, "may": 5,
    "juni": 6, "jun": 6,
    "juli": 7, "jul": 7,
    "agustus": 8, "agu": 8, "agt": 8, "aug": 8,
    "september": 9, "sep": 9, "sept": 9,
    "oktober": 10, "okt": 10, "oct": 10,
    "november": 11, "nov": 11, "nop": 11,
    "desember": 12, "des": 12, "dec": 12,
}


def parse_tanggal(teks):
    """Ubah '20 Mei 2026' atau '22-Apr-26' menjadi Timestamp."""
    bagian = str(teks).strip().replace("-", " ").split()
    if len(bagian) != 3:
        raise ValueError(f"Format tanggal tidak dikenali: {teks!r}")
    hari, bulan, tahun = bagian
    bulan_no = BULAN.get(bulan.lower())
    if bulan_no is None:
        raise ValueError(f"Nama bulan tidak dikenali: {teks!r}")
    tahun = int(tahun)
    if tahun < 100:          # '26' -> 2026 (seluruh data berada di tahun 2000-an)
        tahun += 2000
    return pd.Timestamp(year=tahun, month=bulan_no, day=int(hari))


def baca_bi7drr(sumber=DATA_PATH, satuan="persen"):
    """
    Membaca BI7DRR.csv dan mengembalikan DataFrame dengan kolom:
    tanggal (datetime), rate (float). Urut dari tanggal terlama ke terbaru.
    satuan: 'persen' (5.25) atau 'desimal' (0.0525).
    """
    df = pd.read_csv(sumber, sep=",", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()

    for kolom in (KOLOM_TANGGAL, KOLOM_RATE):
        if kolom not in df.columns:
            raise KeyError(f"Kolom '{kolom}' tidak ada. Tersedia: {list(df.columns)}")

    # Konversi rate: hapus '%', jangan bergantung pada dtype (object/str berbeda antar versi pandas)
    rate = (df[KOLOM_RATE].astype("string")
            .str.replace("%", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip())
    rate = pd.to_numeric(rate, errors="raise").astype("float64")   # gagal keras; float64 biasa agar .values berupa array NumPy

    out = pd.DataFrame({
        "tanggal": df[KOLOM_TANGGAL].map(parse_tanggal),
        "rate": rate,
    })

    if satuan == "desimal":
        out["rate"] = out["rate"] / 100
    elif satuan != "persen":
        raise ValueError("satuan harus 'persen' atau 'desimal'")

    out = out.sort_values("tanggal").reset_index(drop=True)

    if out["tanggal"].duplicated().any():
        raise ValueError("Ada tanggal ganda pada data.")
    return out


if __name__ == "__main__":
    data = baca_bi7drr()
    r_data = data["rate"].values

    print("Path file   :", DATA_PATH)
    print("File ada?   :", DATA_PATH.exists())
    print("Jumlah data :", len(r_data))
    print("Periode     :", data["tanggal"].min().date(), "s.d.", data["tanggal"].max().date())
    print("5 data awal :", r_data[:5])
    print("Min / Max   :", r_data.min(), "/", r_data.max())
    print(data.dtypes)
