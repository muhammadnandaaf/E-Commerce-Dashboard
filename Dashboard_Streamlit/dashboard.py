import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from babel.numbers import format_currency

from func_dashboard import DataExploration, MapExploration

sns.set(style='dark')

datetime= ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]

# Dataset 
all_df = pd.read_csv("Dashboard_Streamlit/all_datasets.csv")

# All Geo Dataset
geo_df = pd.read_csv("Data/E-Commerce Public Dataset/geolocation_dataset.csv")

for col in datetime:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Title
    st.title("M. Nandaarjuna F.")

    # Logo Image
    st.image("Dashboard_Streamlit//date_img.jpg")

    # Date Range
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

# Ambil Fungsi dari Class func_dashboard
func = DataExploration(main_df)
map_plot = MapExploration(geo_df, plt, mpimg, urllib, st)

daily_orders_df = func.create_daily_orders_df()
trending_orders_df = func.create_trending_orders_df()
review_score_df = func.review_score_df()
most_sold_df = func.most_sold_df()
least_sold_df = func.least_sold_df()
payments_method_df = func.payments_method_df()

# Title
st.header("E-Commerce Dashboard 🛒: \n Dicoding Submission Data Analis 📊")

# Daily Orders  
st.subheader("Daily Orders")

col1, col2 = st.columns(2)

with col1:
    total_order = daily_orders_df["order_count"].sum()
    st.markdown(f"Total Order: **{total_order}**")

with col2:
    total_revenue = format_currency(daily_orders_df["revenue"].sum(), "USD", locale="en_US")
    st.markdown(f"Total Revenue: **{total_revenue}**")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Trending Orders Yearly 
st.subheader("Trending Orders")

col1,col2 = st.columns(2)
with col1:
    avg_order = trending_orders_df["order_count"].mean()
    st.markdown(f"Average Order: **{avg_order:.2f}**")

with col2:
    max_order = trending_orders_df["order_count"].max()
    st.markdown(f"Highest Order: **{max_order:.2f}**")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    trending_orders_df["order_approved_at"],
    trending_orders_df["order_count"],
    marker='o', 
    linewidth=2
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Review Score
st.subheader("Review Score")
col1,col2 = st.columns(2)

with col1:
    avg_review_score = review_score_df["review_score"].mean()
    st.markdown(f"Average Review Score: **{avg_review_score:.2f}**")

with col2:
    most_review_score = review_score_df["review_score"].max()
    st.markdown(f"Most Review Score: **{most_review_score}**")

max_score = review_score_df["review_score"].max()
min_score = review_score_df["review_score"].min()

default_color = "#2196F3"
review_score_df["color"] = review_score_df["review_score"].apply(lambda x:
    "#4CAF50" if x == max_score else  # Hijau untuk rating tertinggi
    "#2196F3"  # Biru untuk lainnya
)

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="review_score", 
    y="customer_id",
    data=review_score_df.sort_values(by="review_score", ascending=True),
    palette=review_score_df["color"].tolist(),  # Convert ke list warna
    ax=ax
)
ax.set_title("Rating Review Score", loc="center", fontsize=30)
ax.set_ylabel("Jumlah Customer")
ax.set_xlabel("Rating Score")
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=25)
st.pyplot(fig)

# Most & Least Sold
st.subheader("Produk dengan Penjualan Tertinggi dan Terendah")
 
col1, col2 = st.columns(2)
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

with col1: # Menampilkan data jumlah barang paling banyak terjual
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="product_category_name_english", 
        x="total_sold",
        data=most_sold_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Most Sold", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2: # Menampilkan data jumlah barang paling sedikit terjual
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="product_category_name_english", 
        x="total_sold",
        data=least_sold_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Least Sold", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.invert_xaxis()
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# Payment Method
st.subheader("Distribusi Metode Pembayaran Customer")

labels = payments_method_df['payment_type']
sizes = payments_method_df['total_count']
colors = ['#72BCD4', '#D3D3D3', '#FFA07A', '#FFD700']

fig, ax = plt.subplots(figsize=(20, 10))

ax.pie(sizes, 
       labels=labels, 
       autopct='%1.1f%%', 
       colors=colors, 
       shadow=False, 
       startangle=140)
st.pyplot(fig)

# Distribusi Geolocation

st.subheader("Distribusi Geolokasi Pelanggan di Brasil")

map_plot.plot()
with st.expander("See Explanation"):
        st.write('Distribusi pelanggan menunjukkan konsentrasi tinggi di Wilayah Tenggara dan Selatan Brasil, yang merupakan pusat ekonomi dan populasi terbesar dengan infrastruktur yang lebih berkembang. Sebaliknya, distribusi pelanggan menurun di Wilayah Utara dan Tengah, kemungkinan dipengaruhi oleh faktor geografis seperti hutan hujan Amazon dan populasi yang lebih jarang. Selain itu, kepadatan pelanggan sejalan dengan populasi kota, menandakan bahwa layanan atau produk dalam dataset ini lebih banyak digunakan di daerah perkotaan dibandingkan dengan daerah pedesaan atau terpencil.).')

st.caption('Copyright (C) Muhammad Nandaarjuna F. 2025')