import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    return df

# Visualisasi data untuk mengetahui persebaran kawasan dari pembeli
def plot_customer_state(df):
    country = df['customer_state'].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=country.index, y=country.values, ax=ax)
    ax.set_title("Pembeli dari Tiap Kawasan")
    ax.set_xlabel("State")
    ax.set_ylabel("Count")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Visualisasi scatter plot dengan garis korelasi
def plot_delivery_time_vs_review_score(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='delivery_time', y='review_score', data=df, scatter_kws={'s':5}, line_kws={'color':'red'}, ax=ax)
    ax.set_title('Scatter Plot antara Waktu Pengiriman dan Review Score')
    ax.set_xlabel('Waktu Pengiriman')
    ax.set_ylabel('Review Score')
    ax.set_ylim(0, 5)
    st.pyplot(fig)

# Visualisasi data untuk mengetahui jumlah customer yang melakukan pembayaran secara angsuran
def plot_credit_installments(df):
    credit = df[df['payment_type'] == 'credit_card'] # Membuat dataset dimana tipe pembayaran = kartu kredit
    new = credit.query('payment_installments >= 1') # Membuat dataset dimana angsuran >= 1
    credit_count = new['payment_installments'].value_counts()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=credit_count.index, y=credit_count.values, ax=ax)
    ax.set_title("Angsuran Customer")
    ax.set_xlabel("Payment Installment")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# Main function
def main():
    st.title("Dashboard Proyek Analisis Data")
    
    # Load data
    df = load_data()
    
    # Pilihan filter
    options = ['Persebaran Pembeli', 'Waktu Pengiriman vs Review Score', 'Angsuran Customer']
    choice = st.sidebar.selectbox("Pilih Visualisasi", options)
    
    # Filter for order status
    order_status_options = df['order_status'].unique()
    selected_order_status = st.sidebar.multiselect('Filter by Order Status', order_status_options, default=order_status_options)

    # Filter the dataframe based on selected order status
    filtered_df = df[df['order_status'].isin(selected_order_status)]
    
    # Menampilkan visualisasi berdasarkan pilihan filter
    if choice == 'Persebaran Pembeli':
        plot_customer_state(filtered_df)
    elif choice == 'Waktu Pengiriman vs Review Score':
        plot_delivery_time_vs_review_score(filtered_df)
    elif choice == 'Angsuran Customer':
        plot_credit_installments(filtered_df)

# Panggil fungsi utama
if __name__ == '__main__':
    main()
