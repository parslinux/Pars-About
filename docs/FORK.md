# Pars About — Fork ve Geliştirme Notları (FORK.md)

Bu belge, **Pars About** projesinin kökenini, Pardus ekosisteminden çatallanma (fork) sürecini, gerçekleştirilen mimari ve görsel iyileştirmeleri açıklar.

---

## 1. Projenin Kökeni ve Çatallanma Amacı

Pars About, TÜBİTAK ULAKBİM tarafından Pardus GNU/Linux dağıtımı için geliştirilen `pardus-about` projesi temel alınarak **Pars Linux** ekosistemi için çatallanmıştır.

Çatallanmanın temel hedefleri:
1. **Pars Linux Kimliği ve Entegrasyonu**: Uygulamanın Pars Linux masaüstü deneyimiyle tam uyumlu hale getirilmesi.
2. **Modern Görsel Standartlar**: Vektörel, yüksek çözünürlüklü ve özgün SVG cihaz ikonları ile zenginleştirilmiş arayüz.
3. **Masaüstü ve Donanım Uyumluluğu**: Farklı masaüstü ortamlarında (XFCE, GNOME, KDE Plasma vb.) pencere ölçekleme, GTK temaları ve donanım algılama yeteneklerinin iyileştirilmesi.
4. **Gelişmiş Uçbirim ve Teftiş Desteği**: Grafik arayüze ihtiyaç duymadan sunucu ve otomasyon ortamlarında donanım raporu alabilen CLI yeteneklerinin güçlendirilmesi.

---

## 2. Gerçekleştirilen Başlıca Değişiklikler ve İyileştirmeler

### A. Uygulama Kimliği ve Yol Yeniden Yapılandırması (Rebranding)
* **Uygulama ID**: `org.parslinux.about` olarak güncellendi.
* **İkili Dosya**: `pars-about` komut adı ile `/usr/bin/pars-about` yoluna yerleştirildi.
* **Veri Yolu**: Kaynak dosyalar ve varlıklar `/usr/share/pars/pars-about/` dizinine taşındı.
* **Masaüstü Dosyaları**:
  - `org.parslinux.about.desktop` (Sistem Özeti & Hakkında)
  - `org.parslinux.about-hardware.desktop` (Donanım Bilgisi doğrudan başlatıcı)
* **Kategori ve XDG Standartları**: Pars Linux masaüstü ayarlarıyla uyumlu `X-Pars-Apps` kategorisi tanımlandı.

### B. Özgün Vektörel İkon Seti (SVG Art Asset Overhaul)
Proje için her bir donanım kategorisine özel, modern ve ölçeklenebilir Pars Linux SVG ikonları hazırlandı ve `data/icons/` altına entegre edildi:
* `pars-about-main.svg`, `pars-about-computer.svg`, `pars-about-desktop.svg`
* `pars-about-processor.svg` (CPU)
* `pars-about-memory.svg` (RAM)
* `pars-about-graphics.svg` (GPU)
* `pars-about-storage.svg` (Diskler ve Depolama)
* `pars-about-monitor.svg` (Ekran ve Monitör)
* `pars-about-network-card.svg`, `pars-about-ethernet.svg`, `pars-about-wifi.svg`, `pars-about-publicip.svg` (Ağ Bileşenleri)
* `pars-about-audio.svg` (Ses Kartları ve Giriş-Çıkışlar)
* `pars-about-bluetooth.svg` (Bluetooth Aygıtları)
* `pars-about-camera.svg` (Webcam ve Kameralar)
* `pars-about-keyboard.svg`, `pars-about-mouse.svg`, `pars-about-touchpad.svg` (Giriş Cihazları)
* `pars-about-printer.svg` (Yazıcılar)
* `pars-about-bios.svg` (Anakart & BIOS/UEFI)
* `pars-about-fingerprint.svg` (Biyometrik Parmak İzi Okuyucuları)
* `pars-hardware-info.svg` & `pars-about-symbolic.svg`

### C. Arayüz ve Ölçekleme İyileştirmeleri
* **Pencere Boyutlandırma**: Küçük ekranlı cihazlarda ve yüksek DPI (HiDPI) ekranlarda yaşanan taşma ve donma sorunları giderildi.
* **CSS İyileştirmeleri**: `css/main.css` dosyası modern GTK+ 3 seçicileri ve Pars teması renk paletiyle zenginleştirildi.
* **Özet Kartları**: Donanım özet kutucuklarının (`HardwareGridCell`) hizalama ve simge boşlukları dengelendi.

### D. Headless CLI (`--json` / `-j`) Bağımsızlığı
* `--json` argümanı çalıştırıldığında X11/Wayland ekran sunucusu arama zorunluluğu ortadan kaldırıldı; sunucu ve konteyner ortamlarında doğrudan stdout'a saf JSON basacak şekilde yalıtıldı.

### E. Yetkilendirme ve PolicyKit Güncellemesi
* PolicyKit yetki kuralı `org.parslinux.pkexec.pars-about.policy` ve kural dosyası `org.parslinux.about.rules` olarak Pars Linux standartlarına geçirildi.
* Sistem adı değiştirme (`hostname`) ve sistem teşhis arşivi oluşturma eylemleri bu kural üzerinden güvenli hale getirildi.

### F. Çeviri ve Yerelleştirme Altyapısı
* Çeviri alan adı `pars-about` olarak güncellendi.
* `update-translations.sh` ve `fix-po.sh` betikleri optimize edildi; Türkçe (`tr`), Portekizce (`pt`) ve İspanyolca (`es`) dil dosyaları güncellendi.
