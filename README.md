# 🚀 AIoT Challenge 2026: Dari Layar ke Dunia Nyata

Selamat datang di repositori proyek AIoT (Artificial Intelligence of Things) yang mengintegrasikan model Deep Learning (CNN) dengan perangkat keras dunia nyata menggunakan NodeMCU dan Relay.

## 📌 Deskripsi Proyek
Proyek ini dirancang untuk mendeteksi kesegaran objek (buah) menggunakan kamera secara real-time, lalu memberikan perintah secara langsung (Direct Control) kepada *microcontroller* melalui Serial Communication. 

Sistem bertindak sebagai "Smart Quality Control" sederhana:
- **Digital Brain**: Python + TensorFlow Keras (MobileNetV2) memproses gambar dari kamera untuk mendeteksi kelas buah.
- **Physical Muscle**: NodeMCU ESP8266 + Relay Module menerima sinyal dari Python untuk menghidupkan indikator (Lampu LED) sesuai dengan jenis/kesegaran objek yang dideteksi.

## 📂 Struktur Repositori

```text
📦 3Fruits-Class
 ┣ 📂 AIoT_Challenge_2026
 ┃ ┣ 📂 arduino
 ┃ ┃ ┗ 📂 aiot_nodemcu
 ┃ ┃   ┗ 📜 aiot_nodemcu.ino      # Kode C++ untuk NodeMCU ESP8266
 ┃ ┣ 📂 python
 ┃ ┃ ┣ 📜 aiot_inference.py       # Script inferensi CNN & Serial Comm
 ┃ ┃ ┗ 📜 aiot_core.py            # Logika mapping + debounce yang dapat diuji
 ┃ ┗ 📂 schematic
 ┃   ┣ 📜 wiring_guide.md         # Panduan perakitan hardware
 ┃   ┣ 📜 wiring_diagram.svg      # Diagram skematik yang dapat diedit
 ┃   ┗ 📜 wiring_diagram.pdf      # Diagram siap dikumpulkan/dicetak
 ┣ 📂 exports                       # File export seperti class_names.json
 ┣ 📂 models                        # Model AI tersimpan (.keras)
 ┣ 📜 .gitattributes                # Pengaturan LFS untuk file model besar
 ┣ 📜 .gitignore                    # Mengabaikan file venv dan temporary
 ┣ 📜 README.md                     # File dokumentasi ini
 ┗ 📜 requirements.txt              # Daftar dependensi Python
```

## ✨ Fitur Unggulan
- **Real-time Inference**: Menggunakan OpenCV untuk menangkap frame dan CNN untuk klasifikasi.
- **Direct Serial Control**: Latensi sangat rendah tanpa membutuhkan koneksi internet.
- **State Change Detection (Debounce Logic)**: Script Python hanya mengirimkan sinyal ke hardware *jika ada perubahan* status kelas objek (menghindari spam ke memori buffer NodeMCU).
- **Multi-Class Actuation**: Mendukung 4 Relay terpisah berdasarkan 4 kategori deteksi objek yang berbeda.

## 🛠️ Hardware yang Dibutuhkan
1. NodeMCU ESP8266 / ESP32
2. Modul Relay 4-Channel (5V)
3. Kabel Jumper secukupnya
4. Lampu LED / Indikator DC & Resistor (220/330 ohm)
5. Kamera / Webcam
6. Kabel Micro-USB untuk komunikasi Serial

> ⚠️ **Catatan Keamanan:** Gunakan beban DC bertegangan rendah (seperti LED 5V) untuk demonstrasi. Dilarang bereksperimen dengan listrik PLN (220V AC) tanpa pengawasan profesional.

## 🚀 Cara Menjalankan

### 1. Persiapan Environment Python
Pastikan Python sudah terinstal di komputer Anda, lalu buat *virtual environment* dan instal semua dependensinya:
```bash
python -m venv .venv

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# Aktivasi di Windows:
.\.venv\Scripts\Activate.ps1
# Aktivasi di Mac/Linux:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Setup NodeMCU (Hardware)
1. Rangkai perangkat keras sesuai panduan di `AIoT_Challenge_2026/schematic/wiring_guide.md`.
2. Buka `aiot_nodemcu.ino` menggunakan Arduino IDE.
3. Hubungkan NodeMCU ke laptop, pilih Port yang sesuai.
4. Klik **Upload**. (Pastikan Anda menutup *Serial Monitor* Arduino IDE setelah selesai mencoba).

### 3. Menjalankan AI Inference
1. Pastikan model LFS tersedia. Jika file model baru berupa pointer kecil, jalankan `git lfs pull` dari root repository.
2. Jalankan script dan berikan port NodeMCU (lebih aman daripada mengubah kode):
```bash
cd AIoT_Challenge_2026/python
python aiot_inference.py --port COM3
```
   Contoh Linux: `python aiot_inference.py --port /dev/ttyUSB0`.
3. Untuk uji kamera tanpa hardware, gunakan `python aiot_inference.py --simulation`.
4. Arahkan buah ke kamera dan saksikan Relay bekerja merespons kecerdasan buatan Anda! 🎉

### Protokol dan keandalan kontrol

Python mengirimkan satu perintah ASCII per baris: `1` apel segar, `2` lemon segar, `3` jeruk segar, `4` semua buah busuk, dan `0` untuk mematikan seluruh relay. Sketch mengirim pesan `ACK` yang dapat dibaca di Serial Monitor pada 115200 baud.

Prediksi hanya digunakan pada confidence **≥ 60%**. Selain *state-change detection*, aplikasi menunggu tiga frame yang sama secara berturut-turut sebelum mengubah relay. Jadi, fluktuasi satu frame tidak memicu relay dan perintah yang sama tidak membanjiri buffer serial. Saat aplikasi berhenti, perintah `0` selalu dikirim sebagai *fail-safe*.

Model deployment `exports/data_inference_model.h5` sudah memuat preprocessing MobileNetV2 di dalam graph model. Frame kamera dikirim sebagai RGB dengan rentang 0–255; aplikasi **tidak** melakukan normalisasi `/255` kedua kali.

### Verifikasi tanpa perangkat

Uji logika mapping confidence dan debounce tidak membutuhkan TensorFlow, kamera, maupun NodeMCU:

```bash
cd AIoT_Challenge_2026/python
python -m unittest -v test_aiot_core.py
```

## 📜 Lisensi
Proyek ini dibuat sebagai bagian dari AIoT Challenge 2026.
