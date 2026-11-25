mport csv
import os

nama_file = "gym_members_exercise_preview_25_baris.csv"



def baca_dataset():
    data = []

    try:
        with open(nama_file, mode="r", encoding="utf-8-sig") as file:
            pembaca = csv.DictReader(file)

            for baris in pembaca:
                if "Height (m)" in baris:
                    tinggi_cm = float(baris["Height (m)"]) * 100
                    baris["Height (cm)"] = str(tinggi_cm)

                data.append(baris)

        print("Dataset berhasil dibaca.")
        return data

    except FileNotFoundError:
        print("File dataset tidak ditemukan.")
        return []

    except (ValueError, KeyError):
        print("Terdapat kesalahan pada format dataset.")
        return []



def validasi_data(data):
    kolom_wajib = [
        "Age", "Gender", "Weight (kg)", "Height (cm)",
        "Max_BPM", "Avg_BPM", "Resting_BPM",
        "Session_Duration (hours)", "Calories_Burned",
        "Workout_Type", "Fat_Percentage", "Water_Intake (liters)",
        "Workout_Frequency (days/week)", "Experience_Level", "BMI"
    ]

    data_valid = []
    jumlah_tidak_valid = 0

    for baris in data:
        valid = True

        for kolom in kolom_wajib:
            if (
                kolom not in baris
                or baris[kolom] is None
                or baris[kolom].strip() == ""
            ):
                valid = False
                break

        if valid:
            try:
                for kolom in kolom_wajib:
                    if kolom not in [
                        "Gender", "Workout_Type", "Experience_Level"
                    ]:
                        float(baris[kolom])

                if (
                    float(baris["Age"]) <= 0
                    or float(baris["Weight (kg)"]) <= 0
                    or float(baris["Height (cm)"]) <= 0
                    or float(baris["Session_Duration (hours)"]) <= 0
                    or float(baris["Calories_Burned"]) < 0
                    or float(baris["Max_BPM"]) <= 0
                ):
                    valid = False

            except ValueError:
                valid = False

        if valid:
            data_valid.append(baris)
        else:
            jumlah_tidak_valid += 1

    print("\nHASIL VALIDASI DATASET")
    print("Jumlah data valid       :", len(data_valid))
    print("Jumlah data tidak valid :", jumlah_tidak_valid)

    return data_valid



def tampilkan_data(data):
    print("\nSELURUH DATASET ANGGOTA GYM")
    print("=" * 150)

    if len(data) == 0:
        print("Dataset tidak tersedia.")
        return

    kolom = list(data[0].keys())

    print(" | ".join(kolom))
    print("-" * 150)

    for baris in data:
        nilai = [str(baris.get(k, "")) for k in kolom]
        print(" | ".join(nilai))

    print("=" * 150)
    print("Seluruh dataset berhasil ditampilkan.")



def input_data_pengguna():
    print("\nINPUT DATA PENGGUNA")

    try:
        nama = input("Masukkan nama: ")
        usia = int(input("Masukkan usia: "))

        print("\nJenis kelamin:")
        print("m. Laki-laki")
        print("f. Perempuan")
        gender = input("Pilih jenis kelamin (m/f): ").lower()

        berat = float(input("Masukkan berat badan (kg): "))
        tinggi = int(input("Masukkan tinggi badan (cm): "))

        frekuensi = int(
            input("Frekuensi olahraga dalam seminggu (1-7): ")
        )

        print("\nPilih tujuan kebugaran:")
        print("1. Menurunkan berat badan")
        print("2. Mempertahankan berat badan")
        print("3. Meningkatkan massa otot")

        pilihan_tujuan = input("Masukkan pilihan (1-3): ")

        if pilihan_tujuan == "1":
            tujuan = "Menurunkan"
        elif pilihan_tujuan == "2":
            tujuan = "Mempertahankan"
        elif pilihan_tujuan == "3":
            tujuan = "Meningkatkan"
        else:
            print("Pilihan tujuan tidak valid.")
            return None

        if usia <= 0 or berat <= 0 or tinggi <= 0:
            print("Usia, berat, dan tinggi harus lebih dari 0.")
            return None

        if gender not in ["m", "f"]:
            print("Jenis kelamin harus m atau f.")
            return None

        if frekuensi < 1 or frekuensi > 7:
            print("Frekuensi olahraga harus antara 1 sampai 7 hari.")
            return None

        return {
            "nama": nama,
            "usia": usia,
            "gender": gender,
            "berat": berat,
            "tinggi": tinggi,
            "frekuensi": frekuensi,
            "tujuan": tujuan
        }

    except ValueError:
        print("Input harus menggunakan format angka yang benar.")
        return None



