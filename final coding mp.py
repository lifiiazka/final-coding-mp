import csv
import os


nama_file = r"C:\Users\MyBook J7\Downloads\gym_members_exercise_preview_25_baris.csv"

def baca_dataset():
    data = []

    if not os.path.exists(nama_file):
        print("File dataset tidak ditemukan!")
        print("Pastikan file CSV berada dalam folder program.")
        return data

    try:
        with open(nama_file, "r", newline="", encoding="utf-8-sig") as file:
            pembaca = csv.DictReader(file)

            for baris in pembaca:
                data.append(baris)

        print("Dataset berhasil dibaca.")

    except Exception as error:
        print("Terjadi kesalahan saat membaca dataset:", error)

    return data


def validasi_data(data):
    data_valid = []
    data_tidak_valid = []

    kolom_wajib = [
        "Age", "Gender", "Weight (kg)", "Height (m)",
        "Max_BPM", "Avg_BPM", "Resting_BPM",
        "Session_Duration (hours)", "Calories_Burned",
        "Workout_Type", "Fat_Percentage",
        "Water_Intake (liters)",
        "Workout_Frequency (days/week)",
        "Experience_Level", "BMI"
    ]

    kolom_angka = [
        "Age", "Weight (kg)", "Height (m)",
        "Max_BPM", "Avg_BPM", "Resting_BPM",
        "Session_Duration (hours)", "Calories_Burned",
        "Fat_Percentage", "Water_Intake (liters)",
        "Workout_Frequency (days/week)", "BMI"
    ]

    for nomor, baris in enumerate(data, start=1):
        alasan = ""

        for kolom in kolom_wajib:
            if kolom not in baris or baris[kolom].strip() == "":
                alasan = "Ada data yang kosong"
                break

        if alasan == "":
            try:
                for kolom in kolom_angka:
                    float(baris[kolom])

                if float(baris["Age"]) <= 0:
                    alasan = "Umur tidak valid"

                elif float(baris["Weight (kg)"]) <= 0:
                    alasan = "Berat badan tidak valid"

                elif float(baris["Height (m)"]) <= 0:
                    alasan = "Tinggi badan tidak valid"

                elif float(baris["Session_Duration (hours)"]) <= 0:
                    alasan = "Durasi olahraga tidak valid"

                elif float(baris["Calories_Burned"]) < 0:
                    alasan = "Kalori terbakar tidak valid"

            except ValueError:
                alasan = "Terdapat data angka yang tidak valid"

        if alasan == "":
            data_valid.append(baris)
        else:
            data_tidak_valid.append({
                "baris": nomor,
                "alasan": alasan
            })

    print("\nHasil Validasi Data")
    print("Jumlah data valid:", len(data_valid))
    print("Jumlah data tidak valid:", len(data_tidak_valid))

    return data_valid, data_tidak_valid

def tampilkan_data(data):
    if len(data) == 0:
        print("Tidak ada data untuk ditampilkan.")
        return

    print("\n===== DATASET GYM =====")

    for nomor, baris in enumerate(data, start=1):
        print("\nData ke-", nomor)
        print("Umur:", baris["Age"])
        print("Gender:", baris["Gender"])
        print("Berat Badan:", baris["Weight (kg)"], "kg")
        print("Tinggi Badan:", baris["Height (m)"], "m")
        print("Jenis Olahraga:", baris["Workout_Type"])
        print("Kalori Terbakar:", baris["Calories_Burned"])

