import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="pemilihan laptop - WP", layout="wide")

st.title("💻 Sistem Pendukung Keputusan Pemilihan Laptop")
st.markdown("Aplikasi ini menggunakan **Metode Weighted Product (WP)** untuk merekomendasikan laptop terbaik berdasarkan kriteria.")

#sidebar
with st.sidebar:
    st.header("Pengaturan Bobot Kiteria")
    st.markdown("Atur bobot dengan skala 1-5")
    st.markdown("1: Sangat Tidak Penting  \n2: Tidak Penting  \n3: Cukup Penting  \n4: Penting  \n5: Sangat Penting")

#.slider
    bobot_cpu = st.slider("Bobot CPU (Benefit)", 1, 5, 3)
    bobot_gpu = st.slider("Bobot GPU (Benefit)", 1, 5, 3)
    bobot_ram = st.slider("Bobot RAM (Benefit)", 1, 5, 3)
    bobot_layar = st.slider("Bobot Layar (Benefit)", 1, 5, 3)
    bobot_harga = st.slider("Bobot Harga (Benefit)", 1, 5, 3)


#table alternatif
st.write("Data Alternatif Laptop")
df_laptop = pd.read_csv('dataset/laptop.csv')
df_claptop = df_laptop.drop(columns=["Laptop_ID"]+["Performance_Level"])
df_claptop.index = df_claptop.index + 1
st.dataframe(df_claptop)

#table CPU
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

#tablegpu
st.write("Nilai GPU (Benchmark)")
df_gpu = pd.read_csv('dataset/GPU.csv')
df_cgpu = df_gpu.drop(columns =["G2Dmark","price","gpuValue","TDP","powerPerformance","testDate","category"])
df_cgpu = df_cgpu.rename(columns={"gpuName": "GPU", "G3Dmark" : "3DMark"})
#df_laptopcpu = pd.merge(df_claptop,df_ccpu, on = "CPU")
st.dataframe(df_cgpu)
#st.dataframe(df_laptopcpu)