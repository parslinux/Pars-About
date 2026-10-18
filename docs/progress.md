# Proje İlerlemesi — Pars About (progress.md)

Bu dosya, **Pars About** (`org.parslinux.about`) projesinin gelişim sürecini, tamamlanan kilometre taşlarını ve gelecek hedeflerini belgeler.

---

## 🎯 Kilometre Taşı 1: Çatallanma ve Pars Linux Markalaması ✅
- [x] Kaynak depo (`pardus-about`) çatallandı.
- [x] Uygulama kimliği `org.parslinux.about` olarak güncellendi.
- [x] İkili çalıştırma komutu `pars-about` olarak tanımlandı.
- [x] Masaüstü kısayolları oluşturuldu (`org.parslinux.about.desktop` ve `org.parslinux.about-hardware.desktop`).
- [x] Kaynak kod dizin yolları `/usr/share/pars/pars-about/` olarak standardize edildi.
- [x] Uygulama telif ve lisans bilgileri Pars Linux olarak güncellendi.

---

## 🎯 Kilometre Taşı 2: Özgün Vektörel SVG Donanım İkonları ✅
- [x] Pars Linux görsel diline uygun yüksek çözünürlüklü SVG aygıt simgeleri tasarlandı (`data/icons/`).
- [x] Tüm donanım kategorilerine özel ikonlar bağlandı (İşlemci, Bellek, GPU, Disk, Ekran, Ses, Ağ, Wi-Fi, Ethernet, Bluetooth, Kamera, Giriş Aygıtları, Anakart/BIOS, Genel IP).
- [x] Sistem tepsisi ve menü için `pars-about.svg`, `pars-hardware-info.svg` ve sembolik simgeler tamamlandı.

---

## 🎯 Kilometre Taşı 3: Headless CLI ve JSON Donanım Motoru ✅
- [x] `--json` (`-j`) komut satırı argümanı eklendi.
- [x] X11/Wayland ekran sunucusu gereksinimi kaldırıldı; saf terminal ve SSH oturumlarında çalışma garantilendi.
- [x] `ComputerManager.get_all_device_info()` ile tüm bileşenlerin hiyerarşik JSON yapısı doğrulandı.
- [x] `--hardware` (`-h`) parametresi ile doğrudan donanım sekmesine geçiş sağlandı.

---

## 🎯 Kilometre Taşı 4: Arayüz ve Ölçekleme İyileştirmeleri ✅
- [x] Küçük ekranlı cihazlarda ve HiDPI ekranlarda pencere yeniden boyutlandırma sorunları çözüldü.
- [x] Rapor kopyalama popover donma hatası giderilerek `GtkRevealer` mimarisine geçildi.
- [x] Donanım özet kartları (`HardwareGridCell`) ve detay satırları (`HardwareDetailRow`) modernize edildi.
- [x] `css/main.css` özel tema stilleri güçlendirildi.

---

## 🎯 Kilometre Taşı 5: Güvenlik ve PolicyKit Entegrasyonu ✅
- [x] PolicyKit yetki politikası `org.parslinux.pkexec.pars-about.policy` dosyasına aktarıldı.
- [x] Yetki kuralı `org.parslinux.about.rules` olarak güncellendi.
- [x] Arayüzün ayrıcalıksız kullanıcı haklarıyla çalışması, yalnızca korumalı eylemlerin (`Actions.py`, `ActionsAsk.py`) `pkexec` üzerinden yürütülmesi sağlandı.
- [x] Sistem teşhis raporu (`SystemReportManager`) güvenli `/tmp/pars_system_report` çalışma alanına bağlandı.

---

## 🎯 Kilometre Taşı 6: Çeviri ve Yerelleştirme Altyapısı ✅
- [x] GNU gettext alan adı `pars-about` olarak güncellendi.
- [x] `update-translations.sh` ve `fix-po.sh` betikleri optimize edildi.
- [x] Türkçe (`tr`), Portekizce (`pt`) ve İspanyolca (`es`) çevirileri güncellendi.

