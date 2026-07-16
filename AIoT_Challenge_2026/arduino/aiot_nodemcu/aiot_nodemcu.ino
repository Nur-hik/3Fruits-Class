/*
 * AIoT Challenge 2026: Dari Layar ke Dunia Nyata
 * NodeMCU ESP8266 Code
 * 
 * Fungsi: Menerima perintah dari Python melalui Serial (Kabel USB)
 * dan mengaktifkan Relay yang sesuai dengan objek yang dideteksi (3Fruits-Class).
 * 
 * Mapping Kelas:
 * '1' -> Relay 1 ON (Fresh Apples)
 * '2' -> Relay 2 ON (Fresh Lemons)
 * '3' -> Relay 3 ON (Fresh Oranges)
 * '4' -> Relay 4 ON (Rotten Fruits - Apples, Lemons, Oranges)
 * '0' -> Semua Relay OFF (Tidak ada objek / confidence rendah)
 */

// Mendefinisikan pin Relay pada NodeMCU (ESP8266)
#define RELAY1 D1 // GPIO 5
#define RELAY2 D2 // GPIO 4
#define RELAY3 D5 // GPIO 14
#define RELAY4 D6 // GPIO 12

// Ubah dua nilai ini jika modul relay Anda active-HIGH.
const uint8_t RELAY_ON = LOW;
const uint8_t RELAY_OFF = HIGH;

void setup() {
  // Inisialisasi komunikasi serial pada baudrate 115200
  Serial.begin(115200);
  
  // Set pin relay sebagai output
  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);
  pinMode(RELAY3, OUTPUT);
  pinMode(RELAY4, OUTPUT);

  // Matikan semua relay pada saat startup
  // Catatan: Sebagian besar Modul Relay adalah Active LOW (LOW = ON, HIGH = OFF)
  turnOffAllRelays();
  
  Serial.println("AIoT NodeMCU Siap Menerima Perintah!");
}

void loop() {
  // Mengecek apakah ada data yang masuk di buffer Serial
  if (Serial.available() > 0) {
    // Membaca satu karakter dari Serial
    char command = Serial.read();
    
    // Abaikan karakter newline/enter dari Serial Monitor
    if (command == '\n' || command == '\r') return;

    // Tampilkan perintah yang diterima (opsional untuk debugging)
    // Serial.print("Menerima perintah: ");
    // Serial.println(command);

    // Menjalankan aksi berdasarkan command
    switch (command) {
      case '1':
        turnOffAllRelays(); // Matikan relay lain (debounce prevention)
        digitalWrite(RELAY1, RELAY_ON);
        Serial.println("ACK:1 Fresh Apples");
        break;
      case '2':
        turnOffAllRelays();
        digitalWrite(RELAY2, RELAY_ON);
        Serial.println("ACK:2 Fresh Lemons");
        break;
      case '3':
        turnOffAllRelays();
        digitalWrite(RELAY3, RELAY_ON);
        Serial.println("ACK:3 Fresh Oranges");
        break;
      case '4':
        turnOffAllRelays();
        digitalWrite(RELAY4, RELAY_ON);
        Serial.println("ACK:4 Rotten Fruits");
        break;
      case '0':
        turnOffAllRelays();
        Serial.println("ACK:0 All relays OFF");
        break;
      default:
        // Jangan lakukan apa-apa jika command tidak dikenal
        break;
    }
  }
}

// Fungsi bantuan untuk mematikan semua relay
void turnOffAllRelays() {
  digitalWrite(RELAY1, RELAY_OFF);
  digitalWrite(RELAY2, RELAY_OFF);
  digitalWrite(RELAY3, RELAY_OFF);
  digitalWrite(RELAY4, RELAY_OFF);
}
