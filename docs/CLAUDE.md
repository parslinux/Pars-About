# CLAUDE.md — Pars About Geliştirici ve AI Yönergesi

Bu dosya, `pars-about` deposunda çalışan geliştiriciler ve AI kodlama asistanları için kritik mimari, geliştirme ve stil kurallarını içerir.

---

## 🛠️ Temel Komutlar

### Uygulamayı Çalıştırma (Kaynak Koddan)
```bash
# Doğrudan başlatıcı üzerinden (GUI)
python3 pars-about.py

# Kaynak modülü üzerinden (GUI)
python3 src/Main.py

# Doğrudan Donanım Bilgisi sekmesini açma
python3 pars-about.py --hardware
# veya:
python3 pars-about.py -h

# Headless modda doğrudan JSON donanım raporu alma (X11 gerektirmez)
python3 pars-about.py --json
# veya:
python3 pars-about.py -j
```

### Derleme ve Sisteme Kurma (Meson & Ninja)
```bash
# Meson yapılandırma dizini oluşturma
meson setup builddir --prefix=/usr

# Derleme ve çevirileri derleme
ninja -C builddir

# Sisteme yükleme
sudo ninja -C builddir install

# Sistemden kaldırma
sudo ninja -C builddir uninstall
```

### Debian (.deb) Paketi Derleme
```bash
# Bağımlılıkları yükleme ve paket oluşturma
dpkg-buildpackage -b -uc -us
```

### Çevirileri Güncelleme
```bash
# Çeviri şablonunu ve dil dosyalarını yenileme
./update-translations.sh

# Bozuk çevirileri düzeltme
./fix-po.sh
```

---

## 🏛️ Mimari ve Kodlama Kuralları

1. **PEP 8 Uyumluluğu**: Tüm Python kodları PEP 8 standartlarına uygun olmalıdır (`flake8`, `pylint` veya `black` kullanılabilir).
2. **Değişken İsimlendirmeleri**: Değişken isimlerinde daima küçük harf ve alt çizgi (`snake_case`) kullanılmalıdır (örn. `package_size = 30`). Anlamsız kısaltmalardan kaçınılmalıdır (örn. `pkg_sz` yerine `package_size`).
3. **GTK Widget Kimlikleri (ID Standardı)**: Hem Glade XML (`ui/MainWindow.glade`) dosyasında hem de Python kodunda GTK widget ID'leri kesinlikle `ui_<isim>_<tur>` kalıbına uygun olmalıdır (örn. `ui_hostname_entry`, `ui_refresh_button`, `ui_hardware_stack`).
4. **Standart Kütüphane Tercihi**: Eğer standart Python kütüphaneleriyle çözülebilecek bir durum varsa harici bağımlılık veya tekeri yeniden icat etmek yerine standart modüller tercih edilmelidir.
5. **En Az Yetki İlkesi (Least Privilege)**: Arayüz (`MainWindow.py`) asla `root` olarak çalıştırılmamalıdır. Yalnızca kök yetkisi gerektiren işlemler (`Actions.py`, `ActionsAsk.py`) PolicyKit (`pkexec`) üzerinden ve `org.parslinux.pkexec.pars-about.policy` kurallarına tabi olarak çağrılmalıdır.
6. **Headless Uyumluluğu**: Donanım yöneticileri (`src/util/`) arayüz nesnelerinden bağımsız tasarlanmalıdır. `ComputerManager.py` ve alt yöneticiler GUI olmadan doğrudan veri üretebilmelidir.
7. **Çoklu Dil Desteği (i18n)**: Arayüzde ve kullanıcıya gösterilen tüm metinler `_("Metin")` gettext sarmalayıcısı ile yazılmalıdır.

---

## 📂 Dizin Yapısı Özeti

* `pars-about.py`: Ana çalıştırıcı betik ve python arama yolu ayarlayıcı.
* `src/Main.py`: `Gtk.Application` ana döngüsü ve CLI argüman ayrıştırıcısı.
* `src/MainWindow.py`: Arayüz yöneticisi, sayfa geçişleri, sinyal işleyicileri.
* `src/Actions.py`: PolicyKit (`pkexec`) ile korunan arka plan eylemleri (ACPI, DualBoot).
* `src/ActionsAsk.py`: Teşhis raporu oluşturma tetikleyicisi.
* `src/util/`: Donanım ve sistem algılama kütüphaneleri (CPU, GPU, RAM, Disk, Ağ, EDID, Hostname vb.).
* `src/widget/`: Özel GTK bileşenleri (`HardwareDetailRow.py`, `HardwareGridCell.py`).
* `ui/`: Glade arayüz şablonları (`MainWindow.glade`).
* `css/`: Özel GTK tema ve stil tanımları (`main.css`).
* `data/icons/`: Pars Linux özgün SVG donanım simgeleri.
* `po/`: Çoklu dil çeviri şablonları ve dil dosyaları.
* `polkit/`: PolicyKit eylem tanımları ve kural betikleri.
* `docs/`: Proje dokümantasyonu.