def input_data_pengguna():
    print("\n===== INPUT DATA PENGGUNA =====")

    pengguna = {}

    pengguna["nama"] = input("Masukkan nama: ")

    try:
        pengguna["umur"] = int(input("Masukkan umur: "))
        pengguna["gender"] = input("Masukkan gender (Male/Female): ")
        pengguna["berat"] = float(input("Masukkan berat badan (kg): "))
        pengguna["tinggi"] = float(input("Masukkan tinggi badan (m): "))
        pengguna["frekuensi"] = int(
            input("Berapa hari olahraga dalam seminggu? ")
        )
        
        pengguna["tujuan"] = input(
            "Tujuan olahraga (Menurunkan/Mempertahankan/Meningkatkan): "
        )

        if (pengguna["umur"] <= 0 or
            pengguna["berat"] <= 0 or
            pengguna["tinggi"] <= 0 or
            pengguna["frekuensi"] < 0 or
            pengguna["frekuensi"] > 7):
            print("Data tidak valid. Silakan masukkan ulang.")
            return None

        if pengguna["gender"].lower() not in ["male", "female"]:
            print("Gender harus Male atau Female.")
            return None

        print("Data pengguna berhasil dimasukkan.")
        return pengguna

    except ValueError:
        print("Input angka tidak valid.")
        return None

def hitung_bmi(pengguna):
    if pengguna is None:
        print("Masukkan data pengguna terlebih dahulu.")
        return None

    tinggi = pengguna["tinggi"]
    berat = pengguna["berat"]
    if tinggi >3:
        tinggi = tinggi / 100
    if berat <= 0 or tinggi <= 0:
        print("berat dan tinggi badan harus lebih dari 0.")
        return None
    
    bmi = berat / (tinggi ** 2)

    if bmi < 18.5:
        kategori = "Berat badan kurang"
    elif bmi < 25:
        kategori = "Normal"
    elif bmi < 30:
        kategori = "Berat badan berlebih"
    else:
        kategori = "Obesitas"

    print("\n===== HASIL BMI =====")
    print("Nama:", pengguna["nama"])
    print("Nilai BMI:", round(bmi, 2))
    print("Kategori:", kategori)

    hasil = {
        "bmi": round(bmi, 2),
        "kategori_bmi": kategori
    }

    return hasil

def analisis_kalori(data, pengguna):
    if len(data) == 0:
        print("Dataset belum tersedia.")
        return None

    berat = float(pengguna["berat"])
    tinggi = float(pengguna["tinggi"])

    kebutuhan_kalori = (10 * berat) + (6.25 * tinggi)

    total = 0
    kalori_tertinggi = 0
    kalori_terendah = float("inf")

    for baris in data:
        kalori = float(baris["Calories_Burned"])

        total += kalori

        if kalori > kalori_tertinggi:
            kalori_tertinggi = kalori

        if kalori < kalori_terendah:
            kalori_terendah = kalori

    rata_rata = total / len(data)

    print("\n===== ANALISIS KALORI =====")
    print("Berat badan:", berat, "kg")
    print("Tinggi badan:", tinggi, "cm")
    print("Perkiraan kebutuhan kalori:", round(kebutuhan_kalori, 2), "kkal/hari")


    hasil = {
        "kebutuhan_kalori": round(kebutuhan_kalori, 2),
        "rata_rata_kalori": round(rata_rata, 2),
        "kalori_tertinggi": kalori_tertinggi,
        "kalori_terendah": kalori_terendah
    }

    return hasil