def hitung_bmi(pengguna):
    if pengguna is None:
        return None

    berat = pengguna["berat"]
    tinggi = pengguna["tinggi"] / 100

    bmi = berat / (tinggi ** 2)

    if bmi < 18.5:
        kategori = "Berat badan kurang"
    elif bmi < 25:
        kategori = "Normal"
    elif bmi < 30:
        kategori = "Berat badan berlebih"
    else:
        kategori = "Obesitas"

    print("\nHASIL PERHITUNGAN BMI")
    print("BMI:", round(bmi, 2))
    print("Kategori:", kategori)

    return {
        "bmi": bmi,
        "kategori_bmi": kategori
    }



def analisis_kalori(data, pengguna):
    if len(data) == 0 or pengguna is None:
        print("Data tidak tersedia untuk analisis kalori.")
        return None

    berat = pengguna["berat"]
    tinggi = pengguna["tinggi"]
    usia = pengguna["usia"]
    gender = pengguna["gender"]
    frekuensi = pengguna["frekuensi"]
    tujuan = pengguna["tujuan"]

    
    if gender == "m":
        bmr = (10 * berat) + (6.25 * tinggi) - (5 * usia) + 5
    else:
        bmr = (10 * berat) + (6.25 * tinggi) - (5 * usia) - 161

    
    if frekuensi <= 2:
        faktor_aktivitas = 1.2
    elif frekuensi <= 4:
        faktor_aktivitas = 1.375
    elif frekuensi <= 6:
        faktor_aktivitas = 1.55
    else:
        faktor_aktivitas = 1.725

    kebutuhan_harian = bmr * faktor_aktivitas

    
    if tujuan == "Menurunkan":
        target_kalori = kebutuhan_harian - 500
    elif tujuan == "Mempertahankan":
        target_kalori = kebutuhan_harian
    else:
        target_kalori = kebutuhan_harian + 300

    total_kalori = 0

    for baris in data:
        total_kalori += float(baris["Calories_Burned"])

    rata_rata_kalori = total_kalori / len(data)

    print("\nANALISIS KEBUTUHAN KALORI HARIAN")
    print("Kebutuhan kalori harian:",
          round(kebutuhan_harian, 2), "kkal/hari")
    print("Target kalori berdasarkan tujuan:",
          round(target_kalori, 2), "kkal/hari")
    
    return {
        "kebutuhan_harian": kebutuhan_harian,
        "target_kalori": target_kalori,
        
    }



