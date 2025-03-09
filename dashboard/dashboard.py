# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import streamlit as st
# from babel.numbers import format_currency
# sns.set(style='dark')

# def create_daily_orders_df(df):
#     daily_orders_df = df.resample(rule='D', on='order_date').agg({
#         "order_id": "nunique",
#         "total_price": "sum"
#     })
#     daily_orders_df = daily_orders_df.reset_index()
#     daily_orders_df.rename(columns={
#         "order_id": "order_count",
#         "total_price": "revenue"
#     }, inplace=True)
    
#     return daily_orders_df

# def create_sum_order_items_df(df):
#     sum_order_items_df = df.groupby("product_name").quantity_x.sum().sort_values(ascending=False).reset_index()
#     return sum_order_items_df

# def create_bygender_df(df):
#     bygender_df = df.groupby(by="gender").customer_id.nunique().reset_index()
#     bygender_df.rename(columns={
#         "customer_id": "customer_count"
#     }, inplace=True)
    
#     return bygender_df

# def create_byage_df(df):
#     byage_df = df.groupby(by="age_group").customer_id.nunique().reset_index()
#     byage_df.rename(columns={
#         "customer_id": "customer_count"
#     }, inplace=True)
#     byage_df['age_group'] = pd.Categorical(byage_df['age_group'], ["Youth", "Adults", "Seniors"])
    
#     return byage_df

# def create_bystate_df(df):
#     bystate_df = df.groupby(by="state").customer_id.nunique().reset_index()
#     bystate_df.rename(columns={
#         "customer_id": "customer_count"
#     }, inplace=True)
    
#     return bystate_df

# def create_rfm_df(df):
#     rfm_df = df.groupby(by="customer_id", as_index=False).agg({
#         "order_date": "max", #mengambil tanggal order terakhir
#         "order_id": "nunique",
#         "total_price": "sum"
#     })
#     rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
#     rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
#     recent_date = df["order_date"].dt.date.max()
#     rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
#     rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
#     return rfm_df

# all_df = pd.read_csv("all_data.csv")
 
# datetime_columns = ["order_date", "delivery_date"]
# all_df.sort_values(by="order_date", inplace=True)
# all_df.reset_index(inplace=True)
 
# for column in datetime_columns:
#     all_df[column] = pd.to_datetime(all_df[column])

#     min_date = all_df["order_date"].min()
# max_date = all_df["order_date"].max()
 
# with st.sidebar:
#     # Menambahkan logo perusahaan
#     st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
#     # Mengambil start_date & end_date dari date_input
#     start_date, end_date = st.date_input(
#         label='Rentang Waktu',min_value=min_date,
#         max_value=max_date,
#         value=[min_date, max_date]
#     )

# main_df = all_df[(all_df["order_date"] >= str(start_date)) & 
#                 (all_df["order_date"] <= str(end_date))]

# daily_orders_df = create_daily_orders_df(main_df)
# sum_order_items_df = create_sum_order_items_df(main_df)
# bygender_df = create_bygender_df(main_df)
# byage_df = create_byage_df(main_df)
# bystate_df = create_bystate_df(main_df)
# rfm_df = create_rfm_df(main_df)

# st.header('Dicoding Collection Dashboard :sparkles:')

# st.subheader('Daily Orders')
 
# col1, col2 = st.columns(2)
 
# with col1:
#     total_orders = daily_orders_df.order_count.sum()
#     st.metric("Total orders", value=total_orders)
 
# with col2:
#     total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO') 
#     st.metric("Total Revenue", value=total_revenue)
 
# fig, ax = plt.subplots(figsize=(16, 8))
# ax.plot(
#     daily_orders_df["order_date"],
#     daily_orders_df["order_count"],
#     marker='o', 
#     linewidth=2,
#     color="#90CAF9"
# )
# ax.tick_params(axis='y', labelsize=20)
# ax.tick_params(axis='x', labelsize=15)
 
# st.pyplot(fig)

# st.subheader("Best & Worst Performing Product")
 
# fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
# colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
# sns.barplot(x="quantity_x", y="product_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
# ax[0].set_ylabel(None)
# ax[0].set_xlabel("Number of Sales", fontsize=30)
# ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
# ax[0].tick_params(axis='y', labelsize=35)
# ax[0].tick_params(axis='x', labelsize=30)
 
# sns.barplot(x="quantity_x", y="product_name", data=sum_order_items_df.sort_values(by="quantity_x", ascending=True).head(5), palette=colors, ax=ax[1])
# ax[1].set_ylabel(None)
# ax[1].set_xlabel("Number of Sales", fontsize=30)
# ax[1].invert_xaxis()
# ax[1].yaxis.set_label_position("right")
# ax[1].yaxis.tick_right()
# ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
# ax[1].tick_params(axis='y', labelsize=35)
# ax[1].tick_params(axis='x', labelsize=30)
 
