import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt



# Load dataset
kekerasansmi = pd.read_excel('kekerasansmi.xlsx')
kekerasankej = pd.read_excel('kekerasankej.xlsx')

# Judul aplikasi
st.title('Analisis Tingkat Kekerasan Berdasarkan Tempat Kejadian, Pendidikan & Jenis Kelamin di Provinsi Jawa Barat Tahun 2018 - 2022')

kekerasansmi['kategori_pendidikan'] = kekerasansmi['kategori_pendidikan'].fillna('TIDAK DIKETAHUI')
kekerasansmi['kategori_pendidikan'] = kekerasansmi['kategori_pendidikan'].replace('TIDAK \nSEKOLAH', 'TIDAK SEKOLAH')
kekerasansmi['kategori_pendidikan'] = kekerasansmi['kategori_pendidikan'].replace('PERGURUAN \nTINGGI', 'PERGURUAN TINGGI')

# Create Streamlit app
st.header('Perubahan Jumlah Kekerasan dari Tahun ke Tahun Berdasarkan Jenis Kelamin dan Tingkat Pendidikan')

# Get the available years
tahun_min = int(kekerasansmi['tahun'].min())
tahun_max = int(kekerasansmi['tahun'].max())

# Range slider for selecting years
tahun_awal, tahun_akhir = st.slider('Pilih Rentang Tahun', tahun_min, tahun_max, (tahun_min, tahun_max))

# Filter the data based on selected years
filtered_data = kekerasansmi[(kekerasansmi['tahun'] >= tahun_awal) & (kekerasansmi['tahun'] <= tahun_akhir)]

# Calculate the total jumlah kekerasan per tahun
jumlah_kekerasan_per_tahun = filtered_data.groupby('tahun')['jumlah'].sum()

# Line plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=jumlah_kekerasan_per_tahun.index, y=jumlah_kekerasan_per_tahun.values, ax=ax)
ax.set_xlabel('Tahun')
ax.set_ylabel('Jumlah Kekerasan')
ax.set_title('Perubahan Jumlah Kekerasan dari Tahun ke Tahun')
ax.grid(True)

# Display the plot
st.pyplot(fig)

# Calculate the total jumlah kekerasan per kategori pendidikan
total_kekerasan_per_pendidikan = kekerasansmi.groupby('kategori_pendidikan')['jumlah'].sum()

# Display the total jumlah kekerasan per kategori pendidikan
st.subheader('Total Jumlah Kekerasan per Kategori Pendidikan:')
st.write(total_kekerasan_per_pendidikan)




# Create Streamlit app
st.header('Jumlah Kekerasan Keseluruhan berdasarkan Kategori Pendidikan')


# Pilihan Kategori Pendidikan
kategori_pendidikan = st.selectbox('Pilih Kategori Pendidikan', ['Semua'] + list(kekerasansmi['kategori_pendidikan'].unique()))

# Pilihan Tahun
tahun = st.selectbox('Pilih Tahun', ['Semua'] + list(kekerasansmi['tahun'].unique()))

# Filter data berdasarkan kategori pendidikan dan tahun yang dipilih
filtered_data = kekerasansmi.copy()
if kategori_pendidikan != 'Semua':
    filtered_data = filtered_data[filtered_data['kategori_pendidikan'] == kategori_pendidikan]
if tahun != 'Semua':
    filtered_data = filtered_data[filtered_data['tahun'] == tahun]

# Hitung jumlah kekerasan keseluruhan
jumlah_kekerasan = filtered_data['jumlah'].sum()

# Group data berdasarkan kategori pendidikan dan tahun, dan hitung jumlah kekerasan
grouped_data = filtered_data.groupby(['kategori_pendidikan', 'tahun'])['jumlah'].sum().reset_index()

# Bar plot
fig, ax = plt.subplots(figsize=(15, 6))
sns.barplot(x='kategori_pendidikan', y='jumlah', hue='tahun', data=grouped_data, ax=ax)
ax.set_xlabel('Kategori Pendidikan')
ax.set_ylabel('Jumlah Kekerasan')