def rekomendasi_set_aktivitas(jenis, tujuan):

    if jenis == "Yoga":
        if tujuan == "Menurunkan":
            return "3 set, 5-6 gerakan, tahan 20-30 detik"
        elif tujuan == "Mempertahankan":
            return "2-3 set, 5-6 gerakan, tahan 20-30 detik"
        else:
            return "2-3 set, 5-6 gerakan untuk fleksibilitas"

    elif jenis == "HIIT":
        if tujuan == "Menurunkan":
            return "3 set, 4-6 interval, 30 detik latihan"
        elif tujuan == "Mempertahankan":
            return "2-3 set, 4 interval, 30 detik latihan"
        else:
            return "2 set, 3-4 interval sebagai latihan tambahan"

    elif jenis == "Cardio":
        if tujuan == "Menurunkan":
            return "3 set, 10 menit per set"
        elif tujuan == "Mempertahankan":
            return "2-3 set, 10 menit per set"
        else:
            return "2 set, 10 menit sebagai latihan pendukung"

    elif jenis == "Strength":
        if tujuan == "Menurunkan":
            return "3 set, 12-15 repetisi"
        elif tujuan == "Mempertahankan":
            return "2-3 set, 10-12 repetisi"
        else:
            return "3-4 set, 8-12 repetisi"

    return "Belum ada rekomendasi untuk jenis olahraga ini"



def analisis_aktivitas(data, pengguna):

    if len(data) == 0 or pengguna is None:
        print("Data tidak tersedia untuk analisis aktivitas.")
        return None

    berat_pengguna = pengguna["berat"]
    tinggi_pengguna = pengguna["tinggi"] / 100
    bmi_pengguna = berat_pengguna / (tinggi_pengguna ** 2)
    tujuan = pengguna["tujuan"]

    kelompok_olahraga = {}

    
    for baris in data:
        jenis = baris["Workout_Type"]

        if jenis not in kelompok_olahraga:
            kelompok_olahraga[jenis] = {
                "jumlah": 0,
                "total_kalori": 0,
                "total_durasi": 0,
                "total_berat": 0,
                "total_bpm": 0,
                "total_max_bpm": 0
            }

        kelompok_olahraga[jenis]["jumlah"] += 1
        kelompok_olahraga[jenis]["total_kalori"] += float(
            baris["Calories_Burned"]
        )
        kelompok_olahraga[jenis]["total_durasi"] += float(
            baris["Session_Duration (hours)"]
        )
        kelompok_olahraga[jenis]["total_berat"] += float(
            baris["Weight (kg)"]
        )
        kelompok_olahraga[jenis]["total_bpm"] += float(
            baris["Avg_BPM"]
        )
        kelompok_olahraga[jenis]["total_max_bpm"] += float(
            baris["Max_BPM"]
        )

    print("\n======================================")
    print("ANALISIS AKTIVITAS FISIK")
    print("======================================")

    print("Nama pengguna:", pengguna["nama"])
    print("Berat badan:", berat_pengguna, "kg")
    print("Tinggi badan:", pengguna["tinggi"], "cm")
    print("BMI:", round(bmi_pengguna, 2))
    print("Tujuan kebugaran:", tujuan)

    hasil_analisis = {}

    
    for jenis, nilai in kelompok_olahraga.items():

        jumlah = nilai["jumlah"]

        rata_kalori = nilai["total_kalori"] / jumlah
        rata_durasi = nilai["total_durasi"] / jumlah
        rata_berat = nilai["total_berat"] / jumlah
        rata_bpm = nilai["total_bpm"] / jumlah
        rata_max_bpm = nilai["total_max_bpm"] / jumlah

        estimasi_kalori = (
            rata_kalori * berat_pengguna / rata_berat
        )

        rasio_bpm = rata_bpm / rata_max_bpm

        if rasio_bpm < 0.78:
            intensitas = "Ringan"
        elif rasio_bpm < 0.85:
            intensitas = "Menengah"
        else:
            intensitas = "Berat"

        jumlah_set = rekomendasi_set_aktivitas(jenis, tujuan)

        hasil_analisis[jenis] = {
            "rata_kalori": rata_kalori,
            "rata_durasi": rata_durasi,
            "estimasi_kalori": estimasi_kalori,
            "intensitas": intensitas,
            "rasio_bpm": rasio_bpm,
            "jumlah_set": jumlah_set
        }

        print("\n--------------------------------------")
        print("JENIS OLAHRAGA:", jenis)
        print("--------------------------------------")

        print("Rata-rata kalori terbakar:",
              round(rata_kalori, 2), "kkal")

        print("Rata-rata durasi:",
              round(rata_durasi * 60, 2), "menit")

        print("Rata-rata denyut jantung:",
              round(rata_bpm, 2), "BPM")

        print("Intensitas berdasarkan dataset:", intensitas)

        print("Estimasi kalori untuk pengguna:",
              round(estimasi_kalori, 2), "kkal")

        print("Rekomendasi jumlah set:")
        print(jumlah_set)

        if bmi_pengguna >= 30 and intensitas == "Berat":
            print(
                "Catatan: Mulai dengan intensitas lebih rendah "
                "dan tingkatkan secara bertahap."
            )

        elif bmi_pengguna < 18.5:
            print(
                "Catatan: Perhatikan pemenuhan nutrisi "
                "dan pemulihan tubuh."
            )

    
    if tujuan == "Menurunkan":
        jenis_rekomendasi = max(
            hasil_analisis,
            key=lambda jenis: hasil_analisis[jenis]["estimasi_kalori"]
        )

    elif tujuan == "Mempertahankan":
        jenis_rekomendasi = min(
            hasil_analisis,
            key=lambda jenis: abs(
                hasil_analisis[jenis]["rasio_bpm"] - 0.81
            )
        )

    else:
        if "Strength" in hasil_analisis:
            jenis_rekomendasi = "Strength"
        else:
            jenis_rekomendasi = max(
                hasil_analisis,
                key=lambda jenis: hasil_analisis[jenis]["estimasi_kalori"]
            )

    print("\nJENIS OLAHRAGA YANG DIREKOMENDASIKAN:")
    print(jenis_rekomendasi)

    return {
        "bmi": bmi_pengguna,
        "hasil_analisis": hasil_analisis,
        "jenis_rekomendasi": jenis_rekomendasi,
        "tujuan": tujuan
    }



