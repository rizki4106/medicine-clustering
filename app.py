from helper.preprocessing import string_to_num
from helper.preprocessing import optimize_k_means
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Clustering Produk Kesehatan")

# upload file excel
file = st.file_uploader("Upload file excel", ["xlsx", "csv"])

if file:
    data = pd.read_excel(file)
else:
    data = pd.read_excel("./data/data.xlsx")

st.markdown("## Data")

# menampilkan data ke user
st.write(data.head())

st.markdown("### Memilih Filed")
st.write("Memilih field data yang akan dipakai")

# memilih field excel
field = data[['Qty', 'Nilai']]

# menampilkan field yang akan dipilih
st.write(field.head())

st.markdown("### Memproses data")
st.markdown("Data Qty berupa data `string` dan masih tergabung antara angka dan string oleh karena itu perlu memisahkannya kemudian pilih data angka")

# memisahkan angka dari teks
field['Qty'] = field['Qty'].apply(string_to_num)

# menampilkan hasil pemrosesan
st.write(field.head())

st.markdown("### Menstandarisasi Data")
st.markdown("Data akan dibuat dari rentang `0` dan `1` supaya pemrosesan cepat dan tidak ada perbedaan data yang signifikan. Metode yang dipakai adalah `MinMaxScaller`")

# inisialisasi min max scaller
scaler = MinMaxScaler()
scaler.fit(field.values)
standarize = scaler.transform(field.values)

#
field['Qty'] = standarize[:, 0]
field['Nilai'] = standarize[:, 1]

st.write(field.head())

st.markdown("## Mencari nilai cluster optimal")
st.markdown("Untuk mencari nilai cluster yang optimal akan menggunakan teknik `elbow`")

# mencoba jumlah cluster dari 1 hingga 10
n_cluster = 10

# menemukan cluster optimal dan menampilkannya
optimize_k_means(field.values, n_cluster)

st.markdown("dari hasil diatas dapat kita ambil nilai yang membentuk siku yaitu `3`")

st.markdown("## Melakukan Clustering")
st.write("melakukan clustering dengan 3 cluster")

# inisialisasi kmeans
kmeans = KMeans(n_clusters=3)
kmeans.fit(field.values)

# menambahkan label pada data yang field nya dipilih
field['label'] = kmeans.labels_

# menampilkan hasil clustering
fig, ax = plt.subplots()
sc = ax.scatter(x=field['Qty'], y=field['Nilai'], c=field['label'])
plt.title("Cluster obat")
plt.xlabel("Qty")
plt.ylabel("Nilai")
fig.colorbar(sc)
st.pyplot(fig)

# membuat tabel keterangan
keterangan = pd.DataFrame([
    {"Label": 0, "Keterangan": "Harga rendah dan Kuantitas rendah"},
    {"Label": 1, "Keterangan": "Harga rendah dan Kuantitas tinggi"},
    {"Label": 2, "Keterangan": "Harga tinggi dan Kuantitas Rendah"}
])

st.markdown("### Keterangan hasil clustering")
st.table(keterangan)

st.markdown("# Hasil cluster berdasarkan kota")

# menambahkan label pada data
data['label'] = field['label']

# menghilangkan data yang kotanya tidak ada
# data = data.dropna(axis=0)

# memilih kota
option = st.selectbox(
    "Pilih Kota",
    tuple(data['KOTA'].unique().tolist())
)

# memilih data berdasarkan kota
data_kota = data[data['KOTA'] == option]

# menampilkan setiap label data didalam 1 kota yang telah dipilih
st.markdown("#### Data label 0")
st.write(data_kota[data_kota['label'] == 0])

st.markdown("#### Data label 1")
st.write(data_kota[data_kota['label'] == 1])

st.markdown("#### Data label 2")
st.write(data_kota[data_kota['label'] == 2])