# Judul plot
if kategori_pendidikan != 'Semua' and tahun != 'Semua':
    ax.set_title('Jumlah Kekerasan\nKategori Pendidikan:\n{} | Tahun: {}'.format(kategori_pendidikan, tahun))
elif kategori_pendidikan != 'Semua':
    ax.set_title('Jumlah Kekerasan\nKategori Pendidikan:\n{}'.format(kategori_pendidikan))
elif tahun != 'Semua':
    ax.set_title('Jumlah Kekerasan\nTahun: {}'.format(tahun))
else:
    ax.set_title('Jumlah Kekerasan Keseluruhan')

# Display the plot in Streamlit
st.pyplot(fig)

# Display total jumlah kekerasan
st.write('Total Jumlah Kekerasan: {}'.format(jumlah_kekerasan))


# Create Streamlit app
st.header('Perbandingan Jumlah Kekerasan Berdasarkan Jenis Kelamin')

# Filter options
tahun_options = ['Semua'] + kekerasansmi['tahun'].unique().tolist()

# Widget inputs
tahun = st.selectbox('Pilih Tahun', tahun_options, key='tahun_selectbox')

# Filter data
filtered_data = kekerasansmi.copy()
if tahun != 'Semua':
    filtered_data = filtered_data[filtered_data['tahun'] == tahun]

# Calculate total incidents per gender
total_kekerasan_per_jenis_kelamin = filtered_data.groupby('jenis_kelamin')['jumlah'].sum()

# Pie chart
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(total_kekerasan_per_jenis_kelamin, labels=total_kekerasan_per_jenis_kelamin.index, autopct='%1.1f%%')
ax.set_title('Perbandingan Jumlah Kekerasan Berdasarkan Jenis Kelamin')

# Display the plot in Streamlit
st.pyplot(fig)

# Total jumlah kekerasan
total_kekerasan = filtered_data['jumlah'].sum()

# Display total jumlah kekerasan
st.subheader('Total Jumlah Kekerasan:')
st.write(total_kekerasan)

# Create Streamlit app
st.header('Analisis Jenis Kelamin Kekerasan per Tahun')

# Filter options
tahun_options = ['Semua'] + kekerasansmi['tahun'].unique().tolist()
tahun = st.selectbox('Pilih Tahun', tahun_options, key='select_tahun')

# Filter data
filtered_data = kekerasansmi.copy()
if tahun != 'Semua':
    filtered_data = filtered_data[filtered_data['tahun'] == tahun]

# Group data by jenis kelamin and tahun, then sum the jumlah kekerasan
jenis_kelamin = filtered_data.groupby(['jenis_kelamin', 'tahun'])['jumlah'].sum().unstack()

# Plot heatmap
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(jenis_kelamin, cmap='Blues', annot=True, fmt='g', ax=ax)
ax.set_xlabel('Tahun')
ax.set_ylabel('Jenis Kelamin')
ax.set_title('Analisis Jenis Kelamin Kekerasan per Tahun')

# Display the plot in Streamlit
st.pyplot(fig)

# Total jumlah kekerasan
total_kekerasan = filtered_data['jumlah'].sum()

# Display total jumlah kekerasan
st.subheader('Total Jumlah Kekerasan:')
st.write(total_kekerasan)

# Create Streamlit app
st.header('Analisis Kategori Pendidikan Terhadap Kekerasan per Tahun')

# Sidebar - Pilihan Tahun
tahun_options = ['Semua'] + list(kekerasansmi['tahun'].unique())
tahun = st.selectbox('Pilih Tahun', tahun_options, key='tahun_select')

# Filter data berdasarkan tahun yang dipilih
filtered_data = kekerasansmi.copy()
if tahun != 'Semua':
    filtered_data = filtered_data[filtered_data['tahun'] == tahun]