def rekomendasi_kebugaran(pengguna, hasil_bmi, hasil_aktivitas):

    if (
        pengguna is None
        or hasil_bmi is None
        or hasil_aktivitas is None
    ):
        print("Lakukan analisis aktivitas terlebih dahulu.")
        return []

    tujuan = pengguna["tujuan"]
    frekuensi = pengguna["frekuensi"]
    kategori = hasil_bmi["kategori_bmi"]

    
    jenis = hasil_aktivitas["jenis_rekomendasi"]
    data_olahraga = hasil_aktivitas["hasil_analisis"][jenis]

    set_latihan = data_olahraga["jumlah_set"]
    intensitas = data_olahraga["intensitas"]

    if jenis == "Yoga":
        durasi = "20-30 menit setiap sesi"
        istirahat = "30-60 detik antarset"

    elif jenis == "HIIT":
        durasi = "15-25 menit setiap sesi"
        istirahat = "30-60 detik antarset"

    elif jenis == "Cardio":
        durasi = "30-45 menit setiap sesi"
        istirahat = "2 menit antarset"

    else:
        durasi = "45-60 menit setiap sesi"
        istirahat = "60-90 detik antarset"

    rekomendasi = [
        "Jenis olahraga: " + jenis,
        "Tujuan latihan: " + tujuan,
        "Intensitas berdasarkan dataset: " + intensitas,
        "Durasi latihan: " + durasi,
        "Jumlah set: " + set_latihan,
        "Waktu istirahat: " + istirahat
    ]

    if kategori == "Berat badan kurang":
        rekomendasi.append(
            "Perhatikan pemenuhan nutrisi dan pemulihan tubuh."
        )
    elif kategori == "Normal":
        rekomendasi.append(
            "Pertahankan keseimbangan latihan dan pemulihan."
        )
    elif kategori == "Berat badan berlebih":
        rekomendasi.append(
            "Mulai latihan secara bertahap sesuai kemampuan."
        )
    else:
        rekomendasi.append(
            "Mulai dari intensitas yang sesuai kemampuan tubuh."
        )

    if frekuensi < 3:
        rekomendasi.append(
            "Tingkatkan frekuensi latihan secara bertahap."
        )
    else:
        rekomendasi.append(
            "Pertahankan jadwal latihan dan waktu pemulihan."
        )

    return rekomendasi



