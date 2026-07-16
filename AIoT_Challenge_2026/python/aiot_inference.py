import cv2
import numpy as np
import tensorflow as tf
import serial
import time
import json
import os

# Import konfigurasi terpusat
from settings import *

def load_ai_model():
    """Fungsi untuk memuat model CNN dan nama kelas"""
    print(f"[INFO] Memuat model dari {MODEL_PATH}...")
    model = tf.keras.models.load_model(MODEL_PATH)
    
    with open(CLASS_NAMES_PATH, 'r') as f:
        class_names = json.load(f)
        
    print(f"[INFO] Berhasil memuat {len(class_names)} kelas: {class_names}")
    return model, class_names

def init_serial():
    """Membuka komunikasi Serial dengan NodeMCU"""
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2) # Memberikan jeda agar NodeMCU siap setelah koneksi dibuka
        print(f"[INFO] Berhasil terhubung ke NodeMCU di {SERIAL_PORT}")
        return ser
    except Exception as e:
        print(f"[WARNING] Tidak bisa membuka {SERIAL_PORT}. Berjalan dalam mode Simulasi (Tanpa Hardware).")
        print(f"[WARNING] Error Detail: {e}")
        return None

def preprocess_image(frame):
    """Mempersiapkan gambar untuk masuk ke model Keras"""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized_frame = cv2.resize(rgb_frame, IMAGE_SIZE)
    input_tensor = np.expand_dims(resized_frame, axis=0)
    
    # Scaling sesuai dengan yang digunakan saat pelatihan (biasanya 0-1)
    input_tensor = input_tensor.astype("float32") / 255.0 
    return input_tensor

def main():
    model, class_names = load_ai_model()
    ser = init_serial()
    
    # State Change Detection / Debounce Logic
    # (Solusi Profesional untuk mencegah serial buffer penuh - Misi 3)
    last_sent_command = None 
    
    # Buka kamera sesuai konfigurasi di settings.py
    cap = cv2.VideoCapture(CAMERA_ID)
    
    # Atur resolusi agar FPS stabil
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
    print("[INFO] Memulai kamera... Arahkan objek ke kamera. Tekan 'q' untuk keluar.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Gagal membaca dari kamera.")
            break
            
        # 1. Preprocessing & Inferensi
        input_tensor = preprocess_image(frame)
        predictions = model.predict(input_tensor, verbose=0)
        confidence = np.max(predictions[0])
        predicted_idx = np.argmax(predictions[0])
        predicted_class = class_names[predicted_idx]
        
        # 2. Logika Aktuator (Mapping Kelas ke Relay)
        command_to_send = '0' # Default: Semua Relay OFF
        
        # Hanya gunakan hasil prediksi jika confidence melebihi threshold
        if confidence >= CONFIDENCE_THRESHOLD:
            if predicted_class == "freshapples":
                command_to_send = '1'
            elif predicted_class == "freshlemons":
                command_to_send = '2'
            elif predicted_class == "freshoranges":
                command_to_send = '3'
            elif "rotten" in predicted_class:
                # Semua buah busuk akan menyalakan Relay 4
                command_to_send = '4'
                
        # 3. Misi 3: Implementasi State Change Detection (Debounce)
        # Hanya mengirim data ke NodeMCU jika perintah BERUBAH dari sebelumnya.
        if command_to_send != last_sent_command:
            print(f"[AKSI] State Berubah! Mengirim: '{command_to_send}' (Objek: {predicted_class if command_to_send != '0' else 'NONE'}, Conf: {confidence:.2f})")
            
            if ser is not None:
                try:
                    # Kirim karakter (byte) melalui komunikasi Serial USB
                    ser.write(command_to_send.encode())
                except Exception as e:
                    print(f"[ERROR] Gagal mengirim data: {e}")
            
            # Perbarui status terakhir yang dikirim
            last_sent_command = command_to_send

        # 4. Level Silver Bonus: Visualisasi / Dashboard Monitoring lokal
        label = f"{predicted_class} ({confidence:.2f})" if confidence >= CONFIDENCE_THRESHOLD else "Tidak ada objek valid"
        color = (0, 255, 0) if confidence >= CONFIDENCE_THRESHOLD else (0, 0, 255)
        
        # Tampilkan teks pada frame video
        cv2.putText(frame, label, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(frame, f"Instruksi Serial: {command_to_send}", (15, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Tampilkan jendela aplikasi
        cv2.imshow("Smart Environment - AIoT Camera", frame)
        
        # Keluar jika pengguna menekan tombol 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Cleanup Hardware dan Resource
    print("[INFO] Menutup sistem...")
    cap.release()
    cv2.destroyAllWindows()
    if ser is not None:
        ser.write('0'.encode()) # Pastikan semua relay mati sebelum program berakhir
        ser.close()

if __name__ == "__main__":
    main()
