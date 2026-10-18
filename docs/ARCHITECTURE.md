# Pars About Mimarisi (ARCHITECTURE.md)

Bu belge, **Pars About** (`org.parslinux.about`) sistem ve donanım bilgilendirme aracının iç mimarisini, veri toplama mekanizmalarını, GUI ve CLI katmanlarını ile yetkilendirme (PolicyKit) modelini detaylandırır.

---

## 1. Genel Mimari Bakış

Pars About, GNU/Linux sistemlerde donanım ve işletim sistemi bilgilerini derinlemesine tarayarak hem kullanıcı dostu modern bir GTK+ 3 arayüzünde sunan, hem de uçbirim üzerinden JSON formatında teftiş imkanı sağlayan iki katmanlı bir mimariye sahiptir.

```
+-----------------------------------------------------------------------------------+
|                        Kullanıcı Arayüzü / Giriş Katmanı                          |
|                                                                                   |
|  +-------------------------------------+   +-----------------------------------+  |
|  |           pars-about.py             |   |        pars-about --json          |  |
|  |     (GTK+ 3 GUI / GtkApplication)   |   |     (Headless CLI / JSON Çıktı)   |  |
|  +-------------------------------------+   +-----------------------------------+  |
|                   |                                          |                    |
+-------------------|------------------------------------------|--------------------+
                    v                                          v
+-----------------------------------------------------------------------------------+
|                         Arayüz ve Görselleştirme Katmanı                           |
|  - MainWindow.py (Arayüz Denetleyicisi, Sayfa Değişimleri, Olay Yönetimi)         |
|  - ui/MainWindow.glade (GTK Builder Arayüz Tanımı)                                |
|  - css/main.css (Özel Stil ve Tema Kuralları)                                     |
|  - widget/HardwareDetailRow.py (Kategori bazlı donanım detay satırları)           |
|  - widget/HardwareGridCell.py (Donanım özet kartları ve ızgara bileşenleri)       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                     Sistem & Donanım Yöneticileri (src/util)                      |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                 ComputerManager.py (Merkezi Veri Toplayıcı)                 |  |
|  +-----------------------------------------------------------------------------+  |
|       |              |             |              |             |            |    |
|       v              v             v              v             v            v    |
|  +----------+  +-----------+  +----------+  +-----------+  +---------+  +------+  |
|  | OSManager|  |PCIManager |  |USBManager|  |DiskManager|  |Monitor- |  |edid. |  |
|  |desktop.py|  |           |  |          |  |           |  |Manager  |  |py    |  |
|  +----------+  +-----------+  +----------+  +-----------+  +---------+  +------+  |
|       |              |             |              |             |            |    |
|       v              v             v              v             v            v    |
|  +----------+  +-----------+  +----------+  +-----------+  +---------+  +------+  |
|  |network.py|  |Printer-   |  |Serio-    |  |ACPI-      |  |DualBoot-|  |Host- |  |
|  |          |  |Manager    |  |Manager   |  |Manager    |  |Manager  |  |name- |  |
|  +----------+  +-----------+  +----------+  +-----------+  +---------+  +------+  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                     Yetkilendirme ve Sistem Eylemleri (Polkit)                    |
|  - Actions.py (Ayrıcalıklı eylemler: ACPI kontrolü, Dual Boot taraması)           |
|  - ActionsAsk.py / SystemReportManager.py (Kök günlükleri & Teşhis arşivi)        |
|  - org.parslinux.pkexec.pars-about.policy (PolicyKit yetki tanımları)             |
|  - org.parslinux.about.rules (Yetki kuralları ve istisnalar)                       |
+-----------------------------------------------------------------------------------+
```

---

## 2. Katmanlar ve Bileşen Sorumlulukları

### A. Giriş Noktaları (Entry Points)
* **`pars-about.py`**: Yürütülebilir sembolik bağ ve başlatıcı. Yerel geliştirme ortamında `src/` dizinini, kurulu sistemde `/usr/share/pars/pars-about/src` dizinini Python arama yoluna (`sys.path`) ekler ve `Main.py`'yi başlatır.
* **`src/Main.py`**: `Gtk.Application` tabanlı ana yürütücü. `application_id="org.parslinux.about"` kimliği ile tekil oturum (single-instance) denetimi yapar.
  - `--json` veya `-j` parametresi verildiğinde grafik arayüz döngüsünü başlatmaz; doğrudan `ComputerManager.get_all_device_info()` çalıştırarak JSON çıktısını standart çıktıya (stdout) basar ve `0` koduyla çıkar.
  - `--hardware` veya `-h` argümanı verildiğinde doğrudan donanım ayrıntıları sekmesini açar.

