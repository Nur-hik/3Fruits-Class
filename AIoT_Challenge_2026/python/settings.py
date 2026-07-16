"""Konfigurasi default untuk demonstrasi kontrol relay berbasis serial."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Model deployment ini sudah menyertakan preprocessing MobileNetV2 (nilai piksel
# RGB 0--255 -> -1--1). Jangan membagi nilai piksel dengan 255 lagi di aplikasi.
MODEL_PATH = PROJECT_ROOT / "exports" / "data_inference_model.h5"
CLASS_NAMES_PATH = PROJECT_ROOT / "exports" / "class_names.json"
IMAGE_SIZE = (224, 224)
CONFIDENCE_THRESHOLD = 0.60

# Perintah satu-karakter yang dipahami sketch NodeMCU.
COMMAND_BY_CLASS = {
    "freshapples": "1",
    "freshlemons": "2",
    "freshoranges": "3",
    "rottenapples": "4",
    "rottenlemons": "4",
    "rottenoranges": "4",
}
OFF_COMMAND = "0"

SERIAL_PORT = "COM3"  # Ganti, atau gunakan opsi CLI --port.
BAUD_RATE = 115200
SERIAL_STARTUP_DELAY_SECONDS = 2.0

CAMERA_ID = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Sebuah prediksi harus konsisten pada beberapa frame sebelum relay berubah.
MIN_STABLE_FRAMES = 3
