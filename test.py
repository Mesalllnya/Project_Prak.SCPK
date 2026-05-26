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
        "Data Raw",
        "Data CPU",
        "Data GPU",
        "WP"
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
    bobot_harga = st.slider("Bobot Harga (Benefit)", 1, 5, 3)


#table alternatif
if page == "Data Raw" : 
    st.title("💻 Sistem Pendukung Keputusan Pemilihan Laptop")
    st.markdown("Aplikasi ini menggunakan **Metode Weighted Product (WP)** untuk merekomendasikan laptop terbaik berdasarkan kriteria.")

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
        
        st.write("Nilai CPU (Benchmark)")
        df_cpu = pd.read_csv('dataset/CPU.csv')
        df_cpu["CPU"] = df_cpu["manufacturer"].astype(str) + " " + df_cpu["namaCPU"].astype(str)
        df_ccpu = df_cpu.drop(columns =["manufacturer", "namaCPU", "singleScore","cores","threads","baseClock","turboClock","type"])
        kolom_baru_cpu = ["CPU","multiScore"]
        df_ccpu = df_ccpu[kolom_baru_cpu]
        #df_laptopcpu = pd.merge(df_claptop,df_ccpu, on = "CPU")
        st.dataframe(df_ccpu)
        #st.dataframe(df_laptopcpu)

        #tablelaptopcpu
        st.write("Nilai Laptop dan CPU")
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
        st.dataframe(df_fixlaptopcpu)
        st.session_state["df_fixlaptopcpu"] = df_fixlaptopcpu
    else:
        st.warning("error")

#tablegpu
if page == "Data GPU":
    if "df_rawlaptop" in st.session_state:
        df_claptop = st.session_state["df_rawlaptop"]

        st.write("Nilai GPU (3DMark)")
        df_gpu = pd.read_csv('dataset/GPU.csv')
        df_cgpu = df_gpu.drop(columns =["G2Dmark","price","gpuValue","TDP","powerPerformance","testDate","category"])
        df_cgpu = df_cgpu.rename(columns={"gpuName": "GPU", "G3Dmark" : "3DMark"})
        df_cgpu.index = df_cgpu.index + 1
        #df_laptopcpu = pd.merge(df_claptop,df_ccpu, on = "CPU")
        st.dataframe(df_cgpu)
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
        st.dataframe(df_fixlaptopgpu)
        st.session_state["df_fixlaptopgpu"] = df_fixlaptopgpu

if page == "WP" :
    if "df_rawlaptop" in st.session_state and "df_fixlaptopcpu" in st.session_state and "df_fixlaptopgpu" in st.session_state:
        df_claptop = st.session_state["df_rawlaptop"]
        df_fixlaptopcpu = st.session_state["df_fixlaptopcpu"]
        df_fixlaptopgpu = st.session_state["df_fixlaptopgpu"]


        #st.dataframe(df_claptop)
        #$st.dataframe(df_fixlaptopcpu)
        #st.dataframe(df_fixlaptopgpu)
#datafinal
        st.write("Data Final")
        df_step1 =  pd.merge(df_claptop,df_fixlaptopcpu, on="Model", how="left")
        df_stepfinal = pd.merge(df_step1,df_fixlaptopgpu, on="Model", how="left")
        df_final = df_stepfinal.dropna()
        df_datafinal = df_final.drop(columns=["Brand","CPU_x","GPU_x","CPU_Clean","GPU_Clean","CPU_y","GPU_y"])
        st.dataframe(df_datafinal)

#konversi semua ke float
        df_datafinal["Storage"] = df_datafinal["Storage"].apply(konversi_storage)
        df_datafinal["RAM"] = df_datafinal["RAM"].apply(konversi_ram)
        df_datafinal["Price_USD"] = df_datafinal["Price_USD"].apply(konversi_Price)
        st.dataframe(df_datafinal)
        #df_datafinal.info()

#WP method
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

        df_ranking = df_wp_result.sort_values(by="Vektor_V", ascending=False).reset_index(drop=True)
        df_ranking.index = df_ranking.index + 1

        st.success("Hasil Rekomendasi Peringkat Laptop: ")

        kolom_tampilan_akhir = ["Model", "RAM", "Storage", "Price_USD", "multiScore", "3DMark", "Vektor_V"]
        st.dataframe(df_ranking[kolom_tampilan_akhir])



