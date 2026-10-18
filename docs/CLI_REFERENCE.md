# Pars About — Uçbirim (CLI) Referansı (CLI_REFERENCE.md)

`pars-about`, modern GTK+ 3 grafiksel arayüzünün yanı sıra, sistem yöneticileri, kurumsal envanter otomasyonları ve uzaktan yönetim ihtiyaçları için güçlü bir komut satırı (CLI) arayüzüne sahiptir.

---

## 1. Temel Komut Sözdizimi

```bash
pars-about [SEÇENEKLER]
```

### Desteklenen Parametreler

| Parametre | Kısa Yol | Açıklama |
|:---|:---|:---|
| `--help` | `-?` | Komut satırı seçeneklerini ve yardım metnini görüntüler. |
| `--hardware` | `-h` | Uygulamayı doğrudan ayrıntılı **Donanım Bilgisi** sekmesi açık olarak başlatır. |
| `--json` | `-j` | Grafik arayüzü açmadan, tüm donanım ve sistem verilerini standart çıktıya (**stdout**) saf JSON formatında basar ve sonlanır. |

---

## 2. Headless CLI ve JSON Rapor Modu (`--json` / `-j`)

`--json` parametresi verildiğinde:
* Grafik sunucusu (**X11** veya **Wayland**) bağlantısı aranmaz; `DISPLAY` değişkeni olmadan (saf SSH oturumunda, sunucularda veya konteynerlerde) sorunsuz çalışır.
* `ComputerManager.get_all_device_info()` modülü tetiklenir ve standart çıktıya tam hiyerarşik JSON üretilir.
* Başarılı tamamlanmada çıkış kodu (exit code) `0` döner.

### 2.1. Standart JSON Çıktısı Alma
```bash
pars-about --json
```

### 2.2. JSON Verisini Dosyaya Kaydetme
```bash
pars-about -j > /tmp/sistem_raporu.json
```

### 2.3. `jq` ile Otomasyon ve Filtreleme Örnekleri

Sistem envanteri veya betik kontrollerinde belirli donanım bilgilerini hızlıca çekmek için `jq` aracıyla birlikte kullanılabilir:

**İşlemci Modelini Öğrenme:**
```bash
pars-about -j | jq -r '.processor.model'
```

**Toplam ve Boş Bellek (RAM) Bilgisi:**
```bash
pars-about -j | jq '{Toplam: .memory.total, Bos: .memory.free}'
```

**Ekran Kartı (GPU) ve Sürücü Bilgisi:**
```bash
pars-about -j | jq '.graphics[] | {Model: .device, Surucu: .driver}'
```

**Bağlı Diskler ve Boyutları:**
```bash
pars-about -j | jq '.storage[] | {Disk: .model, Boyut: .size, Tip: .type}'
```

**Ağ Arayüzleri ve IP Adresleri:**
```bash
pars-about -j | jq '.network[] | {Arayuz: .interface, IP: .ip_address, MAC: .mac_address}'
```

---

## 3. Donanım Ayrıntıları Modu (`--hardware` / `-h`)

Kullanıcı doğrudan donanım teftişi yapmak istediğinde genel sistem özet ekranını atlayarak doğrudan sol menüdeki donanım ağacını açar:

```bash
pars-about --hardware
```

Masaüstü ortamlarında bu komut `org.parslinux.about-hardware.desktop` kısayolu ile menüdeki **"Pars Donanım Bilgisi"** girdisi tarafından çağrılır.

---

## 4. PolicyKit Ayrıcalıklı Eylemleri (`Actions.py` & `ActionsAsk.py`)

Kök yetkisi gerektiren hassas işlemler `pkexec` aracılığıyla arka planda yürütülür:

### 4.1. ACPI Desteği Kontrolü
```bash
pkexec /usr/share/pars/pars-about/src/Actions.py acpi
# Çıkış: 0 (Destekleniyor), 1 (Desteklenmiyor)
```

### 4.2. Dual Boot / Çift Önyükleme Algılama
```bash
pkexec /usr/share/pars/pars-about/src/Actions.py dualboot
# Çıktı: Sistemdeki diğer işletim sistemlerinin listesi
```

### 4.3. Tam Teşhis Arşivi Üretme
```bash
pkexec /usr/share/pars/pars-about/src/ActionsAsk.py report
# Sistem günlüklerini (/var/log), çekirdek mesajlarını (dmesg) ve sistem konfigürasyonlarını
# /tmp/pars_system_report altına derler.
```