# Group data berdasarkan Kategori Pendidikan dan tahun, dan hitung jumlah kekerasan
kategori_pendidikan = filtered_data.groupby(['kategori_pendidikan', 'tahun'])['jumlah'].sum().unstack()

# Heatmap plot
plt.figure(figsize=(10, 6))
sns.heatmap(kategori_pendidikan, cmap='Blues', annot=True, fmt='g')
plt.xlabel('Tahun')
plt.ylabel('Kategori Pendidikan')
plt.title('Analisis Kategori Pendidikan Terhadap Kekerasan per Tahun')

# Display the plot in Streamlit
st.pyplot(plt)


# Create Streamlit app
st.header('Jumlah Kekerasan Keseluruhan berdasarkan Tempat Kejadian')

# Get the available years
tahun_min2 = int(kekerasankej['tahun'].min())
tahun_max2 = int(kekerasankej['tahun'].max())

# Range slider for selecting years
tahun_awal2, tahun_akhir2 = st.slider('Pilih Rentang Tahun', tahun_min2, tahun_max2, (tahun_min2, tahun_max2), key='rentang_tahun')

# Filter the data based on selected years
filtered_data2 = kekerasankej[(kekerasankej['tahun'] >= tahun_awal2) & (kekerasankej['tahun'] <= tahun_akhir2)]

# Calculate the total jumlah kekerasan per tahun
jumlah_kekerasan_per_tahun2 = filtered_data2.groupby('tahun')['jumlah_kekerasan'].sum()

# Line plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=jumlah_kekerasan_per_tahun2.index, y=jumlah_kekerasan_per_tahun2.values, ax=ax)
ax.set_xlabel('Tahun')
ax.set_ylabel('Jumlah Kekerasan')
ax.set_title('Perubahan Jumlah Kekerasan dari Tahun ke Tahun')
ax.grid(True)

# Display the plot
st.pyplot(fig)

# Create Streamlit app
st.header('Jumlah Kekerasan Keseluruhan berdasarkan Tempat Kejadian')

# Pilihan Tempat Kejadian
tempat_kejadian = st.selectbox('Pilih Tempat Kejadian', ['Semua'] + list(kekerasankej['tempat_kejadian'].unique()), key='tempat_kejadian')

# Pilihan Tahun
tahun = st.selectbox('Pilih Tahun', ['Semua'] + list(kekerasankej['tahun'].unique()), key='tahun')

# Filter data berdasarkan tempat kejadian dan tahun yang dipilih
filtered_data = kekerasankej.copy()
if tempat_kejadian != 'Semua':
    filtered_data = filtered_data[filtered_data['tempat_kejadian'] == tempat_kejadian]
if tahun != 'Semua':
    filtered_data = filtered_data[filtered_data['tahun'] == tahun]

# Hitung jumlah kekerasan keseluruhan
jumlah_kekerasan = filtered_data['jumlah_kekerasan'].sum()

# Group data berdasarkan tempat kejadian dan tahun, dan hitung jumlah kekerasan
grouped_data = filtered_data.groupby(['tempat_kejadian', 'tahun'])['jumlah_kekerasan'].sum().reset_index()

# Bar plot
fig, ax = plt.subplots(figsize=(15, 6))
sns.barplot(x='tempat_kejadian', y='jumlah_kekerasan', hue='tahun', data=grouped_data, ax=ax)
ax.set_xlabel('Tempat Kejadian')
ax.set_ylabel('Jumlah Kekerasan')

# Judul plot
if tempat_kejadian != 'Semua' and tahun != 'Semua':
    ax.set_title('Jumlah Kekerasan\nTempat Kejadian:\n{} | Tahun: {}'.format(tempat_kejadian, tahun))
elif tempat_kejadian != 'Semua':
    ax.set_title('Jumlah Kekerasan\nTempat Kejadian:\n{}'.format(tempat_kejadian))
elif tahun != 'Semua':
    ax.set_title('Jumlah Kekerasan\nTahun: {}'.format(tahun))
else:
    ax.set_title('Jumlah Kekerasan Keseluruhan')

