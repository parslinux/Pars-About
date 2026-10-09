# Pars About - Kurulum ve Derleme Kılavuzu

Bu belge, **Pars About** uygulamasının bağımlılıklarını, yerel geliştirme ortamında çalıştırılmasını, kaynak koddan derlenerek sisteme kurulmasını ve Debian/Pars paketi (.deb) olarak derlenmesini anlatmaktadır.

---

## 1. Bağımlılıklar

Uygulamanın sorunsuz çalışabilmesi için aşağıdaki paketlerin sistemde yüklü olması gerekmektedir:

### Sistem ve Derleme Paketleri (Debian / Pars / Ubuntu)
```bash
sudo apt update
sudo apt install -y \
    python3 \
    python3-gi \
    python3-requests \
    python3-cairosvg \
    python3-cups \
    gir1.2-gtk-3.0 \
    gir1.2-glib-2.0 \
    gir1.2-gudev-1.0 \
    gir1.2-soup-2.4 \
    mesa-utils \
    pciutils \
    lsb-release \
    hwdata \
    dconf-cli \
    pkexec \
    meson \
    ninja-build \
    gettext
```

### Sistem ve Derleme Paketleri (Arch Linux)
```bash
sudo pacman -Syu --needed \
    python \
    python-gobject \
    python-requests \
    python-cairosvg \
    pycups \
    gtk3 \
    glib2 \
    libgudev \
    libsoup3 \
    mesa-utils \
    pciutils \
    lsb-release \
    hwdata \
    dconf \
    polkit \
    meson \
    ninja \
    gettext
```

---

## 2. Yerel Ortamda Çalıştırma (Kurulum Yapmadan)

Geliştirme veya test amacıyla uygulamayı sisteme kurmadan doğrudan proje dizininden çalıştırabilirsiniz:

### Grafik Arayüzü (GUI) İle Çalıştırma:
```bash
python3 pars-about.py
```
veya:
```bash
python3 src/Main.py
```

### Donanım Sekmesini Doğrudan Açma:
```bash
python3 pars-about.py --hardware
```

### CLI Üzerinden JSON Raporu Alma:
```bash
python3 pars-about.py --json
```

---

## 3. Kaynak Koddan Derleme ve Sisteme Kurma (Meson & Ninja)

Uygulamayı Meson yapılandırma sistemi ile derleyip `/usr` dizinine yükleyebilirsiniz.

### Adım 1: Meson Yapılandırma Dizini Oluşturma
```bash
meson setup builddir --prefix=/usr
```

### Adım 2: Derleme ve Çevirileri Derleme
```bash
ninja -C builddir
```

### Adım 3: Sisteme Yükleme
```bash
sudo ninja -C builddir install
```

Kurulum tamamlandıktan sonra uygulamayı terminalden `pars-about` komutuyla veya uygulama menüsünden başlatabilirsiniz.

---

## 4. Debian / Pars Paketi (.deb) Oluşturma

Pars veya Debian tabanlı sistemler için paket (.deb) derlemek isterseniz:

### Adım 1: Paket Derleme Araçlarını Yükleme
```bash
sudo apt install -y build-essential debhelper devscripts
```

### Adım 2: .deb Paketini Derleme
Proje ana dizinindeyken:
```bash
dpkg-buildpackage -b -uc -us
```

### Adım 3: Derlenen Paketi Yükleme
Derlenen `.deb` paketi bir üst dizinde oluşacaktır. Yüklemek için:
```bash
sudo dpkg -i ../pars-about_*.deb
sudo apt install -f  # Eksik bağımlılık varsa tamamlar
```

---

## 5. Sisteme Kurulan Uygulamayı Kaldırma

### Meson İle Yüklendiyseniz:
```bash
sudo ninja -C builddir uninstall
```

### Paket (.deb) İle Yüklendiyseniz:
```bash
sudo apt remove pars-about
```