# st.pyplot(fig)

# st.subheader("Customer Demographics")
 
# col1, col2 = st.columns(2)
 
# with col1:
#     fig, ax = plt.subplots(figsize=(20, 10))
 
#     sns.barplot(
#         y="customer_count", 
#         x="gender",
#         data=bygender_df.sort_values(by="customer_count", ascending=False),
#         palette=colors,
#         ax=ax
#     )
#     ax.set_title("Number of Customer by Gender", loc="center", fontsize=50)
#     ax.set_ylabel(None)
#     ax.set_xlabel(None)
#     ax.tick_params(axis='x', labelsize=35)
#     ax.tick_params(axis='y', labelsize=30)
#     st.pyplot(fig)
 
# with col2:
#     fig, ax = plt.subplots(figsize=(20, 10))
    
#     colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
#     sns.barplot(
#         y="customer_count", 
#         x="age_group",
#         data=byage_df.sort_values(by="age_group", ascending=False),
#         palette=colors,
#         ax=ax
#     )
#     ax.set_title("Number of Customer by Age", loc="center", fontsize=50)
#     ax.set_ylabel(None)
#     ax.set_xlabel(None)
#     ax.tick_params(axis='x', labelsize=35)
#     ax.tick_params(axis='y', labelsize=30)
#     st.pyplot(fig)
 
# fig, ax = plt.subplots(figsize=(20, 10))
# colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
# sns.barplot(
#     x="customer_count", 
#     y="state",
#     data=bystate_df.sort_values(by="customer_count", ascending=False),
#     palette=colors,
#     ax=ax
# )
# ax.set_title("Number of Customer by States", loc="center", fontsize=30)
# ax.set_ylabel(None)
# ax.set_xlabel(None)
# ax.tick_params(axis='y', labelsize=20)
# ax.tick_params(axis='x', labelsize=15)
# st.pyplot(fig)

# st.subheader("Best Customer Based on RFM Parameters")
 
# col1, col2, col3 = st.columns(3)
 
# with col1:
#     avg_recency = round(rfm_df.recency.mean(), 1)
#     st.metric("Average Recency (days)", value=avg_recency)
 
# with col2:
#     avg_frequency = round(rfm_df.frequency.mean(), 2)
#     st.metric("Average Frequency", value=avg_frequency)
 
# with col3:
#     avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
#     st.metric("Average Monetary", value=avg_frequency)
 
# fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
# colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
# sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
# ax[0].set_ylabel(None)
# ax[0].set_xlabel("customer_id", fontsize=30)
# ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
# ax[0].tick_params(axis='y', labelsize=30)
# ax[0].tick_params(axis='x', labelsize=35)
 
# sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
# ax[1].set_ylabel(None)
# ax[1].set_xlabel("customer_id", fontsize=30)
# ax[1].set_title("By Frequency", loc="center", fontsize=50)
# ax[1].tick_params(axis='y', labelsize=30)
# ax[1].tick_params(axis='x', labelsize=35)
 
# sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
# ax[2].set_ylabel(None)
# ax[2].set_xlabel("customer_id", fontsize=30)
# ax[2].set_title("By Monetary", loc="center", fontsize=50)
# ax[2].tick_params(axis='y', labelsize=30)
# ax[2].tick_params(axis='x', labelsize=35)
 
# st.pyplot(fig)
 
# st.caption('Copyright (c) Dicoding 2023')

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load Data
# @st.cache_data
# def load_data():
#     hourly_summary = pd.read_csv("hourly_summary.csv")
#     weather_day = pd.read_csv("weather_day.csv")
#     weather_hour = pd.read_csv("weather_hour.csv")
#     workingday_summary = pd.read_csv("workingday_summary.csv")
#     return hourly_summary, weather_day, weather_hour, workingday_summary

# hourly_summary, weather_day, weather_hour, workingday_summary = load_data()

# # Data Cleaning
# hourly_summary.dropna(inplace=True)
# weather_day.dropna(inplace=True)
# weather_hour.dropna(inplace=True)
# workingday_summary.dropna(inplace=True)

# # Sidebar Filter
# st.sidebar.header("Filter Options")
# hour_filter = st.sidebar.slider("Select Hour", min_value=int(hourly_summary.hour.min()), 
#                                 max_value=int(hourly_summary.hour.max()), value=int(hourly_summary.hour.min()))

# # Filtered Data
# df_filtered = hourly_summary[hourly_summary["hour"] == hour_filter]

# # Dashboard Title
# st.title("Bike Sharing Dashboard")

# # Metrics Display
# st.subheader("Summary Metrics")
# st.metric("Total Usage", df_filtered["total"].sum())

