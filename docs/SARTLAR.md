# Kullanım Şartları ve Sorumluluk Reddi (SARTLAR.md)

Bu belge, **Pars About** (`org.parslinux.about`) sistem ve donanım bilgilendirme uygulamasının kullanım koşullarını, garanti kapsamını ve teşhis verisi sorumluluk sınırlarını belirler.

---

## 1. Uygulamanın Amacı ve Kapsamı

Pars About, Pars Linux ve uyumlu GNU/Linux sistemlerinde donanım bileşenlerini, sistem yapılandırmalarını ve çalışma zamanı durumlarını görüntülemek, analiz etmek ve teknik destek süreçleri için raporlamak amacıyla geliştirilmiş ücretsiz ve açık kaynaklı bir sistem aracıdır.

---

## 2. Garanti Reddi (GPL-3.0+)

Bu program, faydalı olacağı umuduyla dağıtılmaktadır; ancak **HİÇBİR GARANTİSİ YOKTUR**; hatta **TİCARİ DEĞER** veya **BELİRLİ BİR AMACA UYGUNLUK** gibi zımni garantiler de verilmemektedir. Ayrıntılar için GNU Genel Kamu Lisansı'na bakınız.

Pars Linux geliştiricileri veya katkıda bulunanlar:
* Donanım üreticisi sürücülerinden, BIOS/UEFI bellenimlerinden veya çekirdek arabirimlerinden (`/sys`, `/proc`) kaynaklanan eksik veya hatalı donanım raporlamalarından,
* Üçüncü taraf araçlar veya donanım sınırlarının zorlanması sonucu ortaya çıkabilecek aşırı ısınma ve donanım arızalarından,
* Yazılımın kullanımından veya kullanılamamasından doğabilecek doğrudan veya dolaylı veri kayıplarından sorumlu tutulamaz.

---

## 3. Teşhis Verileri ve Gizlilik

* **Yerel İşleme**: Tüm donanım sorguları ve veri toplama işlemleri tamamen yerel bilgisayarınızda gerçekleştirilir.
* **Telemetri ve Arka Plan Takibi Yoktur**: Pars About arka planda telemetri toplamaz; kullanıcının açık rızası ve isteği dışında harici sunuculara donanım parmak izi göndermez.
* **Sistem Raporu Paylaşımı**: "Sistem Teşhis Raporu" oluşturulduğunda (`/tmp/pars_system_report`), sistem günlükleri, ağ konfigürasyonu ve donanım dökümü tek bir arşivde toplanır. Bu arşivi üçüncü kişilerle veya teknik destek forumlarıyla paylaşmadan önce kişisel veya hassas bilgileri (örneğin IP adresleri, özel ağ adları) incelemek kullanıcının sorumluluğundadır.

---

## 4. Lisans

Pars About, **GNU Genel Kamu Lisansı sürüm 3 veya daha yenisi (GPL-3.0+)** ile lisanslanmıştır. Yazılımın kaynak kodlarını inceleme, değiştirme ve yeniden dağıtma haklarına sahipsiniz.
