# Güvenlik Politikası (SECURITY.md)

Pars Linux ekibi olarak kullanıcılarımızın sistem güvenliğini, veri gizliliğini ve ayrıcalık sınırlarını en üst düzeyde korumayı taahhüt ediyoruz.

---

## 1. Desteklenen Sürümler

| Sürüm | Destek Durumu |
|:---|:---|
| 0.1.x (Pars Linux) | :white_check_mark: Aktif Geliştirme ve Destek |
| 1.2.x (Geçiş Tabanı) | :warning: Hata Çözümleri |
| < 1.0 | :x: Desteklenmiyor |

---

## 2. Güvenlik ve Ayrıcalık Modeli (Privilege Separation)

Pars About aşağıdaki temel güvenlik prensiplerine göre tasarlanmıştır:

1. **Ayrıcalıksız Arayüz (Unprivileged UI)**: Grafik kullanıcı arayüzü (`MainWindow.py`) ve temel donanım algılama modülleri (`src/util/`) kesinlikle standart kullanıcı izinleriyle çalışır. Kök (`root`) yetkisiyle arayüz başlatılmaz.
2. **Korumalı Eylem İzolasyonu**: Yalnızca kök yetkisi gerektiren hassas işlemler (`Actions.py`, `ActionsAsk.py`) PolicyKit (`pkexec`) üzerinden çalıştırılır:
   - Sistem bilgisayar adını (`hostname`) değiştirme
   - Çift önyükleme (Dual Boot) için ham disk bölüntülerini ve EFI tablolarını tarama
   - `/var/log` altındaki kök yetkili sistem günlüklerini teşhis arşivine kopyalama
3. **PolicyKit Yetki Denetimi**: `/usr/share/polkit-1/actions/org.parslinux.pkexec.pars-about.policy` dosyası, eylemlerin yalnızca yetkili sistem yöneticileri (`auth_admin_keep`) tarafından şifre ile onaylanarak yürütülmesini garanti eder.
4. **Geçici Dosya Güvenliği**: Teşhis raporu oluşturulurken `/tmp/pars_system_report` dizini üzerinde sahiplik (`chown`) ve dosya izinleri (`chmod 755`) sıkı şekilde ayarlanır; yetkisiz kullanıcıların verilere erişimi veya sembolik bağ saldırıları önlenir.
5. **Ağ Güvenliği**: Uygulama herhangi bir harici telemetri sunucusuna donanım parmak izi göndermez.

---

## 3. Güvenlik Açığı Bildirimi

Bir güvenlik açığı veya yetki yükseltme zaafı tespit ederseniz, lütfen bunu herkese açık GitHub/GitLab sorunlarında (Issues) paylaşmayınız.

Açığı doğrudan aşağıdaki kanallardan bildiriniz:
* **E-posta**: `security@parslinux.org` veya `dev@parslinux.org`
* **Bildirim İçeriği**:
  - Açığın türü ve etkisi
  - Yeniden üretme adımları ve PoC (varsa)
  - Etkilenen sistem ve mimari ayrıntıları

Güvenlik bildiriminiz en geç 48 saat içinde değerlendirilecek ve gerekli güvenlik güncellemeleri ivedilikle yayınlanacaktır.
