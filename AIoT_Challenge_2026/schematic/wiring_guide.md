# Diagram Skematik & Panduan Wiring (AIoT Challenge 2026)

Misi 1 adalah "Engineer Never Skip Wiring". Berikut adalah panduan merakit NodeMCU (ESP8266) dengan Modul Relay 4 Channel dan Lampu LED Indikator.

## Komponen yang Dibutuhkan
1. 1x NodeMCU ESP8266
2. 1x Modul Relay 4-Channel (5V)
3. 4x Lampu LED Kecil (Berbeda warna disarankan, misal Merah, Kuning, Hijau, Biru)
4. 4x Resistor (220 Ohm atau 330 Ohm) untuk keamanan LED
5. Kabel Jumper (Male-to-Female dan Male-to-Male) secukupnya
6. Kabel USB (Micro-USB) untuk menghubungkan Laptop ke NodeMCU
7. 1x Breadboard (Opsional, sangat disarankan)

## Wiring / Tabel Koneksi

### 1. NodeMCU ke Modul Relay 4-Channel
| Pin NodeMCU ESP8266 | Pin Modul Relay | Keterangan |
| :--- | :--- | :--- |
| **VIN** (atau VU / 5V) | **VCC** | Sumber daya 5V untuk Relay |
| **GND** | **GND** | Ground bersama |
| **D1** (GPIO 5) | **IN1** | Sinyal Relay 1 (Fresh Apples) |
| **D2** (GPIO 4) | **IN2** | Sinyal Relay 2 (Fresh Lemons) |
| **D3** (GPIO 0) | **IN3** | Sinyal Relay 3 (Fresh Oranges) |
| **D4** (GPIO 2) | **IN4** | Sinyal Relay 4 (Rotten Fruits) |

> **⚠️ Peringatan:** Pastikan jumper JD-VCC ke VCC terpasang pada modul relay jika menggunakan power yang sama, atau gunakan sumber tegangan eksternal (5V) terpisah pada JD-VCC jika relay bergetar karena kurang daya dari USB.

### 2. Modul Relay ke LED Indikator (Layer Fisik)
Relay berfungsi sebagai saklar mekanik. Kita akan menggunakan sisi **Normally Open (NO)**.
Untuk lampu DC kecil / LED 5V:

1. Hubungkan pin **3V3** NodeMCU (atau sumber 5V jika LED mampu 5V) ke **Kaki Panjang LED (Anoda)** masing-masing LED, TAPI lewati dulu switch Relay.
2. Karena kita ingin Relay yang memutus/menyambung listrik, skema amannya:
   - Sumber 3.3V / 5V NodeMCU  ➡️  Terminal **COM** (Common) di setiap Channel Relay.
   - Terminal **NO** (Normally Open) pada masing-masing Relay ➡️ Resistor (220 Ohm) ➡️ Kaki **Anoda (+)** LED 1, 2, 3, 4.
   - Kaki **Katoda (-)** semua LED ➡️ dihubungkan menjadi satu ke jalur **GND** NodeMCU.

---

## Diagram Alir Logika & Hardware (Mermaid)

Anda dapat menggunakan screenshot dari diagram ini, atau men-generate PDF/PNG dari Markdown viewer yang mendukung Mermaid (misalnya GitHub atau plugin VSCode) sebagai bagian dari deliverable tugas.

```mermaid
graph TD
    %% Digital Brain (Laptop)
    subgraph Laptop [Layer 2: Digital Brain (Python)]
        Webcam[Kamera / Webcam] -->|Video Feed| CNN[Model CNN Keras]
        CNN -->|Objek Dideteksi| PythonScript[aiot_inference.py]
        PythonScript -->|Kirim '1', '2', '3', '4' atau '0'| USB_Port[USB Port Serial]
    end

    %% Communication
    USB_Port -->|Kabel Micro-USB\nBaudrate 115200| NodeMCU_Port[USB NodeMCU]

    %% Physical World (ESP & Actuator)
    subgraph Hardware [Layer 1: Physical World]
        NodeMCU_Port --> MCU[NodeMCU ESP8266]
        
        MCU -->|Pin D1| IN1[Relay IN1]
        MCU -->|Pin D2| IN2[Relay IN2]
        MCU -->|Pin D3| IN3[Relay IN3]
        MCU -->|Pin D4| IN4[Relay IN4]
        
        subgraph ModulRelay [Modul Relay 4-Channel]
            IN1 -.-> R1((Switch R1))
            IN2 -.-> R2((Switch R2))
            IN3 -.-> R3((Switch R3))
            IN4 -.-> R4((Switch R4))
        end
        
        R1 -->|Normally Open| LED1((LED 1 - Apples))
        R2 -->|Normally Open| LED2((LED 2 - Lemons))
        R3 -->|Normally Open| LED3((LED 3 - Oranges))
        R4 -->|Normally Open| LED4((LED 4 - Rotten))
        
        LED1 & LED2 & LED3 & LED4 --> GND[Ground NodeMCU]
    end
```

## Tips Keselamatan (Safety First)
- Sesuai dengan instruksi modul, **DILARANG MENGGUNAKAN PLN 220V**. Cukup gunakan LED kecil atau lampu DC 5V/12V untuk presentasi.
- Jika menggunakan lampu 12V DC, gunakan adaptor 12V terpisah untuk menyuplai COM Relay, jangan mengambil 12V dari NodeMCU. Pastikan GND (Ground) dari sumber 12V dihubungkan ke GND NodeMCU jika menggunakan relay yang non-optocoupler (atau biarkan terpisah jika relay sudah full isolated dengan jumper terlepas).