def analisis_aktivitas(data, pengguna):
    if len(data) == 0:
        print("Dataset belum tersedia.")
        return None

    berat = float(pengguna["berat"])
    tinggi = float(pengguna["tinggi"])


    tinggi_meter = tinggi / 100
    bmi = berat / (tinggi_meter ** 2)

    kebutuhan_kalori = (10 * berat) + (6.25 * tinggi)

    kelompok_olahraga = {}
    total_durasi = 0
    total_frekuensi = 0

    for baris in data:
        jenis = baris["Workout_Type"]
        kalori = float(baris["Calories_Burned"])
        durasi = float(baris["Session_Duration (hours)"])
        frekuensi = float(baris["Workout_Frequency (days/week)"])

        if jenis not in kelompok_olahraga:
            kelompok_olahraga[jenis] = {
                "jumlah": 0,
                "total_kalori": 0
            }

        kelompok_olahraga[jenis]["jumlah"] += 1
        kelompok_olahraga[jenis]["total_kalori"] += kalori

        total_durasi += durasi
        total_frekuensi += frekuensi

    hasil_olahraga = []

    for jenis, nilai in kelompok_olahraga.items():
        rata_kalori = nilai["total_kalori"] / nilai["jumlah"]

        hasil_olahraga.append({
            "jenis_olahraga": jenis,
            "jumlah": nilai["jumlah"],
            "rata_kalori": round(rata_kalori, 2)
        })

    hasil_olahraga.sort(
        key=lambda x: x["rata_kalori"],
        reverse=True
    )

    rata_durasi = total_durasi / len(data)
    rata_frekuensi = total_frekuensi / len(data)

    print("\n===== ANALISIS AKTIVITAS FISIK =====")
    print("Berat badan:", berat, "kg")
    print("Tinggi badan:", tinggi, "cm")
    print("BMI:", round(bmi, 2))
    print("Estimasi kebutuhan kalori:",
          round(kebutuhan_kalori, 2), "kkal")
    
    print("\nRata-rata durasi olahraga:",
          round(rata_durasi, 2), "jam")

    print("Rata-rata frekuensi olahraga:",
          round(rata_frekuensi, 2), "hari/minggu")

    print("\n===== REKOMENDASI OLAHRAGA =====")

    for olahraga in hasil_olahraga[:3]:
        print(
            "-", olahraga["jenis_olahraga"],
            ":", olahraga["rata_kalori"], "kkal"
        )

    hasil_analisis = {
        "bmi": round(bmi, 2),
        "kebutuhan_kalori": round(kebutuhan_kalori, 2),
        "rata_durasi": round(rata_durasi, 2),
        "rata_frekuensi": round(rata_frekuensi, 2),
        "rekomendasi": hasil_olahraga[:3]
    }

    return hasil_analisis

def rekomendasi_kebugaran(pengguna, hasil_bmi):
    if pengguna is None or hasil_bmi is None:
        print("Masukkan data pengguna dan hitung BMI terlebih dahulu.")
        return None

    print("\n===== REKOMENDASI KEBUGARAN =====")

    rekomendasi = []

    if hasil_bmi["kategori_bmi"] == "Berat badan kurang":
        rekomendasi.append(
            "Lakukan latihan kekuatan dan perhatikan asupan makanan."
        )

    elif hasil_bmi["kategori_bmi"] == "Normal":
        rekomendasi.append(
            "Pertahankan berat badan dengan olahraga teratur."
        )

    elif hasil_bmi["kategori_bmi"] == "Berat badan berlebih":
        rekomendasi.append(
            "Lakukan aktivitas kardio secara bertahap."
        )

    else:
        rekomendasi.append(
            "Mulai aktivitas fisik ringan dan tingkatkan secara bertahap."
        )

    if pengguna["frekuensi"] < 3:
        rekomendasi.append(
            "Tingkatkan frekuensi olahraga secara bertahap."
        )
    else:
        rekomendasi.append(
            "Pertahankan jadwal olahraga dan berikan waktu istirahat."
        )

    if pengguna["tujuan"].lower() == "menurunkan":
        rekomendasi.append(
            "Gabungkan aktivitas kardio dengan pola makan seimbang."
        )

    elif pengguna["tujuan"].lower() == "mempertahankan":
        rekomendasi.append(
            "Jaga konsistensi olahraga dan pola hidup sehat."
        )

    elif pengguna["tujuan"].lower() == "meningkatkan":
        rekomendasi.append(
            "Lakukan latihan kekuatan secara bertahap."
        )

    else:
        rekomendasi.append(
            "Pilih tujuan olahraga yang sesuai dengan kebutuhan."
        )

    for nomor, saran in enumerate(rekomendasi, start=1):
        print(nomor, ".", saran)

    return rekomendasi

