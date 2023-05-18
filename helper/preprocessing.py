from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import streamlit as st

def optimize_k_means(data, iteration):
  """Memilih jumlah cluster optimal

  Args:
    data : pandas dataframe -> data yang akan dicluster
    iteration : int -> mau coba berapa cluster ? 1 2 atau 3 hingga ke N
  """

  means = []
  inertia = []

  # mencoba satu per satu cluster
  for i in range(1, iteration):
    kmeans = KMeans(n_clusters=i)
    kmeans.fit(data)

    means.append(i)
    inertia.append(kmeans.inertia_)

  # menampilkan hasil percobaan
  fig = plt.subplots(figsize=(10, 5))
  plt.plot(means, inertia, "o-")
  plt.grid(True)
  st.pyplot(plt)


def string_to_num(text) -> int:
  """Memisahkan angka dari string kemudian mengembalikan angka yang telah dipisahkan

  Args:
    text: string -> text yang mengandung angka
  Returns
    angka : int
  """
  # memisahkan data berdasarkan spasi kemudian pilih data di index pertama
  text = text.split()[0]

  # angka yang telah dipisahkan akan dijadikan tipe data int
  # kemudian dikirimkan ke user
  return int(text)