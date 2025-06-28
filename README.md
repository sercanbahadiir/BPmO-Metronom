# BPMO - Arduino Metronom Projesi

## Proje Özeti
BPMO, Arduino tabanlı, sesli ve görsel geri bildirimli, uzaktan kontrol edilebilen bir metronom sistemidir. Başlangıç BPM (Beats Per Minute) değeri, artış miktarı, artış periyodu ve artış yönü Python tabanlı kullanıcı arayüzünden ayarlanabilir. Arduino, buzzer ile tıklama sesi üretir, LED ile görsel vuruş bildirimi yapar, LCD ekran ise anlık BPM değerini gösterir. BPM, belirlenen periyotlarda artırılır veya azaltılır ve bu değerler Python arayüzüne anlık iletilir.

## Özellikler

- Başlangıç BPM, artış miktarı, periyot ve artış yönü kullanıcı tarafından kolayca ayarlanabilir
- BPM minimum 40, maksimum 208 arasında sınırlandırılmıştır
- Metronom vuruşlarında LED yanıp söner ve buzzer sesi çıkar
- I2C arayüzlü LCD ekranda anlık BPM değeri gösterilir
- Python Tkinter arayüzü üzerinden metronom başlatılır, durdurulur ve ayarlar gerçek zamanlı güncellenir
- Seri iletişim ile Arduino ve Python arasında çift yönlü veri aktarımı sağlanır

## Kullanılan Donanım ve Bağlantılar

| Bileşen     | Arduino Bağlantısı              | Açıklama                                 |
|-------------|--------------------------------|-----------------------------------------|
| Arduino Uno | -                              | Ana kontrolcü                           |
| Buzzer      | Pin 8 (digital çıkış)           | Sesli metronom tıklaması                |
| LED         | Pin 7 (digital çıkış)           | Metronom vuruşunda yanıp sönme (220Ω direnç ile) |
| Direnç      | 220Ω                           | LED'yi korur                           |
| I2C LCD     | SDA - A4, SCL - A5             | Anlık BPM gösterimi                     |
| GND         | Buzzer, LED, LCD GND ortak     | Topraklama                             |
| 5V          | LCD VCC                        | Güç kaynağı                            |

### Fiziksel Bağlantılar

**Buzzer**
- Arduino Pin 8 → Buzzer +
- Buzzer - → Arduino GND

**LED**
- Arduino Pin 7 → 220Ω direnç → LED uzun bacak (anot)
- LED kısa bacak (katot) → Arduino GND

**LCD I2C**
- Arduino 5V → LCD VCC
- Arduino GND → LCD GND
- Arduino A4 (SDA) → LCD SDA
- Arduino A5 (SCL) → LCD SCL

## Yazılım Detayları

### Arduino Kodu İşleyişi
Arduino Kodu: https://github.com/sercanbahadiir/BPmO-Metronom/blob/main/bpmo_arduino

- `setup()` fonksiyonu: Seri iletişim başlatılır, pinler çıkış olarak ayarlanır, LCD ekran başlatılır ve "Metronom Hazir" mesajı gösterilir.
- `loop()` fonksiyonu:
  - Seri porttan komutlar okunur:
    - `"START"` → Metronom çalışmaya başlar
    - `"STOP"` → Metronom durdurulur
    - `"EXIT"` → Metronom durdurulur ve program sonlandırılmaya hazırlanır
    - Parametreler (bpm, increment, period, direction) gelirse ayarlar güncellenir
  - Metronom aktifse belirlenen BPM'ye göre delay hesaplanır ve buzzer ile LED tetiklenir
  - Belirlenen periyot sonunda BPM, artış yönü ve sınırlar göz önünde bulundurularak artırılır veya azaltılır
  - Anlık BPM LCD'ye yazılır ve seri porttan gönderilir

### Python Arayüzü İşleyişi
Python Kodu:https://github.com/sercanbahadiir/BPmO-Metronom/blob/main/BPmO.py

Tkinter ile oluşturulan arayüz üzerinden kullanıcı:
- Başlangıç BPM
- BPM artış miktarı
- Artış periyodu (kaç vuruşta bir BPM değişecek)
- Artış yönü (artış/azalış) seçimi yapar

"Başlat" düğmesi ile ayarlar Arduino'ya gönderilir ve metronom başlatılır. "Durdur" ile metronom durdurulur. "Bitir" ile program kapatılır. Arduino'dan gelen anlık BPM değerleri arayüzde canlı gösterilir.

## Kullanılan Kütüphaneler

### Arduino

**LiquidCrystal_I2C**
I2C arayüzlü LCD ekran kontrolü için. Kurulum: Arduino IDE > Library Manager > "LiquidCrystal I2C" aratıp yükleyebilirsiniz.

**Wire**
I2C protokolü için. Arduino IDE'ye önceden dahil.

### Python

**pyserial**
Arduino ile seri iletişim için. Kurulum:
```bash
pip install pyserial
```

**Tkinter**
Python standart GUI kütüphanesi. Çoğu Python sürümünde varsayılan olarak gelir.

## Kurulum ve Çalıştırma

### Donanım Kurulumu

1. Yukarıdaki bağlantı şemasına göre Arduino'ya buzzer, LED ve LCD'yi bağlayın
2. Arduino'yu USB ile bilgisayara bağlayın

### Yazılım Kurulumu

1. Arduino IDE'de `arduino_metronom.ino` dosyasını açın ve Arduino'ya yükleyin
2. Bilgisayarınızda Python 3 kurulu olmalı
3. Terminal veya Komut İstemcisinde:
   ```bash
   pip install pyserial
   ```
4. `BPmO.py` dosyasını çalıştırın:
   ```bash
   python BPmO.py
   ```

### Kullanım

1. Python arayüzünden başlangıç BPM, artış miktarı, artış periyodu ve artış yönünü seçin
2. "Başlat" butonuna basın, metronom çalışmaya başlar
3. LED yanıp söner, buzzer vuruşları gelir ve LCD'de BPM gösterilir
4. "Durdur" ile durdurabilir, "Bitir" ile programı kapatabilirsiniz

## Proje Dosyaları

| Dosya                  | Açıklama                     |
| ---------------------- | ---------------------------- |
| `arduino_metronom.ino` | Arduino metronom kaynak kodu |
| `bpm_gui.py`           | Python Tkinter arayüzü       |
| `README.md`            | Proje dokümantasyonu         |

## Geliştirme Fikirleri

- Blynk veya başka IoT platformları ile uzaktan kontrol eklentisi
- Bluetooth veya WiFi üzerinden kablosuz haberleşme
- Metronom ses ayarları (ses yüksekliği, farklı efektler)
- Daha gelişmiş grafik arayüzleri
- Çoklu ritim ve vuruş seçenekleri

Temsili Simülasyon ve Kod Bağlantıları Tinkercad Simülasyon Linki: https://www.tinkercad.com/things/2osEWT5IlJL/editel?returnTo=%2Fdashboard&sharecode=xEbV19hBHN6R44XF8R7WgX9tQ6NPc8N3ULkS6ubnIzE

Proje Videosu Projenin çalışır halde videosunu aşağıdaki bağlantıdan izleyebilirsiniz: https://youtu.be/oeic6eT6llk