def tampilkan_laporan(pengguna, hasil_bmi, hasil_kalori,
                      hasil_aktivitas, rekomendasi):

    if pengguna is None:
        print("Data pengguna belum tersedia.")
        return None

    print("\n====================================")
    print("       LAPORAN KEBUGARAN TUBUH")
    print("====================================")

    print("Nama:", pengguna["nama"])
    print("Umur:", pengguna["umur"])
    print("Berat badan:", pengguna["berat"], "kg")
    print("Tinggi badan:", pengguna["tinggi"], "m")
    print("Tujuan olahraga:", pengguna["tujuan"])

    if hasil_bmi is not None:
        print("BMI:", hasil_bmi["bmi"])
        print("Kategori BMI:", hasil_bmi["kategori_bmi"])

    if hasil_aktivitas is not None:
        print("Rata-rata durasi olahraga:",
              hasil_aktivitas["rata_durasi"], "jam")

    if rekomendasi is not None:
        print("\nRekomendasi:")
        for saran in rekomendasi:
            print("-", saran)

    print("====================================")

    laporan = {
        "nama": pengguna["nama"],
        "umur": pengguna["umur"],
        "berat": pengguna["berat"],
        "tinggi": pengguna["tinggi"],
        "tujuan": pengguna["tujuan"],
        "bmi": hasil_bmi["bmi"] if hasil_bmi else "",
        "kategori_bmi": hasil_bmi["kategori_bmi"] if hasil_bmi else "",
        "rata_rata_kalori": (
            hasil_kalori["rata_rata_kalori"]
            if hasil_kalori else ""
        ),
        "rekomendasi": "; ".join(rekomendasi) if rekomendasi else ""
    }

    return laporan

def simpan_hasil(laporan):
    if laporan is None:
        print("Belum ada laporan untuk disimpan.")
        return

    nama_output = "hasil_perencanaan_kebugaran.csv"

    with open(nama_output, "w", newline="", encoding="utf-8") as file:
        kolom = laporan.keys()

        penulis = csv.DictWriter(file, fieldnames=kolom)
        penulis.writeheader()
        penulis.writerow(laporan)

    print("Hasil berhasil disimpan ke", nama_output)

def menu_utama():
    data = baca_dataset()
    data_valid, data_tidak_valid = validasi_data(data)

    pengguna = None
    hasil_bmi = None
    hasil_kalori = None
    hasil_aktivitas = None
    rekomendasi = None
    laporan = None

    while True:
        print("\n========================================")
        print("       PROGRAM PERENCANAAN KEBUGARAN")
        print("========================================")
        print("1. Menampilkan Dataset Gym")
        print("2. Input Data Pengguna")
        print("3. Menghitung BMI")
        print("4. Analisis Kalori")
        print("5. Analisis Aktivitas Fisik")
        print("6. Rekomendasi Kebugaran")
        print("7. Menampilkan Laporan")
        print("8. Menyimpan Hasil")
        print("0. Keluar")
        print("========================================")

        pilihan = input("Masukkan pilihan Anda: ")

        if pilihan == "1":
            tampilkan_data(data_valid)

        elif pilihan == "2":
            pengguna = input_data_pengguna()
            hasil_bmi = None
            rekomendasi = None
            laporan = None

        elif pilihan == "3":
            hasil_bmi = hitung_bmi(pengguna)
            laporan = None

        elif pilihan == "4":
            hasil_kalori = analisis_kalori(data_valid, pengguna)
            laporan = None

        elif pilihan == "5":
            hasil_aktivitas = analisis_aktivitas(data_valid, pengguna)
            laporan = None

        elif pilihan == "6":
            rekomendasi = rekomendasi_kebugaran(
                pengguna, hasil_bmi
            )
            laporan = None

        elif pilihan == "7":
            laporan = tampilkan_laporan(
                pengguna,
                hasil_bmi,
                hasil_kalori,
                hasil_aktivitas,
                rekomendasi
            )

        elif pilihan == "8":
            simpan_hasil(laporan)

        elif pilihan == "0":
            print("Terima kasih telah menggunakan program.")
            break

        else:
            print("Pilihan tidak tersedia. Silakan coba lagi.")


