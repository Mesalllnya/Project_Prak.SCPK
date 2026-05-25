import streamlit as st
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

# Konfigurasi halaman utama Streamlit
st.set_page_config(page_title="SPK Pemilihan Laptop - WP", page_icon="💻", layout="wide")

st.title("💻 Sistem Pendukung Keputusan Pemilihan Laptop")
st.markdown("Aplikasi ini menggunakan **Metode Weighted Product (WP)** untuk merekomendasikan laptop terbaik berdasarkan kriteria.")

# ================= SIDEBAR PENGATURAN BOBOT =================
st.sidebar.header("⚙️ Pengaturan Bobot Kriteria")
st.sidebar.markdown("Silakan atur bobot (1-10) untuk masing-masing kriteria.")
st.sidebar.markdown("**Catatan:** Harga bersifat **Cost** (semakin murah semakin baik), sedangkan kriteria lain bersifat **Benefit**.")

weight_cpu = st.sidebar.slider("Bobot CPU (Benefit)", 1, 10, 7)
weight_ram = st.sidebar.slider("Bobot RAM (Benefit)", 1, 10, 8)
weight_storage = st.sidebar.slider("Bobot Storage (Benefit)", 1, 10, 6)
weight_gpu = st.sidebar.slider("Bobot GPU (Benefit)", 1, 10, 7)
weight_price = st.sidebar.slider("Bobot Harga (Cost)", 1, 10, 9)

# ================= PROSES MEMBACA & MEMPROSES DATASET =================
@st.cache_data
def load_and_preprocess_data():
    df = pd.read_csv('dataset/laptop.csv')
    
    def extract_ram(ram_str):
        try: return int(re.search(r'\d+', str(ram_str)).group())
        except: return 0

    def extract_storage(storage_str):
        s = str(storage_str).upper()
        try:
            val = int(re.search(r'\d+', s).group())
            return val * 1024 if 'TB' in s else val
        except: return 0

    def score_cpu(cpu_str):
        s = str(cpu_str).upper()
        if any(x in s for x in ['I9', 'RYZEN 9', 'M5 MAX', 'ULTRA 9']): return 5
        if any(x in s for x in ['I7', 'RYZEN 7', 'M5 PRO', 'ULTRA 7', 'AI 9']): return 4
        if any(x in s for x in ['I5', 'RYZEN 5', 'M4', 'ULTRA 5']): return 3
        if any(x in s for x in ['I3', 'RYZEN 3', 'SNAPDRAGON']): return 2
        return 1

    def score_gpu(gpu_str):
        s = str(gpu_str).upper()
        if '4090' in s: return 10
        if '4080' in s or '5080' in s: return 9
        if '40-CORE' in s: return 9
        if '4070' in s: return 8
        if '4060' in s: return 7
        if '20-CORE' in s: return 6
        if '4050' in s: return 5
        if '3050' in s: return 4
        if any(x in s for x in ['ARC', 'IRIS', 'RADEON', 'ADRENO', '10-CORE']): return 3
        return 2

    df['RAM_Score'] = df['RAM'].apply(extract_ram)
    df['Storage_Score'] = df['Storage'].apply(extract_storage)
    df['CPU_Score'] = df['CPU'].apply(score_cpu)
    df['GPU_Score'] = df['GPU'].apply(score_gpu)
    df['Price_Score'] = df['Price_USD']
    
    return df

try:
    df = load_and_preprocess_data()
except FileNotFoundError:
    st.error("File 'laptop.csv' tidak ditemukan! Pastikan file CSV diletakkan di folder yang sama dengan script ini.")
    st.stop()

# ================= TAMPILAN DATASET UTAMA (SCROLL MANDIRI) =================
st.subheader("📋 Dataset Keseluruhan")
st.dataframe(df[['Laptop_ID', 'Brand', 'Model', 'CPU', 'RAM', 'Storage', 'GPU', 'Price_USD']], height=250)


# ================= GRAFIK TREN HARGA (KELIPATAN 100 DOLAR) =================
st.markdown("---")
st.subheader("📈 Grafik Tren Distribusi Harga Laptop")
st.markdown("Grafik di bawah ini menunjukkan tren jumlah laptop berdasarkan rentang interval kelipatan $100 USD.")

# Tentukan rentang bin kelipatan 100 secara dinamis
min_price = int(np.floor(df['Price_USD'].min() / 100) * 100)
max_price = int(np.ceil(df['Price_USD'].max() / 100) * 100)
bins = list(range(min_price, max_price + 101, 100))

# Hitung tren distribusi (frekuensi) menggunakan potongan bin (histogram)
df['Price_Bin'] = pd.cut(df['Price_USD'], bins=bins, right=False)
bin_counts = df['Price_Bin'].value_counts().sort_index()

# Ubah label interval menjadi format string yang rapi (misal: "$100 - $199")
bin_labels = [f"${bins[i]}-\${bins[i+1]-1}" for i in range(len(bins)-1)]

# Plot Grafik menggunakan Matplotlib (kombinasi Line dan Bar)
fig_trend, ax_trend = plt.subplots(figsize=(14, 5))
ax_trend.plot(bin_labels, bin_counts.values, marker='o', linestyle='-', color='purple', linewidth=2, markersize=6)
ax_trend.bar(bin_labels, bin_counts.values, color='purple', alpha=0.15, edgecolor='purple')

ax_trend.set_xticklabels(bin_labels, rotation=45, ha='right', fontsize=9)
ax_trend.set_ylabel('Jumlah Laptop', fontsize=10, fontweight='bold')
ax_trend.set_xlabel('Rentang Harga (USD)', fontsize=10, fontweight='bold')
ax_trend.set_title('Tren Kepadatan Jumlah Alternatif Laptop Berdasarkan Rentang Harga ($100 USD)', fontsize=12, fontweight='bold')
ax_trend.grid(axis='both', linestyle='--', alpha=0.5)

