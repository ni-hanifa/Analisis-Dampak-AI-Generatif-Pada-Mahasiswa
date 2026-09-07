# Analisis Dampak Penggunaan AI Generatif terhadap Performa Akademik dan Kesejahteraan Mental Mahasiswa

**Live Dashboard:** [Dampak AI Generatif pada Mahasiswa](https://dampak-aigenerative-mahasiswa.streamlit.app/)

## Abstrak
Adopsi pesat kecerdasan buatan generatif dalam pendidikan tinggi menghadirkan peluang personalisasi pembelajaran sekaligus tantangan berupa beban kognitif dan ancaman terhadap kesehatan mental[cite: 8]. Penelitian ini bertujuan untuk mengevaluasi korelasi intensitas penggunaan AI dengan perubahan Indeks Prestasi Kumulatif (IPK), dampak ketergantungan AI terhadap retensi keterampilan, serta pengaruh kebijakan institusi terhadap tingkat kecemasan dan sindrom kelelahan kronis atau *burnout*[cite: 8]. 

## Dataset dan Metodologi
Penelitian ini menggunakan dataset evaluasi institusi pendidikan yang mencakup 50.000 data mahasiswa dari berbagai perguruan tinggi[cite: 5]. Analisis dilakukan menggunakan bahasa pemrograman Python dengan pendekatan *Exploratory Data Analysis* (EDA)[cite: 5]. Metodologi mencakup praproses data, rekayasa fitur untuk mengelompokkan segmen pengguna AI, serta analisis statistik inferensial dan deskriptif[cite: 8].

## Temuan Utama
* **Paradoks Intensitas Penggunaan:** Penggunaan AI secara moderat (5 hingga 15 jam per minggu) menghasilkan rata-rata peningkatan IPK yang paling optimal sebesar 0,227[cite: 8]. Segmen pengguna berat (di atas 15 jam per minggu) justru mencatatkan peningkatan terendah sebesar 0,173 akibat fenomena *diminishing returns*[cite: 8].
* **Penurunan Retensi Keterampilan:** Terdapat korelasi negatif antara persepsi ketergantungan AI dengan skor retensi keterampilan[cite: 8]. Ketergantungan ekstrem memunculkan nilai pencilan di bawah skor 40 pada rentang 100 yang mengikis kemampuan analitis dasar mahasiswa[cite: 9].
* **Dampak Kebijakan Institusi:** Kebijakan pelarangan AI secara mutlak berkorelasi dengan tingginya populasi mahasiswa pada kategori risiko *high burnout* yang mendominasi hingga lebih dari 25 persen[cite: 9]. Kebijakan pelarangan mutlak juga memicu batas kuartil atas tingkat kecemasan saat ujian menyentuh skor 7,0[cite: 9].
* **Peta Risiko Kritis:** Mahasiswa pengguna berat dengan tingkat ketergantungan AI di atas 3,5 sangat rentan mengalami *burnout* tinggi dan berpotensi mengalami kegagalan akademik[cite: 9].

## Rekomendasi Kebijakan
* **Integrasi Terpandu:** Institusi pendidikan perlu meninggalkan pendekatan pelarangan mutlak dan merumuskan silabus literasi AI dengan batas ideal penggunaan 10 hingga 15 jam per minggu[cite: 9].
* **Konseling Tepat Sasaran:** Pusat bimbingan konseling kampus direkomendasikan untuk menggunakan data prediktif guna memprioritaskan pendampingan bagi mahasiswa yang berada di zona risiko kritis[cite: 9].
* **Restrukturisasi Evaluasi:** Institusi perlu meningkatkan porsi evaluasi sinkronus (seperti ujian lisan dan pemecahan masalah langsung di laboratorium) sebesar 40 persen untuk mencegah penurunan kemampuan retensi keterampilan[cite: 9].

## Teknologi yang Digunakan
* **Bahasa Pemrograman:** Python 3.x[cite: 5]
* **Library Analisis:** Pandas, NumPy, Matplotlib, Seaborn, Plotly[cite: 4, 6]
* **Lingkungan Analisis:** Jupyter Notebook[cite: 5]
* **Visualisasi Dashboard:** Streamlit[cite: 5]