### B. Arayüz Katmanı (UI Layer)
* **`src/MainWindow.py`**: GTK+ 3 penceresinin tüm sinyal bağlantılarını, dinamik içerik güncellemelerini, sol kategori menüsü geçişlerini ve kullanıcı etkileşimlerini yöneten çekirdek sınıftır.
* **`ui/MainWindow.glade`**: Arayüz tasarımının XML şablonudur.
* **`src/widget/HardwareGridCell.py`**: Özet sayfadaki işlemci, bellek, disk, ekran kartı ve ana kart gibi temel bileşenlerin kart tasarımını sağlar.
* **`src/widget/HardwareDetailRow.py`**: Detay sayfasındaki cihaz özelliklerini (üretici, model, seri numarası, sürücü, veri yolu) standart satır formatında çizer.

### C. Donanım ve Sistem Algılama Katmanı (`src/util/`)

Bu katman, çekirdek (`/sys`, `/proc`, `/dev`) ve sistem araçlarından ham bilgileri toplayıp temiz bir veri sözlüğüne dönüştürür:

| Modül | Sorumluluk Alanı | Veri Kaynağı |
|:---|:---|:---|
| **`ComputerManager.py`** | Tüm alt modülleri koordine eden ana toplayıcı ve JSON üretici | Alt yöneticilerin birleşimi |
| **`OSManager.py` & `desktop.py`** | Dağıtım adı, sürüm, kod adı, masaüstü ortamı (XFCE, GNOME, KDE vb.) | `/etc/os-release`, `lsb_release`, `XDG_CURRENT_DESKTOP` |
| **`PCIManager.py`** | PCI veriyolu cihazları (GPU, ses yongaları, köprüler, denetleyiciler) | `lspci`, `/sys/bus/pci` |
| **`USBManager.py`** | Bağlı USB cihazları ağacı, üretici ve ürün kimlikleri (VID/PID) | `lsusb`, `/sys/bus/usb` |
| **`DiskManager.py`** | Depolama aygıtları (NVMe, SSD, HDD), bölüntüler, dosya sistemleri, doluluk | `lsblk`, `df`, `blkid` |
| **`MonitorManager.py` & `edid.py`** | Ekranlar, çözünürlükler, yenileme hızı, en-boy oranı ve EDID ikili çözümü | `/sys/class/drm/*/edid`, `xrandr` |
| **`network.py`** | Ağ arayüzleri (Ethernet, Wi-Fi), MAC adresi, yerel IP ve genel IP | `ip addr`, `/sys/class/net`, `nmcli` |
| **`PrinterManager.py`** | Sisteme bağlı veya ağdaki yazıcılar ve durumları | `CUPS` API (`pycups`) |
| **`SerioManager.py`** | PS/2, Seri ve tümleşik giriş aygıtları (Klavye, Fare, Touchpad) | `/sys/bus/serio`, `/proc/bus/input/devices` |
| **`ACPIManager.py`** | ACPI güç durumu, pil doluluğu, sağlık durumu, şarj döngüsü | `/sys/class/power_supply` |
| **`DualBootManager.py`** | Sistemde kurulu diğer işletim sistemlerini tespit etme | `os-prober`, EFI boot girişleri |
| **`HostnameManager.py`** | Bilgisayar adını okuma ve değiştirme | `systemd-hostnamed`, DBus, `/etc/hostname` |
| **`SystemReportManager.py`** | Teşhis ve destek raporu oluşturma (`.tar.gz`), logları derleme | Sistem günlükleri, donanım JSON dökümü |

---

## 3. Yetkilendirme ve Güvenlik Ayrımı (Privilege Separation)

Pars About, en az yetki (least privilege) ilkesine sıkı sıkıya bağlıdır:

1. **Ayrıcalıksız GUI**: Grafik arayüz ve standart donanım okuma rutinleri kesinlikle kök (`root`) yetkisi gerektirmez. Standart kullanıcı yetkisiyle `/sys` ve `/proc` üzerinden salt okunur veri çeker.
2. **Korumalı Eylemler (`pkexec`)**:
   - Sistem bilgisayar adını (`hostname`) değiştirme
   - Çift önyükleme (Dual Boot) için diğer disk bölüntülerini ve EFI tablolarını tarama
   - `/var/log` altındaki korumalı sistem günlüklerini içeren tam teşhis raporunu `/tmp/pars_system_report/` dizinine derleme
3. **PolicyKit Entegrasyonu**: Korumalı eylemler yalnızca `/usr/share/polkit-1/actions/org.parslinux.pkexec.pars-about.policy` dosyası aracılığıyla yetkili kullanıcılara şifre sorarak izin verir.

---

## 4. Bağımlılık ve Paketleme Akışı

* **Yapılandırma Sistemi**: Meson (`meson.build`) ve Ninja derleme motoru.
* **Yerelleştirme**: GNU gettext (`po/` dizini altında `.pot` ve `.po` dosyaları).
* **Varlıklar (Assets)**: Ölçeklenebilir vektörel Pars Linux SVG simgeleri (`data/icons/` ve `/usr/share/icons/hicolor/scalable/`).
