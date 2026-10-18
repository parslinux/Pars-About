# Pars About — Çatallanma (Fork) ve Bağımsızlık Bildirisi

Bu belge, **Pars About** (`org.parslinux.about`) projesinin geçmiş kökenini, Pardus ekosisteminden tamamen ayrılma sürecini ve günümüzdeki bağımsız geliştirme yapısını resmî olarak belgeler.

---

## 1. Geçmiş ve Çatallanma Süreci

**Pars About**, TÜBİTAK ULAKBİM tarafından Pardus için geliştirilmiş olan açık kaynaklı `pardus-about` (v1.2.6) yazılımı temel alınarak çatallanmıştır (fork).

Açık kaynak felsefesi ve **GNU Genel Kamu Lisansı (GPL v3.0)** şartlarına tam bağlılık gereğince, orijinal projenin geçmiş kod tabanına ve emeği geçen geliştiricilere teşekkür ederiz.

---

## 2. Pardus ile Bağların Kesilmesi ve Tam Bağımsızlık

Çatallanma sonrasında proje baştan aşağı yeniden yapılandırılmış ve **Pardus ekosistemi ile tüm teknik, yapısal ve kurumsal bağlar tamamen sonlandırılmıştır**:

* **Upstream Senkronizasyonu Sona Erdi:** Orijinal Pardus deposu ile olan eşzamanlama ve sürüm bağı tamamen kaldırılmıştır. Pars About artık bağımsız bir yol haritasına (roadmap) sahiptir.
* **Sunucu ve API Bağımsızlığı:** Eski `donanim.pardus.org.tr` sunucu ve donanım raporlama alan adları projeden arındırılmış, ağ istekleri yerel ve bağımsız hale getirilmiştir.
* **Tek Dağıtım Tekelinden Çıkış:** Orijinal proje yalnızca Debian/Pardus odaklıyken; Pars About başta **Pars Linux (Arch Linux / CachyOS tabanı)** olmak üzere Debian, Ubuntu, Fedora ve diğer tüm modern GNU/Linux dağıtımlarında yerel çalışabilecek şekilde çoklu dağıtım desteğine kavuşturulmuştur.

---

## 3. Yapılan Temel İyileştirmeler ve Yenilikler

Pars Linux ekibi tarafından projeye kazandırılan başlıca özellikler şunlardır:

### 🎨 A. Özgün Görsel Kimlik ve Vektörel İkon Seti
* Uygulamanın tüm grafiksel varlıkları yenilenmiş; her donanım bileşeni (CPU, GPU, RAM, Depolama, Ağ, Ses, Bluetooth, Giriş aygıtları vb.) için özel modern SVG vektörel ikonlar üretilmiştir.
* Modern koyu tema (Dark Mode) uyumu ve yüksek çözünürlüklü ekranlar (HiDPI) için tam ölçekleme optimizasyonu sağlanmıştır.

### 🛠️ B. Yönetim ve Otomasyon Betikleri
Uygulamanın çalıştırılması, kurulması ve paketlenmesi için hepsi-bir-arada araçlar geliştirilmiştir:
* **`manage.sh`**: İnteraktif konsol menülü yönetim merkezi.
* **`run.sh`**: Yerel kaynak koddan GUI, donanım veya JSON modunda hızlı çalıştırma.
* **`install.sh`**: Meson & Ninja ile `/usr` sistem dizinlerine tek adımda kurulum ve önbellek yenileme.
* **`uninstall.sh`**: Masaüstü kısayolları, PolicyKit kuralları ve ikonlarla birlikte sistemden temizleme.
* **`package.sh`**: Arch Linux (`.pkg.tar.zst`), Debian (`.deb`) ve kaynak arşiv (`.tar.gz`) paketleme aracı.

### 📸 C. Otomatik Ekran Görüntüsü Yakalama
* `tools/capture_screenshots.py` aracı ile GTK pencere belleği üzerinden doğrudan piksel piksel güncel ekran görüntüleri (Sistem Özeti, Donanım Ayrıntıları, Rapor Menüsü) otomatik üretilir hale getirilmiştir.

### 🧪 D. Kapsamlı Test Altyapısı
* `tests/` dizini altında 18 farklı birim testinden oluşan otomatik test paketi geliştirilmiştir (CLI JSON doğrulaması, donanım yöneticileri, masaüstü XDG uyumluluğu, PolicyKit ve gettext çeviri denetimi).

### 🔒 E. Güvenlik ve PolicyKit Standartları
* Polkit yetkilendirmesi `org.parslinux.pkexec.pars-about.policy` olarak taşınmış; en düşük yetki prensibiyle sistem raporlama ve hostname işlemleri güvenlik altına alınmıştır.

---

## 4. Geliştirme ve Bakım

Pars About projesi, **Pars Linux Geliştirici Ekibi** tarafından aktif olarak geliştirilmekte ve sürdürülmektedir:

* **Resmî Git Deposu:** [https://github.com/parslinux/Pars-About](https://github.com/parslinux/Pars-About)
* **İletişim & Hata Bildirimi:** GitHub Issues
* **Lisans:** GNU General Public License v3.0 (GPL-3.0-or-later)
