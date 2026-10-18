# Pars About — Sürüm Politikası (VERSION.md)

Bu doküman, **Pars About** (`org.parslinux.about`) projesinin sürümleme mantığını, sürüm numaralarının senkronizasyonunu ve yayın döngüsünü açıklar.

---

## 1. Semantik Sürümleme (SemVer 2.0.0)

Uygulama `MAJOR.MINOR.PATCH` biçiminde semantik sürümleme kurallarını takip eder:

* **MAJOR**: Geriye dönük uyumluluğu bozan köklü mimari dönüşümler (örn. GTK+ 3'ten GTK 4 / Libadwaita'ya geçiş veya JSON veri şemasının tamamen değişmesi).
* **MINOR**: Geriye dönük uyumlu yeni özellikler ve algılayıcılar (örn. yeni donanım sensörleri, yeni donanım kategorisi, yeni CLI filtreleme bayrakları).
* **PATCH**: Geriye dönük uyumlu hata düzeltmeleri, çeviri güncellemeleri ve küçük performans iyileştirmeleri.

---

## 2. Sürüm Senkronizasyon Noktaları

Her yeni sürüm yayınlandığında aşağıdaki dosyalar senkronize tutulur:

1. `__version__`: Proje kökündeki düz metin sürüm dosyası (`0.1.0-alpha`).
2. `meson.build`: `project('pars-about', version: '0.1.0')` tanımı.
3. `debian/changelog`: En üstteki sürüm başlığı (örn. `pars-about (0.1.0-alpha) unstable; urgency=medium`).
4. Git Etiketi (Tag): Sürüm yayınlandığında `v0.1.0` biçiminde etiket basılır.

---

## 3. Sürüm Geçiş Döngüsü

* **Alpha / Geliştirme Sürümleri (`-alpha`)**: Çatallanma, deneysel özellikler ve büyük kod revizyonları dönemi.
* **Beta Sürümleri (`-beta`)**: Özellik dondurma (feature freeze), çeviri ve donanım uyumluluk testleri dönemi.
* **Kararlı Sürümler (Stable)**: Pars Linux ana paket depolarına giren nihai sürümler.