def tampilkan_laporan(
    pengguna, hasil_bmi, hasil_kalori,
    hasil_aktivitas, rekomendasi
):
    if pengguna is None or hasil_bmi is None:
        print("Data pengguna belum lengkap.")
        return None

    print("\n===================================")
    print("LAPORAN PERENCANAAN KEBUGARAN")
    print("===================================")

    print("Nama:", pengguna["nama"])
    print("Usia:", pengguna["usia"], "tahun")
    print("Jenis kelamin:", pengguna["gender"])
    print("Berat badan:", pengguna["berat"], "kg")
    print("Tinggi badan:", pengguna["tinggi"], "cm")
    print("Frekuensi olahraga:", pengguna["frekuensi"], "hari/minggu")
    print("Tujuan:", pengguna["tujuan"])

    print("\nHASIL BMI")
    print("BMI:", round(hasil_bmi["bmi"], 2))
    print("Kategori:", hasil_bmi["kategori_bmi"])

    if hasil_kalori is not None:
        print("\nKEBUTUHAN KALORI HARIAN")
        print("Kebutuhan harian:",
              round(hasil_kalori["kebutuhan_harian"], 2), "kkal")
        print("Target kalori:",
              round(hasil_kalori["target_kalori"], 2), "kkal")

    if hasil_aktivitas is not None:
        print("\nJENIS OLAHRAGA BERDASARKAN DATASET:")
        print(hasil_aktivitas["jenis_rekomendasi"])

    print("\nREKOMENDASI KEBUGARAN")
    for saran in rekomendasi:
        print("-", saran)

    jenis = hasil_aktivitas["jenis_rekomendasi"]

    if pengguna["tujuan"] == "Menurunkan":
        target = "Mendukung penurunan berat badan secara bertahap"
    elif pengguna["tujuan"] == "Mempertahankan":
        target = "Mempertahankan berat badan dan kebugaran"
    else:
        target = "Meningkatkan massa dan kekuatan otot"

    kesimpulan = (
        "Pengguna disarankan melakukan olahraga " + jenis +
        " untuk " + target +
        " sebanyak " + str(pengguna["frekuensi"]) +
        " hari per minggu."
    )

    print("\nKESIMPULAN")
    print(kesimpulan)

    laporan = {
        "nama": pengguna["nama"],
        "usia": pengguna["usia"],
        "berat": pengguna["berat"],
        "tinggi_cm": pengguna["tinggi"],
        "tujuan": pengguna["tujuan"],
        "bmi": round(hasil_bmi["bmi"], 2),
        "kategori_bmi": hasil_bmi["kategori_bmi"],
        "kebutuhan_kalori_harian": (
            round(hasil_kalori["kebutuhan_harian"], 2)
            if hasil_kalori is not None else ""
        ),
        "target_kalori": (
            round(hasil_kalori["target_kalori"], 2)
            if hasil_kalori is not None else ""
        ),
        "jenis_olahraga": jenis,
        "kesimpulan": kesimpulan,
        "rekomendasi": "; ".join(rekomendasi)
    }

    return laporan



def simpan_hasil(laporan):
    if laporan is None:
        print("Laporan belum tersedia.")
        return

    nama_output = "hasil_perencanaan_kebugaran.csv"
    file_sudah_ada = os.path.exists(nama_output)

    with open(
        nama_output, mode="a", newline="", encoding="utf-8"
    ) as file:
        penulis = csv.DictWriter(
            file, fieldnames=laporan.keys()
        )

        if not file_sudah_ada:
            penulis.writeheader()

        penulis.writerow(laporan)

    print("Laporan berhasil disimpan ke", nama_output)



