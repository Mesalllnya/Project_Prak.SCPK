import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="pemilihan laptop - WP", layout="wide")

def konversi_storage(x):
    text = str(x).strip().upper()
    angka_text = "".join([char for char in text if char.isdigit()])
    if not angka_text :
        return 0
    angka = float(angka_text)
        
    if "TB" in text:
        return angka * 1024
    return angka

def konversi_ram(x):  
    text = str(x).strip().upper()
    angka_text = "".join([char for char in text if char.isdigit()])
    if not angka_text:
        return 0 
    return float(angka_text)
    
def konversi_Price(x):
    return float(x)



#sidebar
with st.sidebar:

#page
    page = st.selectbox("pilih halaman",[
        "Data RAW",
        "Data CPU",
        "Data GPU",
        "WP",
        "Visualisasi"
    ])

    st.markdown("___")
    st.header("Pengaturan Bobot Kiteria")
    st.markdown("Atur bobot dengan skala 1-5")
    st.markdown("1: Sangat Tidak Penting  \n2: Tidak Penting  \n3: Cukup Penting  \n4: Penting  \n5: Sangat Penting")

#.slider
    bobot_cpu = st.slider("Bobot CPU (Benefit)", 1, 5, 3)
    bobot_gpu = st.slider("Bobot GPU (Benefit)", 1, 5, 3)
    bobot_ram = st.slider("Bobot RAM (Benefit)", 1, 5, 3)
    bobot_storage = st.slider("Bobot Storage (Benefit)", 1, 5, 3)
    bobot_harga = st.slider("Bobot Harga (Cost)", 1, 5, 3)


