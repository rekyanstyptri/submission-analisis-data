# 🌫️ Beijing Air Quality Analysis Dashboard

![Python](https://img.shields.io/badge/Python-3-blue?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat-square&logo=pandas&logoColor=white)
![Deployment](https://img.shields.io/badge/Deployment-Streamlit%20Cloud-19A7A0?style=flat-square)

## 📋 Deskripsi Proyek

Proyek ini menganalisis kualitas udara Beijing berdasarkan data dari **12 stasiun pemantauan** pada periode **1 Maret 2013–28 Februari 2017**. Analisis berfokus pada perubahan konsentrasi PM2.5, hubungan variabel meteorologis dengan PM2.5, serta perbandingan profil polusi antarstasiun. Hasil analisis disajikan melalui dashboard interaktif menggunakan **Streamlit**.

Dashboard memiliki filter **tahun** dan **stasiun**, serta tiga halaman analisis:

1. **Tren PM2.5:** rata-rata konsentrasi berdasarkan tahun, bulan, dan jam.
2. **Pengaruh Cuaca:** korelasi PM2.5 dengan variabel meteorologis, kecepatan angin, dan arah angin.
3. **Profil Stasiun:** perbandingan tingkat polusi serta pengelompokan deskriptif stasiun berdasarkan batas PM2.5 yang ditetapkan secara manual (bukan algoritma clustering).

---

## 🔗 Link Penting

| Deskripsi | Link |
|---|---|
| 🌐 Dashboard Online | [Beijing Air Quality Dashboard](https://dashboard-air-quality-rekyan.streamlit.app/) |
| 📓 Notebook Analisis | [Colab_Notebook-2.ipynb](./Colab_Notebook-2.ipynb) |
| 📦 Sumber Dataset | [UCI Machine Learning Repository — Beijing Multi-Site Air Quality](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality) |
| 💻 Repositori GitHub | [submission-analisis-data](https://github.com/rekyanstyptri/submission-analisis-data) |

---

## 📂 Struktur Direktori

```text
submission-analisis-data/
├── dashboard/
│   ├── dashboard_air_quality.py
│   └── main_data.csv.gz
├── data/
│   └── .gitkeep
├── Colab_Notebook-2.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

`main_data.csv.gz` merupakan CSV terkompresi yang dipakai dashboard. Folder `data/` disiapkan untuk data mentah; ganti bagian `.gitkeep` pada struktur di atas apabila file data mentah sudah diunggah.

---

## 🚀 Panduan Menjalankan Aplikasi

### 1. Clone Repositori

```bash
git clone https://github.com/rekyanstyptri/submission-analisis-data.git
cd submission-analisis-data
```

### 2. Siapkan Virtual Environment (Disarankan)

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (Command Prompt):

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Instal Library

```bash
python -m pip install -r requirements.txt
```

### 4. Jalankan Dashboard

Jalankan dari direktori utama repositori:

```bash
python -m streamlit run dashboard/dashboard_air_quality.py
```

Buka `http://localhost:8501` di browser apabila tidak terbuka secara otomatis.

---

## 📝 Catatan Analisis

Hubungan korelasi pada dashboard bersifat **asosiatif**, bukan bukti sebab-akibat. Kelompok profil stasiun menggunakan **batas kategori manual**, sehingga tidak boleh diinterpretasikan sebagai hasil algoritma clustering.

## 👤 Author

**Rekyan Setyoputri Prameswari**  
Proyek Akhir Analisis Data — Dicoding Indonesia