menu_utama()
import csv
import os

nama_file = "gym_members_exercise_preview_25_baris.csv"

def baca_dataset():
    data = []

    if not os.path.exists(nama_file):
        print("File dataset tidak ditemukan!")
        print("Pastikan file CSV berada dalam folder program.")
        return data

    try:
        with open(nama_file, "r", newline="", encoding="utf-8-sig") as file:
            pembaca = csv.DictReader(file)

            for baris in pembaca:
                data.append(baris)

        print("Dataset berhasil dibaca.")

    except Exception as error:
        print("Terjadi kesalahan saat membaca dataset:", error)

    return data

def validasi_data(data):
    data_valid = []
    data_tidak_valid = []

    kolom_wajib = [
        "Age", "Gender", "Weight (kg)", "Height (m)",
        "Max_BPM", "Avg_BPM", "Resting_BPM",
        "Session_Duration (hours)", "Calories_Burned",
        "Workout_Type", "Fat_Percentage",
        "Water_Intake (liters)",
        "Workout_Frequency (days/week)",
        "Experience_Level", "BMI"
    ]

    kolom_angka = [
        "Age", "Weight (kg)", "Height (m)",
        "Max_BPM", "Avg_BPM", "Resting_BPM",
        "Session_Duration (hours)", "Calories_Burned",
        "Fat_Percentage", "Water_Intake (liters)",
        "Workout_Frequency (days/week)", "BMI"
    ]

    for nomor, baris in enumerate(data, start=1):
        alasan = ""

        for kolom in kolom_wajib:
            if kolom not in baris or baris[kolom].strip() == "":
                alasan = "Ada data yang kosong"
                break

        if alasan == "":
            try:
                for kolom in kolom_angka:
                    float(baris[kolom])

                if float(baris["Age"]) <= 0:
                    alasan = "Umur tidak valid"

                elif float(baris["Weight (kg)"]) <= 0:
                    alasan = "Berat badan tidak valid"

                elif float(baris["Height (m)"]) <= 0:
                    alasan = "Tinggi badan tidak valid"

                elif float(baris["Session_Duration (hours)"]) <= 0:
                    alasan = "Durasi olahraga tidak valid"

                elif float(baris["Calories_Burned"]) < 0:
                    alasan = "Kalori terbakar tidak valid"

            except ValueError:
                alasan = "Terdapat data angka yang tidak valid"

        if alasan == "":
            data_valid.append(baris)
        else:
            data_tidak_valid.append({
                "baris": nomor,
                "alasan": alasan
            })

    print("\nHasil Validasi Data")
    print("Jumlah data valid:", len(data_valid))
    print("Jumlah data tidak valid:", len(data_tidak_valid))

    return data_valid, data_tidak_valid

def tampilkan_data(data):
    if len(data) == 0:
        print("Tidak ada data untuk ditampilkan.")
        return

    print("\n===== DATASET GYM =====")

    for nomor, baris in enumerate(data, start=1):
        print("\nData ke-", nomor)
        print("Umur:", baris["Age"])
        print("Gender:", baris["Gender"])
        print("Berat Badan:", baris["Weight (kg)"], "kg")
        print("Tinggi Badan:", baris["Height (m)"], "m")
        print("Jenis Olahraga:", baris["Workout_Type"])
        print("Kalori Terbakar:", baris["Calories_Burned"])