def menu_utama():
    data = baca_dataset()

    if len(data) == 0:
        print("Program tidak dapat dijalankan tanpa dataset.")
        return

    data = validasi_data(data)

    if len(data) == 0:
        print("Tidak terdapat data valid untuk dianalisis.")
        return

    
    tampilkan_data(data)

    pengguna = None
    hasil_bmi = None
    hasil_kalori = None
    hasil_aktivitas = None
    rekomendasi = []
    laporan = None

    while True:
        print("\n===================================")
        print("PROGRAM PERENCANAAN KEBUGARAN GYM")
        print("===================================")
        print("1. Input data pengguna")
        print("2. Tampilkan data pengguna")
        print("3. Hitung BMI")
        print("4. Analisis kebutuhan kalori harian")
        print("5. Analisis aktivitas fisik")
        print("6. Rekomendasi kebugaran")
        print("7. Tampilkan laporan")
        print("8. Simpan hasil")
        print("9. Keluar")

        pilihan = input("Pilih menu (1-9): ")

        if pilihan == "1":
            pengguna = input_data_pengguna()
            hasil_bmi = None
            hasil_kalori = None
            hasil_aktivitas = None
            rekomendasi = []
            laporan = None

        elif pilihan == "2":
            if pengguna is None:
                print("Data pengguna belum diinput.")
            else:
                print("\nDATA PENGGUNA")
                for kunci, nilai in pengguna.items():
                    print(kunci, ":", nilai)

        elif pilihan == "3":
            if pengguna is not None:
                hasil_bmi = hitung_bmi(pengguna)
            else:
                print("Input data pengguna terlebih dahulu.")

        elif pilihan == "4":
            if pengguna is not None:
                hasil_kalori = analisis_kalori(data, pengguna)
            else:
                print("Input data pengguna terlebih dahulu.")

        elif pilihan == "5":
            if pengguna is not None:
                hasil_aktivitas = analisis_aktivitas(data, pengguna)
                rekomendasi = []
                laporan = None
            else:
                print("Input data pengguna terlebih dahulu.")

        elif pilihan == "6":
            if pengguna is not None:
                if hasil_bmi is None:
                    hasil_bmi = hitung_bmi(pengguna)

                if hasil_aktivitas is None:
                    hasil_aktivitas = analisis_aktivitas(data, pengguna)

                rekomendasi = rekomendasi_kebugaran(
                    pengguna, hasil_bmi, hasil_aktivitas
                )

                print("\nREKOMENDASI KEBUGARAN")
                for saran in rekomendasi:
                    print("-", saran)

                laporan = None
            else:
                print("Input data pengguna terlebih dahulu.")

        elif pilihan == "7":
            if pengguna is not None:
                if hasil_bmi is None:
                    hasil_bmi = hitung_bmi(pengguna)

                if hasil_kalori is None:
                    hasil_kalori = analisis_kalori(data, pengguna)

                if hasil_aktivitas is None:
                    hasil_aktivitas = analisis_aktivitas(data, pengguna)

                if len(rekomendasi) == 0:
                    rekomendasi = rekomendasi_kebugaran(
                        pengguna, hasil_bmi, hasil_aktivitas
                    )

                laporan = tampilkan_laporan(
                    pengguna,
                    hasil_bmi,
                    hasil_kalori,
                    hasil_aktivitas,
                    rekomendasi
                )
            else:
                print("Input data pengguna terlebih dahulu.")

        elif pilihan == "8":
            if laporan is not None:
                simpan_hasil(laporan)
            else:
                print("Tampilkan laporan terlebih dahulu.")

        elif pilihan == "9":
            print("Terima kasih telah menggunakan program.")
            break

        else:
            print("Pilihan tidak valid. Silakan pilih menu 1-9.")



menu_utama()