# Display the plot in Streamlit
st.title('Jumlah Kekerasan Keseluruhan berdasarkan Tempat Kejadian')
st.pyplot(fig)


st.header('TOP 3 Tingkat Kekerasan per Kota/Kabupaten')

# Mengurutkan data berdasarkan jumlah kekerasan secara descending
top_kota = kekerasansmi.groupby('nama_kabupaten_kota')['jumlah'].sum().nlargest(3).reset_index()

# Pilihan Tahun
tahun_key = 0
tahun = st.selectbox('Pilih Tahun', ['Semua'] + list(kekerasansmi['tahun'].unique()), key=f'tahun_select_{tahun_key}')

# Filter data berdasarkan tahun yang dipilih
filtered_data = kekerasansmi.copy()
if tahun != 'Semua':
    filtered_data = filtered_data[filtered_data['tahun'] == tahun]

# Mengurutkan data berdasarkan jumlah kekerasan secara descending setelah di-filter
top_kota_filtered = filtered_data.groupby('nama_kabupaten_kota')['jumlah'].sum().nlargest(3).reset_index()

# Membuat layout dengan 2 kolom
col1, col2 = st.columns(2)

# Plot bar plot 3 kabupaten/kota terbanyak kekerasan (semua tahun) - Plot 1
with col1:
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='nama_kabupaten_kota', y='jumlah', data=top_kota)
    ax1.set_xlabel('Kabupaten/Kota')
    ax1.set_ylabel('Jumlah Kekerasan')
    ax1.set_title('3 Kabupaten/Kota dengan Jumlah Kekerasan Terbanyak (Semua Tahun)')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    st.pyplot(fig1)

# Plot bar plot 3 kabupaten/kota terbanyak kekerasan (tahun yang dipilih) - Plot 2
with col2:
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='nama_kabupaten_kota', y='jumlah', data=top_kota_filtered)
    ax2.set_xlabel('Kabupaten/Kota')
    ax2.set_ylabel('Jumlah Kekerasan')
    ax2.set_title(f'3 Kabupaten/Kota dengan Jumlah Kekerasan Terbanyak (Tahun {tahun})')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    st.pyplot(fig2)

# Kesimpulan teks
st.header('Penjelasan')
st.markdown(f"**Tahun yang Dipilih:** {tahun}")
st.markdown("Berdasarkan analisis data kekerasan, berikut adalah kesimpulan yang dapat diambil:")
st.markdown("- 3 kabupaten/kota dengan jumlah kekerasan terbanyak adalah:")
for i, row in top_kota.iterrows():
    st.markdown(f"  - {row['nama_kabupaten_kota']}: {row['jumlah']} kekerasan")
st.markdown("- Dalam tahun yang dipilih, 3 kabupaten/kota dengan jumlah kekerasan terbanyak adalah:")
for i, row in top_kota_filtered.iterrows():
    st.markdown(f"  - {row['nama_kabupaten_kota']}: {row['jumlah']} kekerasan")

st.header('Kesimpulan')
st.markdown("Berdasarkan analisis dan visualisasi yang dihasilkan, menunjukan bahwa jenis kelamin Perempuan mendapatkan tingkat kekerasan paling tinggi")
st.markdown("Berdasarkan tingkat pendidikan, Tidak Diketahui, SD, SLTA, SLTP dan Perguruan Tinggi masuk Lima teratas")
st.markdown("Peningkatan jumlah kekerasan terbanyak terjadi pada tahun 2019 akhir - 2020 awal, ini ada hubungannya dengan pandemi covid 19 karena korelasi antara tempat kejadian kekerasan yaitu Rumah Tangga, dan korban yang merupakan tingkat pendidikan SD (anak kecil) juga korban yang tidak diketahui pendidikannya")
st.markdown("Berdasarkan jenis kelamin, tingkat pendidikan dan tempat kejadian, tingkat kekerasan kota/kabupaten 3 tertingginya adalah Kota Bandung, Kabupaten Sukabumi dan Kabupaten Bandung")