def input_data_pengguna():
    print("\n===== INPUT DATA PENGGUNA =====")

    pengguna = {}

    pengguna["nama"] = input("Masukkan nama: ")

    try:
        pengguna["umur"] = int(input("Masukkan umur: "))
        pengguna["gender"] = input("Masukkan gender (Male/Female): ")
        pengguna["berat"] = float(input("Masukkan berat badan (kg): "))
        pengguna["tinggi"] = float(input("Masukkan tinggi badan (m): "))
        pengguna["frekuensi"] = int(
            input("Berapa hari olahraga dalam seminggu? ")
        )
        
        pengguna["tujuan"] = input(
            "Tujuan olahraga (Menurunkan/Mempertahankan/Meningkatkan): "
        )

        if (pengguna["umur"] <= 0 or
            pengguna["berat"] <= 0 or
            pengguna["tinggi"] <= 0 or
            pengguna["frekuensi"] < 0 or
            pengguna["frekuensi"] > 7):
            print("Data tidak valid. Silakan masukkan ulang.")
            return None

        if pengguna["gender"].lower() not in ["male", "female"]:
            print("Gender harus Male atau Female.")
            return None

        print("Data pengguna berhasil dimasukkan.")
        return pengguna

    except ValueError:
        print("Input angka tidak valid.")
        return None

# 5. Fungsi menghitung BMI
def hitung_bmi(pengguna):
    if pengguna is None:
        print("Masukkan data pengguna terlebih dahulu.")
        return None

    tinggi = pengguna["tinggi"]
    berat = pengguna["berat"]
    if tinggi >3:
        tinggi = tinggi / 100
    if berat <= 0 or tinggi <= 0:
        print("berat dan tinggi badan harus lebih dari 0.")
        return None
    
    bmi = berat / (tinggi ** 2)

    if bmi < 18.5:
        kategori = "Berat badan kurang"
    elif bmi < 25:
        kategori = "Normal"
    elif bmi < 30:
        kategori = "Berat badan berlebih"
    else:
        kategori = "Obesitas"

    print("\n===== HASIL BMI =====")
    print("Nama:", pengguna["nama"])
    print("Nilai BMI:", round(bmi, 2))
    print("Kategori:", kategori)

    hasil = {
        "bmi": round(bmi, 2),
        "kategori_bmi": kategori
    }

    return hasil

def analisis_kalori(data, pengguna):
    if len(data) == 0:
        print("Dataset belum tersedia.")
        return None

    berat = float(pengguna["berat"])
    tinggi = float(pengguna["tinggi"])

    kebutuhan_kalori = (10 * berat) + (6.25 * tinggi)

    total = 0
    kalori_tertinggi = 0
    kalori_terendah = float("inf")

    for baris in data:
        kalori = float(baris["Calories_Burned"])

        total += kalori

        if kalori > kalori_tertinggi:
            kalori_tertinggi = kalori

        if kalori < kalori_terendah:
            kalori_terendah = kalori

    rata_rata = total / len(data)

    print("\n===== ANALISIS KALORI =====")
    print("Berat badan:", berat, "kg")
    print("Tinggi badan:", tinggi, "cm")
    print("Perkiraan kebutuhan kalori:", round(kebutuhan_kalori, 2), "kkal/hari")


    hasil = {
        "kebutuhan_kalori": round(kebutuhan_kalori, 2),
        "rata_rata_kalori": round(rata_rata, 2),
        "kalori_tertinggi": kalori_tertinggi,
        "kalori_terendah": kalori_terendah
    }

    return hasil

