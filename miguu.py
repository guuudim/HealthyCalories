import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ==========================

# DATABASE SQLITE

# ==========================

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS konsumsi (
id INTEGER PRIMARY KEY AUTOINCREMENT,
tanggal TEXT,
nama TEXT,
kalori REAL,
protein REAL,
karbo REAL,
lemak REAL,
porsi INTEGER
)
""")
conn.commit()

# ==========================

# DATABASE MAKANAN

# ==========================

database_makanan = {
"Nasi Putih": {"kalori": 175, "protein": 3.5, "karbo": 40, "lemak": 0.3},
"Nasi Goreng": {"kalori": 350, "protein": 8, "karbo": 45, "lemak": 15},
"Mie Goreng": {"kalori": 380, "protein": 10, "karbo": 50, "lemak": 18},
"Ayam Goreng": {"kalori": 260, "protein": 22, "karbo": 5, "lemak": 15},
"Ayam Bakar": {"kalori": 230, "protein": 24, "karbo": 3, "lemak": 12},
"Rendang": {"kalori": 468, "protein": 22, "karbo": 8, "lemak": 38},
"Bakso": {"kalori": 220, "protein": 14, "karbo": 20, "lemak": 9},
"Soto Ayam": {"kalori": 190, "protein": 15, "karbo": 12, "lemak": 8},
"Tempe Goreng": {"kalori": 150, "protein": 8, "karbo": 9, "lemak": 9},
"Tahu Goreng": {"kalori": 130, "protein": 8, "karbo": 4, "lemak": 9},
"Telur Rebus": {"kalori": 78, "protein": 6, "karbo": 1, "lemak": 5},
"Apel": {"kalori": 95, "protein": 0.5, "karbo": 25, "lemak": 0.3},
"Pisang": {"kalori": 105, "protein": 1.3, "karbo": 27, "lemak": 0.4},
"Jeruk": {"kalori": 62, "protein": 1.2, "karbo": 15, "lemak": 0.2},
"Air Putih": {"kalori": 0, "protein": 0, "karbo": 0, "lemak": 0},
"Teh Manis": {"kalori": 90, "protein": 0, "karbo": 22, "lemak": 0},
"Kopi Hitam": {"kalori": 5, "protein": 0, "karbo": 1, "lemak": 0},
"Susu UHT": {"kalori": 130, "protein": 6, "karbo": 12, "lemak": 5}
}

# ==========================

# STREAMLIT UI

# ==========================

st.set_page_config(page_title="Healthy Calories", page_icon="🥗")

st.title("🥗 Healthy Calories")
st.subheader("Pemantauan Kalori dan Nutrisi Harian")

target_kalori = st.sidebar.number_input(
"Target Kalori Harian",
min_value=1000,
max_value=5000,
value=2000
)

st.header("➕ Tambah Konsumsi")

makanan = st.selectbox(
"Pilih Makanan/Minuman",
list(database_makanan.keys())
)

porsi = st.number_input(
"Jumlah Porsi",
min_value=1,
value=1
)

if st.button("Tambah Konsumsi"):

data = database_makanan[makanan]

kalori = data["kalori"] * porsi
protein = data["protein"] * porsi
karbo = data["karbo"] * porsi
lemak = data["lemak"] * porsi

tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")

c.execute("""
INSERT INTO konsumsi
(tanggal,nama,kalori,protein,karbo,lemak,porsi)
VALUES (?,?,?,?,?,?,?)
""",
(
    tanggal,
    makanan,
    kalori,
    protein,
    karbo,
    lemak,
    porsi
))

conn.commit()

st.success("Data berhasil disimpan!")

# ==========================

# LAPORAN HARIAN

# ==========================

st.header("📋 Laporan Konsumsi")

df = pd.read_sql_query(
"SELECT * FROM konsumsi",
conn
)

if not df.empty:

st.dataframe(df, use_container_width=True)

total_kalori = df["kalori"].sum()
total_protein = df["protein"].sum()
total_karbo = df["karbo"].sum()
total_lemak = df["lemak"].sum()

st.header("📊 Statistik Nutrisi")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Kalori", f"{total_kalori:.0f} kkal")
col2.metric("Protein", f"{total_protein:.1f} g")
col3.metric("Karbo", f"{total_karbo:.1f} g")
col4.metric("Lemak", f"{total_lemak:.1f} g")

st.subheader("Target Kalori Harian")

progress = min(total_kalori / target_kalori, 1.0)

st.progress(progress)

st.write(
    f"{total_kalori:.0f} / {target_kalori} kkal"
)

st.subheader("Grafik Kalori")

grafik = df.groupby("nama")["kalori"].sum()

st.bar_chart(grafik)


else:
st.info("Belum ada data konsumsi.")

# ==========================

# JADWAL MAKAN

# ==========================

st.header("⏰ Jadwal Makan Harian")

jadwal = pd.DataFrame({
"Waktu": [
"07:00",
"10:00",
"13:00",
"16:00",
"19:00"
],
"Kegiatan": [
"Sarapan",
"Snack Pagi",
"Makan Siang",
"Snack Sore",
"Makan Malam"
]
})

st.table(jadwal)

st.markdown("---")
st.caption("Healthy Calories © 2026")