---

## 🎯 Kilometre Taşı 7: Kapsamlı Dokümantasyon Seti ✅
- [x] Tüm teknik kılavuzlar `docs/` altında standartlaştırıldı:
  - `ARCHITECTURE.md`, `FORK.md`, `CLAUDE.md`, `CLI_REFERENCE.md`, `CHANGELOG.md`
  - `INSTALL.md`, `TESTING.md`, `TRANSLATION_GUIDE.md`, `CONTRIBUTING.md`
  - `UYGULAMA_BAGLAMA.md`, `DATA_SAVING_GUIDE.md`, `SELF_HOSTING_GUIDE.md`
  - `TERMS.md`, `SARTLAR.md`, `VERSION.md`, `SECURITY.md`, `PAYMENT_INTEGRATION.md`
  - `FLATPAK_PACKAGING_GUIDE.md`, `INDEX.md`.
- [x] `.claudeignore` yapılandırması oluşturuldu.
- [x] Ana `README.md` dokümantasyon haritası ile zenginleştirildi.

---

## 🎯 Kilometre Taşı 8: Teknik Borç Temizliği, AppStream ve Arch Linux Paketleme ✅
- [x] Kalan tüm Pardus ad alanı kalıntıları Pars Linux standartlarına geçirildi (`SystemReportManager` teşhis yolu, `MainWindow` API alanı, PolicyKit vendor bilgileri).
- [x] Masaüstü kısayolları (`org.parslinux.about.desktop` ve `org.parslinux.about-hardware.desktop`) temizlendi ve düzeltildi.
- [x] AppStream metainfo XML spesifikasyonu hazırlandı (`data/org.parslinux.about.metainfo.xml`) ve `meson.build` kurulumuna bağlandı.
- [x] Debian changelog senkronize edildi (`0.1.0-alpha`).
- [x] Arch Linux paketleme dosyaları (`PKGBUILD` ve `.SRCINFO`) oluşturuldu.

---

## 🎯 Kilometre Taşı 9: Otomatik Test Paketi ve Kalite Güvencesi (`tests/`) ✅
- [x] Süreç yalıtımlı modüler test altyapısı kuruldu:
  - `tests/test_cli_json.py`: Headless ve DISPLAY'siz JSON çıktı doğrulaması.
  - `tests/test_hardware_detectors.py`: Donanım algılama modülleri birim testleri.
  - `tests/test_metadata_and_desktop.py`: XDG masaüstü dosyaları, AppStream ve Polkit XML doğrulaması.
  - `tests/test_system_report.py`: Teşhis raporu ve kullanıcı yetki denetimi.
  - `tests/test_translations.py`: gettext dil dosyaları sözdizimi doğrulaması.
- [x] Test yürütücüsü `tests/run_all_tests.py` yazıldı; 18 testin 18'i de başarıyla geçti.

---

## 🚀 Gelecek Kilometre Taşları (Yol Haritası)

### 🎯 Kilometre Taşı 10: Canlı Donanım Sensörleri ve İzleme
- [ ] CPU sıcaklığı, fan hızı ve anlık çekirdek frekansı göstergeleri (`lm-sensors` entegrasyonu).
- [ ] GPU anlık yük ve VRAM kullanım yüzdeleri.

### 🎯 Kilometre Taşı 11: Saf GTK 4 & Libadwaita Dönüşümü (Planlanan)
- [ ] Glade XML bağımlılığını kaldırıp saf Python Libadwaita arayüzüne geçiş.
- [ ] `Adw.PreferencesPage` ve `Adw.ActionRow` bileşenleriyle GNOME HIG standartlarına tam uyum.

### 🎯 Kilometre Taşı 12: Çoklu Monitör Düzeni Görselleştiricisi
- [ ] Bağlı monitörlerin masaüstü konumlarını, ölçekleme oranlarını ve yenileme hızlarını görselleştiren interaktif şema.