# # Visualization - Hourly Usage
# st.subheader("Hourly Bike Usage")
# fig, ax = plt.subplots(figsize=(10, 5))
# sns.lineplot(x=hourly_summary.hour, y=hourly_summary.total, marker="o", ax=ax)
# st.pyplot(fig)

# # Visualization - Weather Impact
# st.subheader("Weather Impact on Usage")
# fig, ax = plt.subplots(figsize=(10, 5))
# sns.barplot(x=weather_day.weather, y=weather_day.total, ax=ax)
# st.pyplot(fig)

# # Footer
# st.caption("Data Source: Bike Sharing Dataset")

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load data
# hour_df = pd.read_csv("hour.csv")
# weather_day_df = pd.read_csv("weather_day.csv")
# weather_hour_df = pd.read_csv("weather_hour.csv")
# workingday_df = pd.read_csv("workingday_summary.csv")

# # Tampilkan daftar kolom untuk verifikasi
# st.sidebar.write("### Kolom dalam dataset:")
# st.sidebar.write(hour_df.columns)

# # Title
# st.title("Dashboard Penyewaan Sepeda")

# # Pertanyaan 1: Pengaruh Cuaca terhadap Penyewaan Sepeda
# st.header("Pengaruh Cuaca terhadap Penyewaan Sepeda")

# if 'weathersit' in hour_df.columns:
#     weather_col = 'weathersit'  # Sesuaikan dengan nama kolom yang benar
# else:
#     st.error("Kolom 'weathersit' tidak ditemukan dalam hour.csv")
#     st.stop()

# weather_agg = hour_df.groupby(by=weather_col).agg({'cnt': ['sum', 'mean']}).reset_index()
# weather_agg.columns = ['weather', 'total_rentals', 'mean_rentals']

# fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# sns.barplot(x='weather', y='total_rentals', data=weather_agg, palette='Blues', ax=axes[0])
# axes[0].set_title('Total Penyewaan Sepeda Berdasarkan Cuaca')
# axes[0].set_xlabel('Kondisi Cuaca')
# axes[0].set_ylabel('Total Sepeda Tersewa')
# for index, value in enumerate(weather_agg['total_rentals']):
#     axes[0].text(index, value + 500, str(int(value)), ha='center', fontsize=10)

# sns.barplot(x='weather', y='mean_rentals', data=weather_agg, palette='Greens', ax=axes[1])
# axes[1].set_title('Rata-rata Penyewaan Sepeda Berdasarkan Cuaca')
# axes[1].set_xlabel('Kondisi Cuaca')
# axes[1].set_ylabel('Rata-rata Sepeda Tersewa')
# for index, value in enumerate(weather_agg['mean_rentals']):
#     axes[1].text(index, value + 4, f"{value:.2f}", ha='center', fontsize=10)

# st.pyplot(fig)

# # Pertanyaan 2: Pola Penyewaan Sepeda Sepanjang Hari
# st.header("Pola Penyewaan Sepeda Sepanjang Hari")

# if 'workingday' in hour_df.columns and 'hr' in hour_df.columns:
#     hourly_trend = hour_df.groupby(['workingday', 'hr']).agg({'cnt': 'mean'}).reset_index()
    
#     fig, ax = plt.subplots(figsize=(10, 5))
#     sns.lineplot(data=hourly_trend, x='hr', y='cnt', hue='workingday', marker='o', ax=ax)
#     ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Jam')
#     ax.set_xlabel('Jam dalam Sehari')
#     ax.set_ylabel('Rata-rata Jumlah Penyewaan')
#     ax.set_xticks(range(0, 24))
#     ax.legend(title='Hari', labels=['Hari Kerja', 'Akhir Pekan'])
#     ax.grid(True, linestyle='--', alpha=0.5)
#     st.pyplot(fig)
# else:
#     st.error("Kolom 'workingday' atau 'hr' tidak ditemukan dalam hour.csv")

# # Analisis Lanjutan menggunakan RFM
# st.header("Analisis RFM Penyewaan Sepeda")

# if 'dteday' in hour_df.columns:
#     rfm_df = hour_df.copy()
#     rfm_df['dteday'] = pd.to_datetime(rfm_df['dteday'])
#     reference_date = rfm_df['dteday'].max()
    
#     rfm = rfm_df.groupby('workingday').agg({
#         'dteday': lambda x: (reference_date - x.max()).days,
#         'hr': 'count',
#         'cnt': 'sum'
#     }).reset_index()
    
#     rfm.columns = ['Working Day (Yes/No)', 'Recency', 'Frequency', 'Monetary']
    
#     st.dataframe(rfm)
# else:
#     st.error("Kolom 'dteday' tidak ditemukan dalam hour.csv")

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