def analisis_aktivitas(data, pengguna):
    if len(data) == 0:
        print("Dataset belum tersedia.")
        return None

    berat = float(pengguna["berat"])
    tinggi = float(pengguna["tinggi"])

    tinggi_meter = tinggi / 100
    bmi = berat / (tinggi_meter ** 2)

    kebutuhan_kalori = (10 * berat) + (6.25 * tinggi)

    kelompok_olahraga = {}
    total_durasi = 0
    total_frekuensi = 0

    for baris in data:
        jenis = baris["Workout_Type"]
        kalori = float(baris["Calories_Burned"])
        durasi = float(baris["Session_Duration (hours)"])
        frekuensi = float(baris["Workout_Frequency (days/week)"])

        if jenis not in kelompok_olahraga:
            kelompok_olahraga[jenis] = {
                "jumlah": 0,
                "total_kalori": 0
            }

        kelompok_olahraga[jenis]["jumlah"] += 1
        kelompok_olahraga[jenis]["total_kalori"] += kalori

        total_durasi += durasi
        total_frekuensi += frekuensi

    hasil_olahraga = []

    for jenis, nilai in kelompok_olahraga.items():
        rata_kalori = nilai["total_kalori"] / nilai["jumlah"]

        hasil_olahraga.append({
            "jenis_olahraga": jenis,
            "jumlah": nilai["jumlah"],
            "rata_kalori": round(rata_kalori, 2)
        })

    hasil_olahraga.sort(
        key=lambda x: x["rata_kalori"],
        reverse=True
    )

    rata_durasi = total_durasi / len(data)
    rata_frekuensi = total_frekuensi / len(data)

    print("\n===== ANALISIS AKTIVITAS FISIK =====")
    print("Berat badan:", berat, "kg")
    print("Tinggi badan:", tinggi, "cm")
    print("BMI:", round(bmi, 2))
    print("Estimasi kebutuhan kalori:",
          round(kebutuhan_kalori, 2), "kkal")
    
    print("\nRata-rata durasi olahraga:",
          round(rata_durasi, 2), "jam")

    print("Rata-rata frekuensi olahraga:",
          round(rata_frekuensi, 2), "hari/minggu")

    print("\n===== REKOMENDASI OLAHRAGA =====")

    for olahraga in hasil_olahraga[:3]:
        print(
            "-", olahraga["jenis_olahraga"],
            ":", olahraga["rata_kalori"], "kkal"
        )

    # Mengembalikan hasil dalam bentuk dictionary
    hasil_analisis = {
        "bmi": round(bmi, 2),
        "kebutuhan_kalori": round(kebutuhan_kalori, 2),
        "rata_durasi": round(rata_durasi, 2),
        "rata_frekuensi": round(rata_frekuensi, 2),
        "rekomendasi": hasil_olahraga[:3]
    }

    return hasil_analisis

def rekomendasi_kebugaran(pengguna, hasil_bmi):
    if pengguna is None or hasil_bmi is None:
        print("Masukkan data pengguna dan hitung BMI terlebih dahulu.")
        return None

    print("\n===== REKOMENDASI KEBUGARAN =====")

    rekomendasi = []

    if hasil_bmi["kategori_bmi"] == "Berat badan kurang":
        rekomendasi.append(
            "Lakukan latihan kekuatan dan perhatikan asupan makanan."
        )

    elif hasil_bmi["kategori_bmi"] == "Normal":
        rekomendasi.append(
            "Pertahankan berat badan dengan olahraga teratur."
        )

    elif hasil_bmi["kategori_bmi"] == "Berat badan berlebih":
        rekomendasi.append(
            "Lakukan aktivitas kardio secara bertahap."
        )

    else:
        rekomendasi.append(
            "Mulai aktivitas fisik ringan dan tingkatkan secara bertahap."
        )

    if pengguna["frekuensi"] < 3:
        rekomendasi.append(
            "Tingkatkan frekuensi olahraga secara bertahap."
        )
    else:
        rekomendasi.append(
            "Pertahankan jadwal olahraga dan berikan waktu istirahat."
        )

    if pengguna["tujuan"].lower() == "menurunkan":
        rekomendasi.append(
            "Gabungkan aktivitas kardio dengan pola makan seimbang."
        )

    elif pengguna["tujuan"].lower() == "mempertahankan":
        rekomendasi.append(
            "Jaga konsistensi olahraga dan pola hidup sehat."
        )

    elif pengguna["tujuan"].lower() == "meningkatkan":
        rekomendasi.append(
            "Lakukan latihan kekuatan secara bertahap."
        )

    else:
        rekomendasi.append(
            "Pilih tujuan olahraga yang sesuai dengan kebutuhan."
        )

    for nomor, saran in enumerate(rekomendasi, start=1):
        print(nomor, ".", saran)

    return rekomendasi

