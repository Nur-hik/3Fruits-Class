"""Inferensi kamera real-time dan kontrol relay NodeMCU melalui USB serial."""

import argparse
import json
import time
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import serial
import tensorflow as tf

from aiot_core import CommandStabilizer, command_for_prediction
from settings import (
    BAUD_RATE, CAMERA_HEIGHT, CAMERA_ID, CAMERA_WIDTH, CLASS_NAMES_PATH,
    COMMAND_BY_CLASS, CONFIDENCE_THRESHOLD, IMAGE_SIZE, MIN_STABLE_FRAMES,
    MODEL_PATH, OFF_COMMAND, SERIAL_PORT, SERIAL_STARTUP_DELAY_SECONDS,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default=SERIAL_PORT, help="Port NodeMCU, mis. COM3 atau /dev/ttyUSB0")
    parser.add_argument("--baud-rate", type=int, default=BAUD_RATE)
    parser.add_argument("--camera", type=int, default=CAMERA_ID)
    parser.add_argument("--threshold", type=float, default=CONFIDENCE_THRESHOLD)
    parser.add_argument("--min-stable-frames", type=int, default=MIN_STABLE_FRAMES)
    parser.add_argument("--simulation", action="store_true", help="Tidak membuka port serial; tampilkan perintah saja")
    parser.add_argument("--no-display", action="store_true", help="Jalankan tanpa jendela OpenCV (tekan Ctrl+C untuk berhenti)")
    args = parser.parse_args()
    if not 0.0 <= args.threshold <= 1.0:
        parser.error("--threshold harus berada antara 0 dan 1")
    if args.min_stable_frames < 1:
        parser.error("--min-stable-frames harus minimal 1")
    return args


def ensure_model_file(path: Path) -> None:
    """Berikan pesan yang jelas jika file model Git LFS belum diunduh."""
    if not path.is_file():
        raise FileNotFoundError(f"Model tidak ditemukan: {path}")
    if path.read_bytes()[:40].startswith(b"version https://git-lfs.github.com/spec"):
        raise RuntimeError("Model masih berupa pointer Git LFS. Jalankan: git lfs pull")


def load_ai_model():
    ensure_model_file(MODEL_PATH)
    print(f"[INFO] Memuat model: {MODEL_PATH}")
    model = tf.keras.models.load_model(MODEL_PATH)
    with CLASS_NAMES_PATH.open(encoding="utf-8") as file:
        class_names = json.load(file)
    if model.output_shape[-1] != len(class_names):
        raise ValueError("Jumlah output model tidak sama dengan class_names.json")
    print(f"[INFO] Kelas ({len(class_names)}): {', '.join(class_names)}")
    return model, class_names


def init_serial(port: str, baud_rate: int, simulation: bool) -> Optional[serial.Serial]:
    if simulation:
        print("[INFO] Mode simulasi aktif: perintah serial tidak dikirim.")
        return None
    try:
        connection = serial.Serial(port, baud_rate, timeout=1, write_timeout=1)
        time.sleep(SERIAL_STARTUP_DELAY_SECONDS)
        connection.reset_input_buffer()
        print(f"[INFO] NodeMCU terhubung pada {port} @ {baud_rate} baud.")
        return connection
    except serial.SerialException as error:
        raise RuntimeError(f"Tidak dapat membuka port {port}: {error}") from error


def preprocess_image(frame: np.ndarray) -> np.ndarray:
    """Siapkan RGB uint8; model deployment melakukan preprocessing internal."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized_frame = cv2.resize(rgb_frame, IMAGE_SIZE, interpolation=cv2.INTER_AREA)
    return np.expand_dims(resized_frame.astype(np.float32), axis=0)


def send_command(connection: Optional[serial.Serial], command: str) -> None:
    """Kirim satu command per baris agar protokol serial mudah dilacak."""
    if connection is not None:
        connection.write(f"{command}\n".encode("ascii"))
        connection.flush()


def main() -> None:
    args = parse_args()
    model, class_names = load_ai_model()
    connection = init_serial(args.port, args.baud_rate, args.simulation)
    camera = cv2.VideoCapture(args.camera)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    if not camera.isOpened():
        if connection is not None:
            connection.close()
        raise RuntimeError(f"Kamera {args.camera} tidak dapat dibuka")

    stabilizer = CommandStabilizer(args.min_stable_frames)
    print("[INFO] Kamera aktif. Tekan q untuk keluar.")
    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                raise RuntimeError("Gagal membaca frame dari kamera")
            probabilities = model.predict(preprocess_image(frame), verbose=0)[0]
            index = int(np.argmax(probabilities))
            confidence = float(probabilities[index])
            predicted_class = class_names[index]
            requested_command = command_for_prediction(
                predicted_class, confidence, args.threshold, COMMAND_BY_CLASS, OFF_COMMAND
            )
            changed_command = stabilizer.update(requested_command)
            if changed_command is not None:
                send_command(connection, changed_command)
                status = predicted_class if changed_command != OFF_COMMAND else "TIDAK VALID"
                print(f"[AKSI] {changed_command} | {status} | confidence={confidence:.1%}")

            valid = requested_command != OFF_COMMAND
            label = f"{predicted_class}: {confidence:.1%}" if valid else f"Tidak valid: {confidence:.1%}"
            color = (0, 220, 0) if valid else (0, 0, 230)
            cv2.putText(frame, label, (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
            cv2.putText(frame, f"Relay command: {requested_command} | stabil: {stabilizer.stable_command or '-'}", (16, 64), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
            if not args.no_display:
                cv2.imshow("AIoT Smart Fruit Quality Control", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    except KeyboardInterrupt:
        print("\n[INFO] Dihentikan pengguna.")
    finally:
        # Fail-safe: relay pasti OFF ketika aplikasi berakhir normal atau error.
        try:
            send_command(connection, OFF_COMMAND)
        finally:
            camera.release()
            cv2.destroyAllWindows()
            if connection is not None:
                connection.close()
            print("[INFO] Sistem ditutup; semua relay dimatikan.")


if __name__ == "__main__":
    main()
