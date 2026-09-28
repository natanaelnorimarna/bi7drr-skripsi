from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "BI7DRR.csv"


def baca_bi7drr(sumber, kolom="BI-7Day-RR"):
    df = pd.read_csv(sumber, sep=None, engine="python", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()

    if kolom not in df.columns:
        raise KeyError(f"Kolom '{kolom}' tidak ada. Tersedia: {list(df.columns)}")

    if df[kolom].dtype == object:
        df[kolom] = (df[kolom].astype(str)
                     .str.replace("%", "", regex=False)
                     .str.replace(",", ".", regex=False)
                     .str.strip())
    df[kolom] = pd.to_numeric(df[kolom], errors="coerce")
    return df


if __name__ == "__main__":
    df_csv = baca_bi7drr(DATA_PATH)
    r_data = df_csv["BI-7Day-RR"].dropna().values

    print("Path file  :", DATA_PATH)
    print("File ada?  :", DATA_PATH.exists())
    print("Jumlah data:", len(r_data))
    print("5 data awal:", r_data[:5])
    print("Min / Max  :", r_data.min(), "/", r_data.max())
    print(df_csv.dtypes)
