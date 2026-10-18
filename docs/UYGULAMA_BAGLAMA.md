# Pars About — Uygulama ve Masaüstü Entegrasyonu Kılavuzu (UYGULAMA_BAGLAMA.md)

Bu doküman, **Pars About** (`org.parslinux.about`) uygulamasının GNU/Linux masaüstü ortamlarına (XFCE, GNOME, KDE Plasma vb.), ayarlar merkezlerine ve sistem menülerine nasıl entegre olduğunu detaylandırır.

---

## 1. Masaüstü Kısayolları (XDG Desktop Entries)

Uygulama sisteme iki bağımsız masaüstü girişi sağlar:

### 1.1. Genel Sistem Özeti ve Hakkında
`/usr/share/applications/org.parslinux.about.desktop`:
```ini
[Desktop Entry]
Name=Pars Linux Hakkında
Name[en]=About Pars Linux
GenericName=Hakkında
GenericName[en]=About
Comment=Pars Linux sisteminiz hakkında bilgi edinin.
Comment[en]=Get info about your Pars system.
Exec=pars-about
Icon=pars-about
Terminal=false
Type=Application
Categories=Settings;X-XFCE-SettingsDialog;X-Pars-Apps;
StartupNotify=true
Keywords=about;info;system;hakkında;bilgi;sistem;
```

### 1.2. Donanım Bilgisi Doğrudan Başlatıcı
`/usr/share/applications/org.parslinux.about-hardware.desktop`:
```ini
[Desktop Entry]
Name=Pars Donanım Bilgisi
Name[en]=Pars Hardware Information
GenericName=Donanım Bilgisi Görüntüleyici
GenericName[en]=Hardware Information Viewer
Comment=Pars sisteminizdeki donanımlar hakkında bilgi edinin.
Comment[en]=Get informations about the hardware in your Pars system.
Exec=pars-about --hardware
Icon=pars-hardware-info
Terminal=false
Type=Application
Categories=Settings;X-XFCE-SettingsDialog;X-Pars-Apps;HardwareSettings;
StartupNotify=true
Keywords=about;info;system;hardware;donanım;aygıt;
```

---

## 2. Ayarlar Yöneticisi ve Kontrol Merkezi Entegrasyonu

* **XFCE Ayarlar Yöneticisi (`xfce4-settings-manager`)**:
  - `X-XFCE-SettingsDialog` kategorisi sayesinde hem "Pars Linux Hakkında" hem de "Pars Donanım Bilgisi" simgeleri XFCE Ayarlar Yöneticisi penceresinde "Sistem" başlığı altında otomatik olarak yer alır.
* **Pars Linux Menüsü**:
  - `X-Pars-Apps` kategorisi, Pars Linux dağıtım menüsünde "Pars Araçları" kategorisi altında doğrudan görünmesini sağlar.
* **GNOME ve KDE**:
  - `Settings` ve `HardwareSettings` standart kategorileri sayesinde uygulama arama çubuğundan "donanım", "sistem" veya "hakkında" yazıldığında anında bulunur.

---

## 3. İkon Teması ve Sistem Varlıkları Entegrasyonu

Meson kurulum kuralları (`meson.build`) gereğince simgeler standart Hicolor ikon hiyerarşisine kopyalanır:

* `/usr/share/icons/hicolor/scalable/apps/pars-about.svg`
* `/usr/share/icons/hicolor/scalable/apps/pars-hardware-info.svg`
* `/usr/share/icons/hicolor/scalable/apps/pars-about-symbolic.svg`
* `/usr/share/icons/hicolor/scalable/devices/pars-about-*.svg` (Tüm donanım kategorisi SVG'leri)

Kurulum sonrasında ikon önbelleğini güncellemek için:
```bash
sudo gtk-update-icon-cache -f /usr/share/icons/hicolor
sudo update-desktop-database /usr/share/applications
```

---

## 4. PolicyKit Yetkilendirme Entegrasyonu

Korumalı eylemler için iki dosya sistemde kayıtlıdır:
1. `/usr/share/polkit-1/actions/org.parslinux.pkexec.pars-about.policy`: Eylemlerin başlıklarını, açıklamalarını ve varsayılan yetkilendirme gereksinimlerini (`auth_admin_keep`) tanımlar.
2. `/usr/share/polkit-1/rules.d/org.parslinux.about.rules`: Sistem yöneticisi grubu (sudo/wheel) için yetkilendirme kurallarını belirler.
