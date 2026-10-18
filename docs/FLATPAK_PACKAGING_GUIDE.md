# Pars About — Flatpak Paketleme Kılavuzu (FLATPAK_PACKAGING_GUIDE.md)

Bu doküman, **Pars About** uygulamasının evrensel Linux paketleme formatı olan **Flatpak** ile nasıl paketleneceğini, korumalı alan (sandbox) izin gereksinimlerini ve Flathub standartlarını açıklar.

---

## 1. Donanım Bilgilendirme Araçlarında Sandbox İzinleri

Donanım araçları çekirdek donanım tablolarını (`/sys`, `/proc`, `/dev`) ve sistem D-Bus servislerini doğrudan okuma ihtiyacı duyar. Bu nedenle Pars About Flatpak paketinde şu izinler zorunludur:

* `--filesystem=host:ro`: Sistemdeki donanım aygıt dosyalarını okumak için.
* `--device=all`: Grafik kartı hızlandırması ve doğrudan aygıt erişimi için.
* `--socket=x11` / `--socket=wayland`: Ekran sunucusu bağlantısı.
* `--share=network`: Genel IP sorgulama için (opsiyonel).
* `--system-talk-name=org.freedesktop.hostname1`: Bilgisayar adı sorgulaması.

---

## 2. Örnek Flatpak Manifestosu (`org.parslinux.About.yaml`)

```yaml
app-id: org.parslinux.About
runtime: org.gnome.Platform
runtime-version: '46'
sdk: org.gnome.Sdk
command: pars-about

finish-args:
  - --share=ipc
  - --socket=fallback-x11
  - --socket=wayland
  - --share=network
  - --device=all
  - --filesystem=/sys:ro
  - --filesystem=/proc:ro
  - --filesystem=/dev:ro
  - --system-talk-name=org.freedesktop.hostname1
  - --system-talk-name=org.freedesktop.PolicyKit1

modules:
  - name: pars-about
    buildsystem: meson
    sources:
      - type: git
        url: https://github.com/parslinux/Pars-About.git
        tag: v0.1.0-alpha
```

---

## 3. Flatpak Paketini Derleme ve Test Etme

### Gerekli Araçları Yükleme
```bash
# Debian / Pars Linux:
sudo apt install flatpak flatpak-builder

# Arch Linux:
sudo pacman -S flatpak flatpak-builder
```

### GNOME Platformunu Kurma
```bash
flatpak install flathub org.gnome.Platform//46 org.gnome.Sdk//46
```

### Paketi Derleme ve Kullanıcı Alanına Kurma
```bash
flatpak-builder --user --install --force-clean build-flatpak org.parslinux.About.yaml
```

### Paketi Çalıştırma
```bash
flatpak run org.parslinux.About
```