def tampilkan_laporan(pengguna, hasil_bmi, hasil_kalori,
                      hasil_aktivitas, rekomendasi):

    if pengguna is None:
        print("Data pengguna belum tersedia.")
        return None

    print("\n====================================")
    print("       LAPORAN KEBUGARAN TUBUH")
    print("====================================")

    print("Nama:", pengguna["nama"])
    print("Umur:", pengguna["umur"])
    print("Berat badan:", pengguna["berat"], "kg")
    print("Tinggi badan:", pengguna["tinggi"], "m")
    print("Tujuan olahraga:", pengguna["tujuan"])

    if hasil_bmi is not None:
        print("BMI:", hasil_bmi["bmi"])
        print("Kategori BMI:", hasil_bmi["kategori_bmi"])

    if hasil_aktivitas is not None:
        print("Rata-rata durasi olahraga:",
              hasil_aktivitas["rata_durasi"], "jam")

    if rekomendasi is not None:
        print("\nRekomendasi:")
        for saran in rekomendasi:
            print("-", saran)

    print("====================================")

    laporan = {
        "nama": pengguna["nama"],
        "umur": pengguna["umur"],
        "berat": pengguna["berat"],
        "tinggi": pengguna["tinggi"],
        "tujuan": pengguna["tujuan"],
        "bmi": hasil_bmi["bmi"] if hasil_bmi else "",
        "kategori_bmi": hasil_bmi["kategori_bmi"] if hasil_bmi else "",
        "rata_rata_kalori": (
            hasil_kalori["rata_rata_kalori"]
            if hasil_kalori else ""
        ),
        "rekomendasi": "; ".join(rekomendasi) if rekomendasi else ""
    }

    return laporan


def simpan_hasil(laporan):
    if laporan is None:
        print("Belum ada laporan untuk disimpan.")
        return

    nama_output = "hasil_perencanaan_kebugaran.csv"

    with open(nama_output, "w", newline="", encoding="utf-8") as file:
        kolom = laporan.keys()

        penulis = csv.DictWriter(file, fieldnames=kolom)
        penulis.writeheader()
        penulis.writerow(laporan)

    print("Hasil berhasil disimpan ke", nama_output)


def menu_utama():
    data = baca_dataset()
    data_valid, data_tidak_valid = validasi_data(data)

    pengguna = None
    hasil_bmi = None
    hasil_kalori = None
    hasil_aktivitas = None
    rekomendasi = None
    laporan = None

    while True:
        print("\n========================================")
        print("       PROGRAM PERENCANAAN KEBUGARAN")
        print("========================================")
        print("1. Menampilkan Dataset Gym")
        print("2. Input Data Pengguna")
        print("3. Menghitung BMI")
        print("4. Analisis Kalori")
        print("5. Analisis Aktivitas Fisik")
        print("6. Rekomendasi Kebugaran")
        print("7. Menampilkan Laporan")
        print("8. Menyimpan Hasil")
        print("0. Keluar")
        print("========================================")

        pilihan = input("Masukkan pilihan Anda: ")

        if pilihan == "1":
            tampilkan_data(data_valid)

        elif pilihan == "2":
            pengguna = input_data_pengguna()
            hasil_bmi = None
            rekomendasi = None
            laporan = None

        elif pilihan == "3":
            hasil_bmi = hitung_bmi(pengguna)
            laporan = None

        elif pilihan == "4":
            hasil_kalori = analisis_kalori(data_valid, pengguna)
            laporan = None

        elif pilihan == "5":
            hasil_aktivitas = analisis_aktivitas(data_valid, pengguna)
            laporan = None

        elif pilihan == "6":
            rekomendasi = rekomendasi_kebugaran(
                pengguna, hasil_bmi
            )
            laporan = None

        elif pilihan == "7":
            laporan = tampilkan_laporan(
                pengguna,
                hasil_bmi,
                hasil_kalori,
                hasil_aktivitas,
                rekomendasi
            )

        elif pilihan == "8":
            simpan_hasil(laporan)

        elif pilihan == "0":
            print("Terima kasih telah menggunakan program.")
            break

        else:
            print("Pilihan tidak tersedia. Silakan coba lagi.")

menu_utama()


       