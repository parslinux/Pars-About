# Değişiklik Günlüğü (CHANGELOG.md)

Bu dosya, **Pars About** projesinin tüm sürüm geçmişini, yapılan iyileştirmeleri, hata düzeltmelerini ve Pars Linux çatallanma (fork) adımlarını belgeler.

Format [Keep a Changelog](https://keepachangelog.com/tr/1.0.0/) standardını ve [Semantic Versioning](https://semver.org/lang/tr/) kurallarını esas alır.

---

## [0.1.0-alpha] - 2026-10-09 (Pars Linux Dönüşümü)

### Eklendi (Added)
* **Pars Linux Görsel Kimliği**: Tüm donanım kategorileri için özgün, modern ve ölçeklenebilir Pars Linux SVG simgeleri eklendi (`data/icons/`):
  - CPU, GPU, Bellek, Depolama, Monitör, Ses, Ağ, Wi-Fi, Ethernet, Bluetooth, Kamera, Biyometri, Giriş Aygıtları, Anakart/BIOS, Genel IP.
* **Headless `--json` / `-j` Desteği**: X11 veya Wayland grafik sunucusu bulunmayan sunucu ve uçbirim oturumlarında saf JSON donanım dökümü alma yeteneği tam bağımsızlaştırıldı.
* **XDG Masaüstü Kısayolları**: `org.parslinux.about.desktop` ve `org.parslinux.about-hardware.desktop` dosyaları güncellendi (`X-Pars-Apps` kategorisi entegre edildi).
* **PolicyKit Kural ve Eylemleri**: `org.parslinux.pkexec.pars-about.policy` ve `org.parslinux.about.rules` dosyaları Pars Linux ad alanına uyarlandı.
* **Kapsamlı Dokümantasyon Seti**: Mimari, Fork, CLI, Test, Kurulum, Güvenlik, Flatpak ve Dağıtım kılavuzları `docs/` altında yapılandırıldı.

### Değiştirildi (Changed)
* Uygulama kimliği `org.parslinux.about` olarak güncellendi.
* Çalıştırılabilir ikili komut `pars-about` olarak adlandırıldı.
* Kaynak kod arama yolları ve yükleme dizinleri `/usr/share/pars/pars-about/` olarak standardize edildi.
* Arayüz ölçekleme mantığı iyileştirildi; küçük ekranlarda ve yüksek çözünürlüklü ekranlarda (HiDPI) pencere yeniden boyutlandırma sorunları çözüldü.
* CSS tema tanımları modern GTK 3 kurallarıyla yenilendi.

---

## [1.2.6] - Pardus Tabanı

### Düzeltildi (Fixed)
* Birleşik ve çoklu `XDG_CURRENT_DESKTOP` değerlerinden masaüstü ortamı sürümünü çözümleme hatası giderildi.
* Rapor kopyalama bildirim açılır penceresinde (`popover`) oluşan kilitlenme giderildi; `GtkRevealer` bileşenine geçildi.
* İşlem adı (`prgname`) ve süreç yönetimi optimize edildi.

---

## [1.2.5] - Pardus Tabanı

### Eklendi & Düzeltildi
* Portekizce (`pt`) ve İspanyolca (`es`) çeviriler güncellendi.
* `--json` parametresinin X11 gereksinimi duyması sorunu düzeltildi.
* `/run/winroot` dizini izinleri kısıtlandı; yetkisiz kullanıcıların dosya okuması engellendi (`nodev`, `noexec`, `nosuid` bayrakları eklendi).

---

## [1.2.4] - Pardus Tabanı

### Değiştirildi
* UI bileşenlerinde yeniden boyutlandırma davranışları iyileştirildi.
* Ekran kartı ve OpenGL sürücü algılama algoritmaları güncellendi.

---

## [1.2.3] - Pardus Tabanı

### Eklendi
* Monitör EDID ikili çözücüsü (`edid.py`) entegre edildi; en-boy oranı, çözünürlük ve model adı algılama yeteneği kazandırıldı.
* Çift önyükleme (`DualBootManager`) tespitinde EFI girdileri desteği eklendi.

---

## [1.0.0] - İlk Kararlı Pardus Sürümü

* Sistem özeti ve donanım bilgilendirme ilk kararlı sürümü yayınlandı.
