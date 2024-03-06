import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_date').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "cnt": "total",
    }, inplace=True)
    
    return daily_orders_df


def create_weekday_df(df):
    weekday_resampled = df.resample(rule='D', on='order_date').sum()
    weekday_df = weekday_resampled.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).round(0)

    weekday_df = weekday_df.reset_index()
    weekday_df.rename(columns={
        "cnt": "total",
    }, inplace=True)

    day_dict = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
    }
    
    weekday_df["weekday"] = weekday_df["weekday"].replace(day_dict)
    weekday_df["weekday"] = weekday_df["weekday"].astype(str)

    return weekday_df


def create_season_df(df):
    season_resampled = df.resample(rule='D', on='order_date').sum()
    season_df = season_resampled.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).round(0)

    season_df = season_df.reset_index()
    season_df.rename(columns={
        "cnt": "total",
    }, inplace=True)

    season_dict = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter",
    }
    
    season_df["season"] = season_df["season"].replace(season_dict)
    season_df["season"] = season_df["season"].astype(str)

    return season_df


def create_month_df(df):
    month_resampled = df.resample(rule='D', on='order_date').sum()
    month_df = month_resampled.groupby("mnth").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).round(0)

    month_df = month_df.reset_index()
    month_df.rename(columns={
        "cnt": "total",
    }, inplace=True)

    month_dict = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "June",
    7: "July",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
    }
    
    month_df["mnth"] = month_df["mnth"].replace(month_dict)
    month_df["mnth"] = month_df["mnth"].astype(str)

    return month_df