#table alternatif
if page == "Data RAW" : 
    st.title("💻 Sistem Pendukung Keputusan Pemilihan Laptop")
    st.markdown("Aplikasi ini menggunakan **Metode Weighted Product (WP)** untuk merekomendasikan laptop terbaik berdasarkan kriteria.")


    st.markdown("### 📋 Kriteria Evaluasi Sistem")
    st.write("Berikut adalah kriteria yang digunakan dalam perhitungan beserta sifatnya (Benefit/Cost):")
    
    # Membuat 5 kolom untuk 5 kriteria
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        with st.container(border=True):
            st.markdown("<b style='color: #2ecc71; font-size: 17px;'>💻 CPU</b>", unsafe_allow_html=True)
            st.markdown("<span style='background-color: #1e3a1e; color: #2ecc71; padding: 2px 8px; border-radius: 5px; font-size: 12px; font-weight: bold;'>BENEFIT</span>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 13px; margin-top: 8px; color: #cbd5e1;'>Diukur dari nilai <i>multiScore</i> benchmark CPU. Semakin tinggi semakin baik.</p>", unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            st.markdown("<b style='color: #2ecc71; font-size: 17px;'>🎮 GPU</b>", unsafe_allow_html=True)
            st.markdown("<span style='background-color: #1e3a1e; color: #2ecc71; padding: 2px 8px; border-radius: 5px; font-size: 12px; font-weight: bold;'>BENEFIT</span>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 13px; margin-top: 8px; color: #cbd5e1;'>Diukur dari skor <i>3DMark</i> grafis. Semakin tinggi semakin bertenaga.</p>", unsafe_allow_html=True)

    with col3:
        with st.container(border=True):
            st.markdown("<b style='color: #2ecc71; font-size: 17px;'>⚡ RAM</b>", unsafe_allow_html=True)
            st.markdown("<span style='background-color: #1e3a1e; color: #2ecc71; padding: 2px 8px; border-radius: 5px; font-size: 12px; font-weight: bold;'>BENEFIT</span>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 13px; margin-top: 8px; color: #cbd5e1;'>Kapasitas memori (GB). Semakin besar mendukung multitasking berat.</p>", unsafe_allow_html=True)

    with col4:
        with st.container(border=True):
            st.markdown("<b style='color: #2ecc71; font-size: 17px;'>💾 Storage</b>", unsafe_allow_html=True)
            st.markdown("<span style='background-color: #1e3a1e; color: #2ecc71; padding: 2px 8px; border-radius: 5px; font-size: 12px; font-weight: bold;'>BENEFIT</span>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 13px; margin-top: 8px; color: #cbd5e1;'>Kapasitas penyimpanan data (GB). Semakin besar semakin lapang.</p>", unsafe_allow_html=True)

    with col5:
        with st.container(border=True):
            st.markdown("<b style='color: #e74c3c; font-size: 17px;'>💰 Harga</b>", unsafe_allow_html=True)
            st.markdown("<span style='background-color: #3a1e1e; color: #e74c3c; padding: 2px 8px; border-radius: 5px; font-size: 12px; font-weight: bold;'>COST</span>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 13px; margin-top: 8px; color: #cbd5e1;'>Harga laptop dalam USD. Semakin murah/kecil nilainya semakin baik.</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.write("Data Alternatif Laptop")
    df_laptop = pd.read_csv('dataset/laptop.csv')
    df_claptop = df_laptop.drop(columns=["Laptop_ID"]+["Performance_Level"])
    df_claptop.index = df_claptop.index + 1
    st.dataframe(df_claptop)
    st.session_state["df_rawlaptop"] = df_claptop

#table CPU
if page == "Data CPU" :
    if "df_rawlaptop" in st.session_state:
        df_claptop = st.session_state["df_rawlaptop"]
        
        st.title("🖥️ Analisis & Pemrosesan Data CPU")
        st.markdown("Halaman ini mengelola kecocokan data spesifikasi prosesor antara unit alternatif laptop dengan skor benchmark performa multithreading.")

        # --- BAGIAN UI: KARTU INFORMASI KRITERIA CPU ---
        with st.container(border=True):
            col_icon, col_desc = st.columns([1, 11])
            with col_icon:
                st.markdown("<h1 style='text-align: center; margin: 0;'>⚙️</h1>", unsafe_allow_html=True)
            with col_desc:
                st.markdown("<b style='color: #2ecc71; font-size: 18px;'>Kriteria Utama: CPU Performance</b>", unsafe_allow_html=True)
                st.markdown("<span style='background-color: #1e3a1e; color: #2ecc71; padding: 3px 10px; border-radius: 5px; font-size: 12px; font-weight: bold;'>BENEFIT CRITERION</span>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='font-size: 14px; margin-top: 8px; color: #cbd5e1; line-height: 1.4;'>"
                    "Performa CPU diukur berdasarkan standarisasi nilai <b>multiScore</b> dari data benchmark. "
                    "Semakin tinggi skor <i>multiScore</i>, maka kemampuan komputasi paralel, rendering, dan multitasking "
                    "pada laptop akan dinilai semakin baik dan mendapatkan prioritas utama dalam pembobotan WP."
                    "</p>", 
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        df_cpu = pd.read_csv('dataset/CPU.csv')
        df_cpu["CPU"] = df_cpu["manufacturer"].astype(str) + " " + df_cpu["namaCPU"].astype(str)
        df_ccpu = df_cpu.drop(columns =["manufacturer", "namaCPU", "singleScore","cores","threads","baseClock","turboClock","type"])
        kolom_baru_cpu = ["CPU","multiScore"]
        df_ccpu = df_ccpu[kolom_baru_cpu]
        #df_laptopcpu = pd.merge(df_claptop,df_ccpu, on = "CPU")
        #st.dataframe(df_laptopcpu)

        #tablelaptopcpu
        df_claptop["CPU_Clean"] = df_claptop["CPU"].astype(str).str.split().str[0:3].str.join(' ')
        df_ccpu["CPU_Clean"] = df_cpu["CPU"].astype(str).str.split().str[0:3].str.join(' ')
        df_laptopcpu = pd.merge(df_claptop, df_ccpu, on="CPU_Clean", how="left")
        df_dislaptopcpu = df_laptopcpu.drop(columns=["CPU_Clean","Brand","RAM","GPU","Price_USD","CPU_x","Storage"])
        df_dislaptopcpu = df_dislaptopcpu.rename(columns={"CPU_y": "CPU"})
        df_dislaptopcpu["multiScore"] = pd.to_numeric(df_dislaptopcpu["multiScore"], errors="coerce")
        df_sortcpu = df_dislaptopcpu.sort_values(by="multiScore", ascending=False)
        df_fixlaptopcpu = df_sortcpu.drop_duplicates(subset="Model", keep="first")
        df_fixlaptopcpu = df_fixlaptopcpu.reset_index(drop=True)
        df_fixlaptopcpu.index = df_fixlaptopcpu.index + 1
        st.session_state["df_fixlaptopcpu"] = df_fixlaptopcpu


        # --- BAGIAN UI: INTERAKTIF TABS UNTUK MENAMPILKAN TABEL ---
        tab1, tab2 = st.tabs(["📊 Hasil Pemetaan Laptop & CPU", "📂 Dataset Raw CPU Benchmark"])
        
        with tab1:
            st.markdown("#### 🎯 Hasil Akhir Pemrosesan Nilai CPU Laptop")
            st.caption("Data alternatif laptop yang telah sukses dipetakan dengan nilai multiScore CPU yang telah diurutkan dari skor tertinggi:")
            st.dataframe(df_fixlaptopcpu, use_container_width=True)
            
        with tab2:
            st.markdown("#### 📑 Seluruh Database CPU Benchmark")
            st.caption("Referensi mentah tabel database performa CPU berdasarkan data benchmark global:")
            st.dataframe(df_ccpu.drop(columns=["CPU_Clean"], errors="ignore"), use_container_width=True)

    else:
        st.warning("error")

#tablegpu
if page == "Data GPU":
    if "df_rawlaptop" in st.session_state:
        df_claptop = st.session_state["df_rawlaptop"]

        st.title("🎮 Analisis & Pemrosesan Data GPU")
        st.markdown("Halaman ini mengelola kecocokan data spesifikasi kartu grafis (GPU) antara unit alternatif laptop dengan skor benchmark performa olah grafis.")

        # --- BAGIAN UI: KARTU INFORMASI KRITERIA GPU ---
        with st.container(border=True):
            col_icon, col_desc = st.columns([1, 11])
            with col_icon:
                st.markdown("<h1 style='text-align: center; margin: 0;'>🎮</h1>", unsafe_allow_html=True)
            with col_desc:
                st.markdown("<b style='color: #2ecc71; font-size: 18px;'>Kriteria Utama: GPU Performance</b>", unsafe_allow_html=True)
                st.markdown("<span style='background-color: #1e3a1e; color: #2ecc71; padding: 3px 10px; border-radius: 5px; font-size: 12px; font-weight: bold;'>BENEFIT CRITERION</span>", unsafe_allow_html=True)
                st.markdown(
                    "<p style='font-size: 14px; margin-top: 8px; color: #cbd5e1; line-height: 1.4;'>"
                    "Performa kartu grafis diukur berdasarkan standarisasi nilai skor <b>3DMark (G3Dmark)</b>. "
                    "Semakin tinggi nilai skor grafis ini, maka kemampuan rendering 3D, gaming, editing video, "
                    "serta pemrosesan AI pada laptop akan dinilai semakin bertenaga dan mendapatkan prioritas utama dalam pembobotan WP."
                    "</p>", 
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        st.write("Nilai GPU (3DMark)")
        df_gpu = pd.read_csv('dataset/GPU.csv')
        df_cgpu = df_gpu.drop(columns =["G2Dmark","price","gpuValue","TDP","powerPerformance","testDate","category"])
        df_cgpu = df_cgpu.rename(columns={"gpuName": "GPU", "G3Dmark" : "3DMark"})
        df_cgpu.index = df_cgpu.index + 1
        #df_laptopcpu = pd.merge(df_claptop,df_ccpu, on = "CPU")
        #st.dataframe(df_cgpu)
        #st.dataframe(df_laptopcpu)

        st.write("Nilai Laptop dan GPU")
        df_claptop["GPU_Clean"] = df_claptop["GPU"].astype(str).str.split().str[0:1].str.join(' ')
        df_cgpu["GPU_Clean"] = df_cgpu["GPU"].astype(str).str.split().str[0:1].str.join(' ')
        df_laptopgpu = pd.merge(df_claptop, df_cgpu, on="GPU_Clean", how="left")
        df_dislaptopgpu = df_laptopgpu.drop(columns=["GPU_Clean","Brand","RAM","CPU","Price_USD","GPU_x","Storage","CPU_Clean"])
        df_dislaptopgpu = df_dislaptopgpu.rename(columns={"GPU_y": "GPU"})
        df_dislaptopgpu["3DMark"] = pd.to_numeric(df_dislaptopgpu["3DMark"], errors="coerce")
        df_sortgpu = df_dislaptopgpu.sort_values(by="3DMark", ascending=False)
        df_fixlaptopgpu = df_sortgpu.drop_duplicates(subset="Model", keep="first")
        df_fixlaptopgpu = df_fixlaptopgpu.reset_index(drop=True)
        df_fixlaptopgpu.index = df_fixlaptopgpu.index + 1
        #st.dataframe(df_fixlaptopgpu)
        st.session_state["df_fixlaptopgpu"] = df_fixlaptopgpu

        # --- BAGIAN UI: INTERAKTIF TABS UNTUK MENAMPILKAN TABEL ---
        tab1, tab2 = st.tabs(["📊 Hasil Pemetaan Laptop & GPU", "📂 Dataset Raw GPU Benchmark"])
        
        with tab1:
            st.markdown("#### 🎯 Hasil Akhir Pemrosesan Nilai GPU Laptop")
            st.caption("Data alternatif laptop yang telah sukses dipetakan dengan nilai skor grafis 3DMark yang telah diurutkan dari skor tertinggi:")
            st.dataframe(df_fixlaptopgpu, use_container_width=True)
            
        with tab2:
            st.markdown("#### 📑 Seluruh Database GPU Benchmark")
            st.caption("Referensi mentah tabel database performa kartu grafis (GPU) berdasarkan data benchmark global 3DMark:")
            st.dataframe(df_cgpu.drop(columns=["GPU_Clean"], errors="ignore"), use_container_width=True)

if page == "WP" :
    if "df_rawlaptop" in st.session_state and "df_fixlaptopcpu" in st.session_state and "df_fixlaptopgpu" in st.session_state:
        df_claptop = st.session_state["df_rawlaptop"]
        df_fixlaptopcpu = st.session_state["df_fixlaptopcpu"]
        df_fixlaptopgpu = st.session_state["df_fixlaptopgpu"]


        #st.dataframe(df_claptop)
        #$st.dataframe(df_fixlaptopcpu)
        #st.dataframe(df_fixlaptopgpu)
        st.title("🧮 Proses Perhitungan Metode Weighted Product (WP)")
        st.markdown("Halaman ini menampilkan transparansi kalkulasi matematis Multi-Criteria Decision Making (MCDM) menggunakan algoritma Weighted Product.")
#datafinal
    with st.expander("🛠️ Langkah 1: Penggabungan & Transformasi Tipe Data", expanded=False):
        st.markdown("#### **Penggabungan Tabel Spesifikasi & Nilai Benchmark**")
        st.caption("Menggabungkan dataset laptop utama dengan nilai multiScore CPU dan 3DMark GPU berdasarkan pencocokan nama komponen:")

        st.write("Data Final")
        df_step1 =  pd.merge(df_claptop,df_fixlaptopcpu, on="Model", how="left")
        df_stepfinal = pd.merge(df_step1,df_fixlaptopgpu, on="Model", how="left")
        df_final = df_stepfinal.dropna()
        df_datafinal = df_final.drop(columns=["Brand","CPU_x","GPU_x","CPU_Clean","GPU_Clean","CPU_y","GPU_y"])
        st.dataframe(df_datafinal)

#konversi semua ke float
        st.markdown("#### **Hasil Konversi Nilai Kriteria Menjadi Numerik (Float)**")
        st.caption("Mengubah teks kapasitas Storage (GB), RAM (GB), dan Harga menjadi angka koma agar bisa diproses secara matematis:")

        df_datafinal["Storage"] = df_datafinal["Storage"].apply(konversi_storage)
        df_datafinal["RAM"] = df_datafinal["RAM"].apply(konversi_ram)
        df_datafinal["Price_USD"] = df_datafinal["Price_USD"].apply(konversi_Price)
        st.dataframe(df_datafinal)
        #df_datafinal.info()

#WP method

    with st.expander("⚖️ Langkah 2: Perbaikan Bobot Kriteria (Normalisasi)", expanded=False):
        st.markdown("#### **Tabel Bobot Kriteria**")
        st.markdown(
            "Sesuai kaidah Weighted Product, bobot awal dari slider diperbaiki sehingga total seluruh bobot bernilai 1 ($\sum w = 1$). "
            "Pangkat bernilai positif jika kriteria bersifat **Benefit**, dan negatif jika kriteria bersifat **Cost**."
            )

        nama_kriteria = (["CPU","GPU","RAM","Storage","Harga"])
        bobot_awal = np.array([bobot_cpu,bobot_gpu,bobot_ram,bobot_storage,bobot_harga])
        k = np.array([1,1,1,1,-1])

        total_bobot_awal = np.sum(bobot_awal)
        norm_bobot = bobot_awal / total_bobot_awal


        df_bobot = pd.DataFrame({
            "Nama Kriteria": nama_kriteria,
            "Bobot Kriteria":  bobot_awal,
            "Bobot Ternormalisasi": np.round(norm_bobot,4)
        })
        df_bobot.index = df_bobot.index + 1
        st.dataframe(df_bobot)

        kolom_kriteria = ["multiScore","3DMark","RAM","Storage","Price_USD"]
        matrix_x = df_datafinal[kolom_kriteria].to_numpy()
        #RumusWP
        
        vektor_s = np.prod((matrix_x + 1e-9) ** (k * norm_bobot), axis=1)

        vektor_v = vektor_s / np.sum(vektor_s)

        df_wp_result = df_datafinal.copy()
        df_wp_result["Vektor_S"] = vektor_s
        df_wp_result["Vektor_V"] = vektor_v

    with st.expander("🔢 Langkah 3: Matriks Perhitungan Vektor S", expanded=False):
        st.markdown("#### **Nilai Kelayakan Komparatif (Vektor S)**")
        st.markdown("Rumus perkalian matriks terhadap pangkat bobot kriteria baru: $S_i = \prod_{j=1}^{n} X_{ij}^{w_j}$")
        st.dataframe(df_wp_result[["Model", "Vektor_S"]], use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        df_ranking = df_wp_result.sort_values(by="Vektor_V", ascending=False).reset_index(drop=True)
        df_ranking.index = df_ranking.index + 1

        #st.success("Hasil Rekomendasi Peringkat Laptop: ")

        kolom_tampilan_akhir = ["Model", "RAM", "Storage", "Price_USD", "multiScore", "3DMark", "Vektor_V"]
        #st.dataframe(df_ranking[kolom_tampilan_akhir])
        st.session_state["df_rankking"] = df_ranking

        st.markdown("### 🏆 Hasil Akhir Rekomendasi Laptop Terbaik")
        st.write("Daftar alternatif laptop yang telah diurutkan berdasarkan nilai preferensi tertinggi (Vektor V):")
        
        # Box Highlight Juara Peringkat 1
        laptop_juara = df_ranking.iloc[0]
        st.info(
            f"🎯 **Rekomendasi Utama:** Berdasarkan pembobotan yang kamu atur, laptop terbaik jatuh kepada "
            f"**{laptop_juara['Model']}** dengan skor preferensi akhir tertinggi yaitu **{laptop_juara['Vektor_V']:.4f}**."
        )

        kolom_tampilan_akhir = ["Model", "RAM", "Storage", "Price_USD", "multiScore", "3DMark", "Vektor_V"]
        st.dataframe(df_ranking[kolom_tampilan_akhir], use_container_width=True)

if page == "Visualisasi":
    st.title("📊 Visualisasi Hasil Rekomendasi")
    
    # Cek apakah data pendukung dari page CPU & GPU sudah siap di session_state
    if "df_rawlaptop" in st.session_state and "df_fixlaptopcpu" in st.session_state and "df_fixlaptopgpu" in st.session_state:
        df_claptop = st.session_state["df_rawlaptop"]
        df_fixlaptopcpu = st.session_state["df_fixlaptopcpu"]
        df_fixlaptopgpu = st.session_state["df_fixlaptopgpu"]

        # 1. Proses kalkulasi ulang WP secara background agar grafik selalu sinkron dengan slider
        df_step1 = pd.merge(df_claptop, df_fixlaptopcpu, on="Model", how="left")
        df_stepfinal = pd.merge(df_step1, df_fixlaptopgpu, on="Model", how="left")
        df_final = df_stepfinal.dropna()
        df_datafinal = df_final.drop(columns=["Brand", "CPU_x", "GPU_x", "CPU_Clean", "GPU_Clean", "CPU_y", "GPU_y"])

        # Konversi tipe data
        df_datafinal["Storage"] = df_datafinal["Storage"].apply(konversi_storage)
        df_datafinal["RAM"] = df_datafinal["RAM"].apply(konversi_ram)
        df_datafinal["Price_USD"] = df_datafinal["Price_USD"].apply(konversi_Price)

        # Hitung Bobot & Vektor S-V
        bobot_awal = np.array([bobot_cpu, bobot_gpu, bobot_ram, bobot_storage, bobot_harga])
        k = np.array([1, 1, 1, 1, -1])

        total_bobot_awal = np.sum(bobot_awal)
        norm_bobot = bobot_awal / total_bobot_awal

        kolom_kriteria = ["multiScore", "3DMark", "RAM", "Storage", "Price_USD"]
        matrix_x = df_datafinal[kolom_kriteria].to_numpy()
        
        vektor_s = np.prod((matrix_x + 1e-9) ** (k * norm_bobot), axis=1)
        vektor_v = vektor_s / np.sum(vektor_s)

        df_wp_result = df_datafinal.copy()
        df_wp_result["Vektor_V"] = vektor_v

        # Membuat DataFrame Ranking
        df_ranking = df_wp_result.sort_values(by="Vektor_V", ascending=False).reset_index(drop=True)
        df_ranking.index = df_ranking.index + 1
        
        # 2. Mulai Tampilan Grafik & Data Top 10
        df_top = df_ranking.head(10)
        
        # Bagian Atas: Tabel Detail Top 10
        st.subheader("📋 Detail Top 10")
        st.write("Laptop dengan nilai preferensi tertinggi berdasarkan bobot kriteria saat ini.")
        st.dataframe(df_top[["Model", "Vektor_V"]], use_container_width=True)

        st.markdown("---") # Garis pembatas visual agar rapi

        # Bagian Bawah: Grafik Perbandingan
        st.subheader("📊 Grafik Perbandingan Vektor V")
        
        fig, ax = plt.subplots(figsize=(12, 6)) # Lebar dinaikkan ke 12 agar grafik memanfaatkan ruang horizontal
        
        models = df_top["Model"].values
        scores = df_top["Vektor_V"].values
        y_pos = np.arange(len(models))
        
        colors = plt.cm.viridis(np.linspace(0.8, 0.3, len(models)))
        bars = ax.barh(y_pos, scores, align='center', color=colors, edgecolor='white', linewidth=0.5)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(models, fontsize=10)
        ax.invert_yaxis()  
        ax.set_xlabel('Skor Preferensi (Vektor V)')
        ax.set_title('Top 10 Laptop Terbaik (Metode WP)', fontsize=14, fontweight='bold', pad=20)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.0002, bar.get_y() + bar.get_height()/2, 
                    f'{width:.4f}', va='center', fontsize=10, fontweight='bold', color='#2E86C1')

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True) # Grafik akan otomatis melebar memenuhi layar

        st.markdown("___")

        laptop_terbaik = df_ranking.iloc[0] # Mengambil baris pertama (Peringkat 1)
        
        st.subheader(f"🎯 Analisis Kriteria Rekomendasi Teratas: **{laptop_terbaik['Model']}**")
        st.write("Persentase nilai setiap kriteria (Skala 0-100%). Semakin tinggi/bagus nilainya, warna bar akan semakin **Hijau**.")

        # Proses Normalisasi ke 0-100% menggunakan NumPy berdasarkan nilai Min-Max dataset
        kriteria_label = ["CPU (multiScore)", "GPU (3DMark)", "RAM", "Storage", "Harga (Price_USD)"]
        persentase_kriteria = []

        # 1. CPU (Benefit)
        val_cpu = laptop_terbaik["multiScore"]
        min_cpu, max_cpu = df_ranking["multiScore"].min(), df_ranking["multiScore"].max()
        pct_cpu = ((val_cpu - min_cpu) / (max_cpu - min_cpu + 1e-9)) * 100
        persentase_kriteria.append(pct_cpu)

        # 2. GPU (Benefit)
        val_gpu = laptop_terbaik["3DMark"]
        min_gpu, max_gpu = df_ranking["3DMark"].min(), df_ranking["3DMark"].max()
        pct_gpu = ((val_gpu - min_gpu) / (max_gpu - min_gpu + 1e-9)) * 100
        persentase_kriteria.append(pct_gpu)

        # 3. RAM (Benefit)
        val_ram = laptop_terbaik["RAM"]
        min_ram, max_ram = df_ranking["RAM"].min(), df_ranking["RAM"].max()
        pct_ram = ((val_ram - min_ram) / (max_ram - min_ram + 1e-9)) * 100
        persentase_kriteria.append(pct_ram)

        # 4. Storage (Benefit)
        val_st = laptop_terbaik["Storage"]
        min_st, max_st = df_ranking["Storage"].min(), df_ranking["Storage"].max()
        pct_st = ((val_st - min_st) / (max_st - min_st + 1e-9)) * 100
        persentase_kriteria.append(pct_st)

        # 5. Harga (Cost -> Rumus dibalik: semakin kecil harga, persentase semakin tinggi/bagus)
        val_pr = laptop_terbaik["Price_USD"]
        min_pr, max_pr = df_ranking["Price_USD"].min(), df_ranking["Price_USD"].max()
        pct_pr = ((max_pr - val_pr) / (max_pr - min_pr + 1e-9)) * 100
        persentase_kriteria.append(pct_pr)

        # Buat Plot Matplotlib baru untuk kriteria
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        y_pos_kriteria = np.arange(len(kriteria_label))

        # Logika Warna Dinamis: Menggunakan colormap 'RdYlGn' (Red-Yellow-Green)
        # Nilai persentase dibagi 100 agar berada di range 0.0 - 1.0 untuk matplotlib
        colors_kriteria = plt.cm.RdYlGn([p / 100.0 for p in persentase_kriteria])

        bars2 = ax2.barh(y_pos_kriteria, persentase_kriteria, align='center', color=colors_kriteria, edgecolor='gray', linewidth=0.5)
        
        ax2.set_yticks(y_pos_kriteria)
        ax2.set_yticklabels(kriteria_label, fontsize=11, fontweight='bold')
        ax2.invert_yaxis()  
        ax2.set_xlabel('Persentase Kualitas Kriteria (%)', fontsize=11)
        ax2.set_xlim(0, 115) # Beri ruang di kanan untuk label teks

        # Tambahkan label teks persentase di ujung bar
        for bar in bars2:
            width = bar.get_width()
            ax2.text(width + 1.5, bar.get_y() + bar.get_height()/2, 
                    f'{width:.1f}%', va='center', fontsize=11, fontweight='bold')

        ax2.spines['right'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)

        # GRAFIK KOMPARASI TOP 3 LAPTOP
        st.markdown("___")
        st.subheader("🥉 Komparasi Kriteria Top 3 Laptop Terbaik")
        st.write("Grafik batang berkelompok (Grouped Bar Chart) di bawah ini membandingkan kekuatan masing-masing kriteria dari 3 laptop dengan peringkat tertinggi. Nilai disajikan dalam persentase (0-100%).")

        # Ambil 3 data teratas
        df_top3 = df_ranking.head(3)
        
        # Label sumbu X untuk kriteria yang lebih ringkas
        kriteria_label_top3 = ["CPU", "GPU", "RAM", "Storage", "Harga"]
        
        x = np.arange(len(kriteria_label_top3))
        width = 0.25 # Lebar masing-masing bar
        
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        
        # Palet warna untuk membedakan ke-3 laptop (Biru, Hijau, Oranye)
        colors_top3 = ['#2E86C1', '#28B463', '#E67E22'] 

        for i, (index, row) in enumerate(df_top3.iterrows()):
            # Normalisasi data ke skala 0-100% menggunakan min-max sebelumnya
            pct_cpu = ((row["multiScore"] - min_cpu) / (max_cpu - min_cpu + 1e-9)) * 100
            pct_gpu = ((row["3DMark"] - min_gpu) / (max_gpu - min_gpu + 1e-9)) * 100
            pct_ram = ((row["RAM"] - min_ram) / (max_ram - min_ram + 1e-9)) * 100
            pct_st = ((row["Storage"] - min_st) / (max_st - min_st + 1e-9)) * 100
            # Rumus harga dibalik karena sifatnya Cost
            pct_pr = ((max_pr - row["Price_USD"]) / (max_pr - min_pr + 1e-9)) * 100
            
            scores = [pct_cpu, pct_gpu, pct_ram, pct_st, pct_pr]
            
            # Posisi x disesuaikan agar bar berjejer rapi
            pos = x - width + (i * width)
            
            bars3 = ax3.bar(pos, scores, width, label=row['Model'], color=colors_top3[i], edgecolor='white', linewidth=1)
            
            # Menambahkan nilai persentase di atas setiap bar
            for bar in bars3:
                yval = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2, yval + 1.5, f'{yval:.0f}%', 
                         ha='center', va='bottom', fontsize=9, fontweight='bold', color='#4d4d4d')

        # Formatting tampilan grafik
        ax3.set_ylabel('Kualitas Relatif Kriteria (%)', fontsize=11)
        ax3.set_xticks(x)
        ax3.set_xticklabels(kriteria_label_top3, fontsize=12, fontweight='bold')
        ax3.set_ylim(0, 115) # Memberi ruang agar teks di atas bar tidak terpotong
        
        # Memposisikan legenda di atas grafik
        ax3.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, frameon=False, fontsize=11)
        
        # Membersihkan garis tepi dan menambahkan grid
        ax3.spines['right'].set_visible(False)
        ax3.spines['top'].set_visible(False)
        ax3.spines['left'].set_visible(False)
        ax3.grid(axis='y', linestyle='--', alpha=0.4)

        plt.tight_layout()
        st.pyplot(fig3, use_container_width=True)
            
    else:
        st.warning("Silakan buka halaman 'Data RAW', 'Data CPU', dan 'Data GPU' terlebih dahulu untuk memuat dataset ke memori aplikasi.")
