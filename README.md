Aplikasi CLI (Command Line Interface) berbasis Python untuk membantu menganalisis data anggota gym, menghitung Indeks Massa Tubuh (BMI) dan kebutuhan kalori harian, serta memberikan rekomendasi jenis dan porsi latihan kebugaran berdasarkan profil pengguna dan dataset.

Disusun oleh Kelompok Mini Projek 2A

Lifia Azka Sajeeda (2610932004)

Nadindra Handika Leswari (2610931005)

Siti Diana (2610931009)

Wianda Dea Estu Wahyudi (2610932012)

Fitur utama:

Pembacaan & Validasi Dataset : Membaca file CSV, mengonversi tinggi dari meter ke sentimeter (`Height (cm)`), serta memvalidasi kelengkapan kolom wajib dan nilai numerik

Input dan Tampilan Data Pengguna : Mengambil data profil pengguna (nama, usia, jenis kelamin, berat badan, tinggi badan, frekuensi olahraga 1–7 hari/minggu, dan tujuan kebugaran).

Perhitungan BMI: Menghitung nilai BMI dan mengkategorikannya (Berat badan kurang, Normal, Berat badan berlebih, atau Obesitas).

Analisis Kebutuhan Kalori Harian: Menghitung BMR  dan mengalikannya dengan faktor aktivitas berdasarkan frekuensi latihan, lalu menyesuaikan target kalori harian sesuai tujuan (Menurunkan `-500 kkal`, Mempertahankan `0`, atau Meningkatkan `+300 kkal`).

Analisis Aktivitas Fisik: Mengelompokkan data berdasarkan jenis olahraga (`Yoga`, `HIIT`, `Cardio`, `Strength`), menghitung rata-rata kalori, durasi, dan rasio BPM (`Avg_BPM / Max_BPM`) untuk menentukan intensitas (Ringan, Menengah, Berat), estimasi kalori sesuai berat badan pengguna, serta jenis olahraga yang direkomendasikan.

Rekomendasi Kebugaran & Laporan: Menyusun saran durasi, jumlah set, waktu istirahat, serta catatan khusus sesuai kondisi BMI dan frekuensi latihan.


Mengekspor Hasil ke CSV: Menyimpan laporan perencanaan kebugaran pengguna ke file `hasil_perencanaan_kebugaran.csv`.

Struktur Repositori:

final coding mp main.py

gym_members_exercise_preview_25_baris.csv

hasil_perencanaan_kebugaran.csv

README.md
