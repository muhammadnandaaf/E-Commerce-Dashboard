import numpy as np
import io
from PIL import Image

class DataExploration:

    def __init__(self, df):
        self.df = df

    # Fungsi Order Per Hari
    def create_daily_orders_df(self):
        return (
            self.df.resample(rule='D', on='order_approved_at')
                .agg(order_count=('order_id', 'nunique'), 
                    revenue=('payment_value', 'sum'))
                .reset_index()
        )
    
    # Fungsi Trending Penjualan
    def create_trending_orders_df(self):
        return (
            self.df.resample(rule='M', on='order_approved_at').agg(order_count=('order_id', 'nunique')).reset_index()
        )
    
    # Fungsi Rangking Rating
    def review_score_df(self):
        review_data = self.df.groupby(['review_score']).customer_id.nunique().reset_index().sort_values(by='review_score', ascending=True)
        return (
            review_data
        )

    # Fungsi Mengambil Produk Paling Banyak Terjual
    def most_sold_df(self):
        product_sales = self.df.groupby(['product_category_name','product_category_name_english']).size().reset_index(name='total_sold')
        product_sales_sorted = product_sales.sort_values(by='total_sold', ascending=False)
        most_sold = product_sales_sorted.head()
        most_sold.reset_index(drop=True, inplace=True)
        return (
            most_sold
        )
    
    # Fungsi Mengambil Produk Paling Sedikit Terjual
    def least_sold_df(self):
        product_sales = self.df.groupby(['product_category_name','product_category_name_english']).size().reset_index(name='total_sold')
        product_sales_sorted = product_sales.sort_values(by='total_sold', ascending=False)
        least_sold = product_sales_sorted.tail()
        least_sold.reset_index(drop=True, inplace=True)
        return (
            least_sold
        )
    
    # Fungsi Metode Pembayaran
    def payments_method_df(self):
        full_products_payments = self.df.groupby(['payment_type']).size().reset_index(name='total_count').sort_values(by='total_count', ascending=False)
        return (
            full_products_payments
        )
    
# Visualisasi Geolocation
class MapExploration:
    def __init__(self, data, plt, mpimg, urllib, st):
        self.data = data
        self.plt = plt
        self.mpimg = mpimg
        self.urllib = urllib
        self.st = st

    def plot(self):
        url = 'https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'
    
        try:
            # Mengunduh dan membaca gambar dari URL
            response = self.urllib.request.urlopen(url)
            image_data = io.BytesIO(response.read())
            brazil_map = Image.open(image_data)
            brazil_map = brazil_map.convert("RGB")
        except Exception as e:
            print(f"Error loading map: {e}")
            return
        
        # Tentukan ukuran plot
        fig, ax = self.plt.subplots(figsize=(12, 12))

        # Konversi gambar ke format numpy array untuk imshow()
        brazil_map = np.array(brazil_map)

        # Plot gambar peta Brasil sebagai latar belakang
        ax.imshow(brazil_map, extent=[-73.9828, -33.8, -33.7511, 5.4], aspect='auto')

        # Scatter plot lokasi pelanggan
        ax.scatter(
            self.data['geolocation_lng'], 
            self.data['geolocation_lat'], 
            c='blue', s=10, alpha=0.5, edgecolors='w', label='Pelanggan'
        )

        # Pengaturan label dan batas koordinat
        ax.set_xlim(-73.9828, -33.8)
        ax.set_ylim(-33.7511, 5.4)
        ax.set_xlabel("Longitude", fontsize=12)
        ax.set_ylabel("Latitude", fontsize=12)
        ax.set_title("Distribusi Pelanggan di Brasil", fontsize=14, fontweight='bold')

        # Menambahkan grid untuk referensi
        ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

        # Menambahkan legenda
        ax.legend()

        self.st.pyplot(fig)