def create_year_df(df):
    year_resampled = df.resample(rule='D', on='order_date').sum()
    year_df = year_resampled.groupby("yr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })

    year_df = year_df.reset_index()
    year_df.rename(columns={
        "cnt": "total",
    }, inplace=True)

    year_dict = {
    0: "2011",
    1: "2012"
    }
    
    year_df["yr"] = year_df["yr"].replace(year_dict)
    year_df["yr"] = year_df["yr"].astype(str)

    return year_df


all_df = pd.read_csv("day.csv")
all_df["dteday"] = pd.to_datetime(all_df["dteday"])
all_df = all_df.rename(columns={"dteday": "order_date"})

min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://cdn-icons-png.flaticon.com/256/1785/1785274.png")
    st.markdown(
    """
    Bike Sharing Dashboard
    """
)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_date"] >= str(start_date)) & 
                (all_df["order_date"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
weekday_df = create_weekday_df(main_df)
season_df = create_season_df(main_df)
month_df = create_month_df(main_df)
year_df = create_year_df(main_df)



st.header('Bike Sharing Dashboard :sparkles: :bike: ')


st.subheader('Daily Orders')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_casual = daily_orders_df.casual.sum()
    st.metric("Total Casual Renter", value=total_casual)
 
with col2:
    total_registered = daily_orders_df.registered.sum()
    st.metric("Total Registered Renter", value=total_registered)

with col3:
    total_user = daily_orders_df.total.sum()
    st.metric("Total Renter", value=total_user)
 

fig, ax = plt.subplots(figsize=(20, 8))
ax.plot(
    daily_orders_df["order_date"],
    daily_orders_df["total"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
ax.set_title("Total Renter", loc="center", fontsize=20)

 
st.pyplot(fig)
st.write("<p style='text-align:justify;'>Interpretasi di atas tergantung dari rentang yang diinginkan, namun untuk penjelasan mengenai awal hingga akhir rentang data adalah sebagai berikut : </p>", unsafe_allow_html=True)
st.write("<p style='text-align:justify;'>Ada banyak hal yang dapat mempengaruhi performa penyewaan sepeda, namun jika kita melihat secara sudut pandang tahunan yang dimana kita melihat trending performa setiap bulan, maka hal yang paling mencolok based on data adalah pengaruh musim dan weathersit. Sisanya dijelaskan diluar data yang didapat. Trending cenderung naik dan sangat tinggi di pertengahan tahun dan turun di akhir tahun. namun di akhir tahun, trend tidak sampai jatuh dibawah awal tahun, seharusnya hal ini akan naik kembali apabila perusahaan bekerja keras dan mencari strategi yang efektif untuk mempertahankan sekaligus meningkatkan performa perusahaan bahkan jika kita lihat pada saat EDA, tahun demi tahun perusahaan dapat mengalami kenaikan performa.</p>", unsafe_allow_html=True)


st.subheader('More Details about Renter in a Day')
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(45, 8))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="casual", y="weekday", data=weekday_df.sort_values(by="casual", ascending=False), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Renter", fontsize=30)
ax[0].set_title("Casual Renter", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=23)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="registered", y="weekday", data=weekday_df.sort_values(by="registered", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Renter", fontsize=30)
ax[1].set_title("Registered Renter", loc="center", fontsize=30)
ax[1].tick_params(axis='y', labelsize=23)
ax[1].tick_params(axis='x', labelsize=30)

sns.barplot(x="total", y="weekday", data=weekday_df.sort_values(by="total", ascending=False), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Number of Renter", fontsize=30)
ax[2].set_title("Total Renter", loc="center", fontsize=30)
ax[2].tick_params(axis='y', labelsize=23)
ax[2].tick_params(axis='x', labelsize=30)

for axis in ax:
    axis.set_xticklabels(axis.get_xticklabels(), rotation=45, ha='right')

for axis in ax:
    axis.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

st.pyplot(fig)
st.write("<p style='text-align:justify;'>Interpretasi di atas tergantung dari rentang yang diinginkan, namun untuk penjelasan mengenai awal hingga akhir rentang data adalah sebagai berikut : </p>", unsafe_allow_html=True)
st.write("<p style='text-align:justify;'>Jumlah penyewa sepeda yang paling tinggi di pegang oleh hari jumat, namun apabila kita gali lebih dalam, sebenarnya untuk casual renter atau peminjam spontan / peminjam non-member, cenderung tinggi pada hari sabtu, hal ini bisa diartikan dipengaruhi oleh weekday, dan banyak orang baru atau orang yang spontan saja menyewa sepeda tanpa berlangganan karena memang mereka menyewa hanya untuk vacation, berlibur, dan tidak ada rencana untuk memperpanjang sewa. Sedangkan untuk Registered Renter atau penyewa yang sudah merupakan member dari perusahaan, cenderung rata-rata terbanyak meminjam di hari kamis, hal ini sulit saya jelaskan karena kurangnya informasi yang diberikan.</p>", unsafe_allow_html=True)


st.subheader('More Details about Renter in a Season')
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(45, 6))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="casual", y="season", data=season_df.sort_values(by="casual", ascending=False), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Renter", fontsize=30)
ax[0].set_title("Casual Renter", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=23)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="registered", y="season", data=season_df.sort_values(by="registered", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Renter", fontsize=30)
ax[1].set_title("Registered Renter", loc="center", fontsize=30)
ax[1].tick_params(axis='y', labelsize=23)
ax[1].tick_params(axis='x', labelsize=30)

sns.barplot(x="total", y="season", data=season_df.sort_values(by="total", ascending=False), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Number of Renter", fontsize=30)
ax[2].set_title("Total Renter", loc="center", fontsize=30)
ax[2].tick_params(axis='y', labelsize=23)
ax[2].tick_params(axis='x', labelsize=30)

for axis in ax:
    axis.set_xticklabels(axis.get_xticklabels(), rotation=45, ha='right')

for axis in ax:
    axis.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

st.pyplot(fig)
st.write("<p style='text-align:justify;'>Interpretasi di atas tergantung dari rentang yang diinginkan, namun untuk penjelasan mengenai awal hingga akhir rentang data adalah sebagai berikut : </p>", unsafe_allow_html=True)
st.write("<p style='text-align:justify;'>Jumlah penyewa sepeda yang paling tinggi baik untuk casual user, registered user, maupun keseluruhan dipegang oleh Fall Season. Karena kurangnya informasi, seperti latar tempat dari data yang diambil maka pendapat saya adalah karena Musim gugur identik dengan udara yang lebih segar dan bersih dibandingkan musim panas. Pada musim gugur juga memiliki udara yang sejuk dan bebas polusi membuat bersepeda lebih menyehatkan dan menyenangkan.</p>", unsafe_allow_html=True)


st.subheader('More Details about Renter in a Month')
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(45, 10))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="casual", y="mnth", data=month_df.sort_values(by="casual", ascending=False), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Renter", fontsize=30)
ax[0].set_title("Casual Renter", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=23)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="registered", y="mnth", data=month_df.sort_values(by="registered", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Renter", fontsize=30)
ax[1].set_title("Registered Renter", loc="center", fontsize=30)
ax[1].tick_params(axis='y', labelsize=23)
ax[1].tick_params(axis='x', labelsize=30)

sns.barplot(x="total", y="mnth", data=month_df.sort_values(by="total", ascending=False), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Number of Renter", fontsize=30)
ax[2].set_title("Total Renter", loc="center", fontsize=30)
ax[2].tick_params(axis='y', labelsize=23)
ax[2].tick_params(axis='x', labelsize=30)

for axis in ax:
    axis.set_xticklabels(axis.get_xticklabels(), rotation=45, ha='right')

for axis in ax:
    axis.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))


st.pyplot(fig)
st.write("<p style='text-align:justify;'>Interpretasi di atas tergantung dari rentang yang diinginkan, namun untuk penjelasan mengenai awal hingga akhir rentang data adalah sebagai berikut : </p>", unsafe_allow_html=True)
st.write("<p style='text-align:justify;'>Jumlah penyewa sepeda yang paling tinggi di pegang oleh bulan Agustus untuk keseluruhan renter dan registered renter, namun untuk casual renter yang meminjam secara spontan / peminjam non-member, mereka cenderung banyak meminjam pada bulan juli</p>", unsafe_allow_html=True)



st.subheader('More Details about Renter in a Year')
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(45, 6))
 
colors = ["#90CAF9", "#D3D3D3"]
 
sns.barplot(x="casual", y="yr", data=year_df.sort_values(by="casual", ascending=False), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Renter", fontsize=30)
ax[0].set_title("Casual Renter", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=23)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="registered", y="yr", data=year_df.sort_values(by="registered", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Renter", fontsize=30)
ax[1].set_title("Registered Renter", loc="center", fontsize=30)
ax[1].tick_params(axis='y', labelsize=23)
ax[1].tick_params(axis='x', labelsize=30)

sns.barplot(x="total", y="yr", data=year_df.sort_values(by="total", ascending=False), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Number of Renter", fontsize=30)
ax[2].set_title("Total Renter", loc="center", fontsize=30)
ax[2].tick_params(axis='y', labelsize=23)
ax[2].tick_params(axis='x', labelsize=30)

for axis in ax:
    axis.set_xticklabels(axis.get_xticklabels(), rotation=45, ha='right')

for axis in ax:
    axis.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))


st.pyplot(fig)
st.write("<p style='text-align:justify;'>Interpretasi di atas tergantung dari rentang yang diinginkan, namun untuk penjelasan mengenai awal hingga akhir rentang data adalah sebagai berikut : </p>", unsafe_allow_html=True)
st.write("<p style='text-align:justify;'>Jumlah penyewa sepeda mengalami kenaikan dari tahun 2011 ke 2012 untuk semua user </p>", unsafe_allow_html=True)



st.caption('Copyright (c) Dicoding 2024')
st.caption('Made by // mraflidwis')
st.caption('Bike Sharing Dataset : [1] Fanaee-T, Hadi, and Gama, Joao, "Event labeling combining ensemble detectors and background knowledge", Progress in Artificial Intelligence (2013): pp. 1-15, Springer Berlin Heidelberg, doi:10.1007/s13748-013-0040-3. ')