# Tampilkan angka presisi di atas setiap titik marker line plot
for i, txt in enumerate(bin_counts.values):
    if txt > 0:
        ax_trend.annotate(f'{txt}', (bin_labels[i], bin_counts.values[i]), textcoords="offset points", xytext=(0,7), ha='center', fontsize=8, fontweight='bold')

plt.tight_layout()
st.pyplot(fig_trend)


# ================= PROSES PERHITUNGAN METODE WP (PROSES SPK DALAM TABEL) =================
st.markdown("---")
st.subheader("📊 Tahapan Proses Perhitungan SPK (Metode WP)")

# 1. Menampung bobot pilihan user
weights = np.array([weight_cpu, weight_ram, weight_storage, weight_gpu, weight_price])

# 2. Normalisasi Bobot (Jumlah total bobot harus = 1)
w_normalized = weights / np.sum(weights)

# 3. Menentukan pangkat kriteria (Kriteria Harga negatif karena bersifat Cost)
w_wp = np.array([w_normalized[0], w_normalized[1], w_normalized[2], w_normalized[3], -w_normalized[4]])

# Menampilkan informasi bobot yang telah dinormalisasi
st.markdown("**1. Normalisasi Bobot Kriteria ($W_j$) dan Penentuan Pangkat:**")
df_weights_info = pd.DataFrame({
    'Kriteria': ['CPU (Benefit)', 'RAM (Benefit)', 'Storage (Benefit)', 'GPU (Benefit)', 'Harga (Cost)'],
    'Bobot Input User': weights,
    'Bobot Ternormalisasi ($W$)': [f"{w:.4f}" for w in w_normalized],
    'Pangkat Akhir WP ($W_{wp}$)': [f"{w:.4f}" for w in w_wp]
})
st.table(df_weights_info)

# 4. Menghitung Nilai Vektor S dan Vektor V untuk setiap alternatif
eps = 1e-9  
s_values = []
for index, row in df.iterrows():
    s = ( (row['CPU_Score'] + eps) ** w_wp[0] ) * \
        ( (row['RAM_Score'] + eps) ** w_wp[1] ) * \
        ( (row['Storage_Score'] + eps) ** w_wp[2] ) * \
        ( (row['GPU_Score'] + eps) ** w_wp[3] ) * \
        ( (row['Price_Score'] + eps) ** w_wp[4] )
    s_values.append(s)

df['S_Value'] = s_values
sum_s = np.sum(s_values)
df['V_Value'] = df['S_Value'] / sum_s

# Tampilkan tabel proses transformasi nilai kriteria menjadi Vektor S dan V
st.markdown("**2. Tabel Hasil Transformasi Skor Kriteria, Nilai Vektor S, dan Nilai Vektor V:**")
df_proses_spk = df[['Model', 'CPU_Score', 'RAM_Score', 'Storage_Score', 'GPU_Score', 'Price_Score', 'S_Value', 'V_Value']].copy()
# Format tampilan koma desimal panjang agar rapi di tabel
df_proses_spk['S_Value'] = df_proses_spk['S_Value'].map('{:.6f}'.format)
df_proses_spk['V_Value'] = df_proses_spk['V_Value'].map('{:.6f}'.format)

st.dataframe(df_proses_spk, height=300)


# ================= KESIMPULAN REKOMENDASI UTAMA =================
st.markdown("---")
st.subheader("🏆 Kesimpulan Akhir Rekomendasi")

# Mengurutkan dataset berdasarkan V_Value dari yang terbesar ke terkecil
df_sorted = df.sort_values(by='V_Value', ascending=False).reset_index(drop=True)
best_laptop = df_sorted.iloc[0]

st.success(f"Berdasarkan matriks penilaian serta pembobotan kriteria yang Anda tentukan, laptop yang mendapatkan rekomendasi tertinggi dan dinilai paling **Worth It** untuk dibeli adalah:")
st.markdown(f"### **🥇 {best_laptop['Model']}**")

# Menampilkan rincian laptop terbaik
col1, col2 = st.columns(2)
with col1:
    st.write("**Spesifikasi Laptop Pilihan Terbaik:**")
    st.write(f"- **CPU:** {best_laptop['CPU']} (Skor Kuantitatif: {best_laptop['CPU_Score']})")
    st.write(f"- **RAM:** {best_laptop['RAM']} ({best_laptop['RAM_Score']} GB)")
    st.write(f"- **Storage:** {best_laptop['Storage']}")
    st.write(f"- **GPU:** {best_laptop['GPU']} (Skor Kuantitatif: {best_laptop['GPU_Score']})")
with col2:
    st.write("**Hasil Nilai Perhitungan WP:**")
    st.write(f"- **Harga:** ${best_laptop['Price_USD']}")
    st.write(f"- **Nilai Vektor S (Produk Pangkat):** `{best_laptop['S_Value']:.6f}`")
    st.write(f"- **Skor Akhir Preferensi (Vektor V):** `{best_laptop['V_Value']:.6f}`")
    st.write(f"- **Status:** Peringkat 1 dari {len(df)} alternatif laptop.")

# Menampilkan tabel peringkat 5 besar
st.markdown("### 📋 Tabel 5 Besar Hasil Rekomendasi Terbaik")
st.dataframe(df_sorted[['Model', 'CPU', 'RAM', 'Storage', 'GPU', 'Price_USD', 'V_Value']].head(5), use_container_width=True)