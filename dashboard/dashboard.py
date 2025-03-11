import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
hour_df = pd.read_csv("hour.csv")
weather_day_df = pd.read_csv("weather_day.csv")
weather_hour_df = pd.read_csv("weather_hour.csv")
workingday_df = pd.read_csv("workingday_summary.csv")

# Pastikan format tanggal benar
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Sidebar untuk filter data
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", hour_df['dteday'].dt.year.unique())
selected_month = st.sidebar.selectbox("Pilih Bulan", hour_df['dteday'].dt.month.unique())

# Filter dataset berdasarkan pilihan pengguna
filtered_df = hour_df[(hour_df['dteday'].dt.year == selected_year) & (hour_df['dteday'].dt.month == selected_month)]

# Title
st.title("Dashboard Penyewaan Sepeda")

# Pertanyaan 1: Pengaruh cuaca terhadap jumlah sepeda yang disewa
st.header("Pengaruh Cuaca terhadap Penyewaan Sepeda")

weather_agg = filtered_df.groupby(by='weathersit').agg({'cnt': ['sum', 'mean']}).reset_index()
weather_agg.columns = ['weather', 'total_rentals', 'mean_rentals']

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

sns.barplot(x='weather', y='total_rentals', data=weather_agg, palette='Blues', ax=axes[0])
axes[0].set_title('Total Penyewaan Sepeda Berdasarkan Cuaca')
axes[0].set_xlabel('Kondisi Cuaca')
axes[0].set_ylabel('Total Sepeda Tersewa')
for index, value in enumerate(weather_agg['total_rentals']):
    axes[0].text(index, value + 500, str(int(value)), ha='center', fontsize=10)

sns.barplot(x='weather', y='mean_rentals', data=weather_agg, palette='Greens', ax=axes[1])
axes[1].set_title('Rata-rata Penyewaan Sepeda Berdasarkan Cuaca')
axes[1].set_xlabel('Kondisi Cuaca')
axes[1].set_ylabel('Rata-rata Sepeda Tersewa')
for index, value in enumerate(weather_agg['mean_rentals']):
    axes[1].text(index, value + 4, f"{value:.2f}", ha='center', fontsize=10)

st.pyplot(fig)

# Pertanyaan 2: Pola penyewaan sepeda sepanjang hari kerja dan akhir pekan
st.header("Pola Penyewaan Sepeda Sepanjang Hari")

hourly_trend = filtered_df.groupby(['workingday', 'hr']).agg({'cnt': 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hourly_trend, x='hr', y='cnt', hue='workingday', marker='o', ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Jam')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Jumlah Penyewaan')
ax.set_xticks(range(0, 24))
ax.legend(title='Hari', labels=['Hari Kerja', 'Akhir Pekan'])
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)

# Analisis Lanjutan menggunakan RFM
st.header("Analisis RFM Penyewaan Sepeda")

rfm_df = filtered_df.copy()
reference_date = rfm_df['dteday'].max()

rfm = rfm_df.groupby('workingday').agg({
    'dteday': lambda x: (reference_date - x.max()).days,
    'hr': 'count',
    'cnt': 'sum'
}).reset_index()

rfm.columns = ['Working Day (Yes/No)', 'Recency', 'Frequency', 'Monetary']

st.dataframe(rfm)
