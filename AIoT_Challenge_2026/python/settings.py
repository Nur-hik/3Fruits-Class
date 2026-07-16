# settings.py
# File konfigurasi terpusat untuk proyek AIoT Challenge 2026

# ==========================================
# KONFIGURASI KECERDASAN BUATAN (AI MODEL)
# ==========================================
# Lokasi model Keras (menggunakan relative path dari folder python)
MODEL_PATH = "../../models/mobilenetv2_finetuned_best.keras"

# Lokasi daftar nama kelas (JSON)
CLASS_NAMES_PATH = "../../exports/class_names.json"

# Ambang batas keyakinan (Confidence). 
# Model hanya akan mengirim perintah ke alat jika prediksi lebih besar dari persentase ini.
CONFIDENCE_THRESHOLD = 0.60

# Ukuran input gambar yang dibutuhkan model (Standar MobileNetV2 adalah 224x224)
IMAGE_SIZE = (224, 224)


# ==========================================
# KONFIGURASI HARDWARE (SERIAL & IOT)
# ==========================================
# UBAH tulisan "COM3" di bawah ini dengan port NodeMCU Anda.
# Cara cek: Buka Arduino IDE -> klik menu "Tools" -> lihat bagian "Port".
# Contoh Windows: "COM3", "COM5"
# Contoh Mac/Linux: "/dev/ttyUSB0" atau "/dev/cu.SLAB_USBtoUART"
SERIAL_PORT = "COM3" 

# Kecepatan komunikasi serial (Baudrate). Harus SAMA dengan yang ada di aiot_nodemcu.ino.
BAUD_RATE = 115200


# ==========================================
# KONFIGURASI KAMERA
# ==========================================
# ID Kamera (0 biasanya untuk webcam bawaan laptop, 1 untuk webcam eksternal)
CAMERA_ID = 0

# Resolusi video. Diturunkan menjadi 640x480 agar FPS (Frame Per Second) stabil.
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
