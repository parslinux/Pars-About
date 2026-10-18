# Pars About — Veri Tasarrufu ve Gizlilik Kılavuzu (DATA_SAVING_GUIDE.md)

Bu kılavuz, **Pars About** (`org.parslinux.about`) uygulamasının veri tüketimini, çevrimdışı çalışma kabiliyetini, sistem teşhis raporu depolamasını ve kullanıcı gizliliği ilkelerini açıklar.

---

## 1. Çevrimdışı (Offline) Çalışma ve Sıfır Bant Genişliği

* **Tamamen Yerel Donanım Taraması**: Pars About sistemdeki tüm donanımları (İşlemci, RAM, Ekran Kartı, Depolama, Ağ Kartları, USB ve PCI cihazları, Monitör EDID verisi) doğrudan Linux çekirdeğinin arabirimlerinden (`/sys`, `/proc`, `/dev`) ve yerel sistem komutlarından (`lspci`, `lsusb`, `lsblk`, `dmidecode`) okur.
* **Ağ Bağımsızlığı**: Uygulama internet bağlantısı olmadan %100 işlevseldir. Kotalı veya hava boşluklu (air-gapped) ortamlarda hiçbir veri transferi yapmaz.
* **Genel IP (Public IP) İstisnası**: Yalnızca kullanıcı arayüzde "Genel IP" sekmesini açtığında veya sorguladığında harici bir HTTP isteği yapılır; bunun haricinde hiçbir arka plan ağ trafiği oluşturulmaz.

---

## 2. Sistem Teşhis Raporu ve Depolama Yönetimi

Uygulamanın "Sistem Raporu Oluştur" özelliği kullanıldığında:

### 2.1. Depolama Konumu
* Rapor verileri geçici olarak `/tmp/pars_system_report/` dizininde oluşturulur.
* `/tmp` dizini çoğu sistemde RAM tabanlı (**tmpfs**) olduğundan disk ömrünü (SSD aşınması) tüketmez ve sistem yeniden başlatıldığında otomatik olarak temizlenir.
* Yeni bir rapor oluşturulmadan önce eski geçici dizin tamamen silinir.

### 2.2. Masaüstüne Arşivleme
* Kullanıcı raporu dışa aktarmak istediğinde veriler `tar -czf` ile sıkıştırılarak kullanıcının masaüstüne tek bir `.tar.gz` arşivi olarak kaydedilir.

---

## 3. Toplanan Verilerin Kapsamı ve Gizlilik Güvencesi

Sistem teşhis raporunda **toplanan** veriler:
* Donanım dökümü (`system_info.json`)
* Çekirdek günlükleri (`dmesg`, `journalctl`)
* Paket listesi (`dpkg -l` / `apt list`)
* Ağ arabirim durumları (`ip addr`, `nmcli`)
* Sistem servis durumları ve süreç listesi (`ps aux`)

Sistem teşhis raporunda **ASLA TOPLANMAYAN** veriler:
* Kullanıcı ev dizini (`/home/kullanici/`) dosyaları ve kişisel belgeler
* Web tarayıcısı geçmişi, çerezler ve parolalar
* Kriptografik anahtarlar (`~/.ssh`, `~/.gnupg`)
* Uygulama veritabanları veya kişisel fotoğraflar

---

## 4. Raporu Paylaşmadan Önce İnceleme ve Temizleme

Teşhis raporunu teknik destek forumlarında paylaşmadan önce incelemek isterseniz:
1. Masaüstünüzdeki `.tar.gz` arşivini açın.
2. `system_info.json` veya günlük dosyalarından IP adresiniz ya da bilgisayar adınız gibi paylaşmak istemediğiniz satırları düzenleyebilirsiniz.
