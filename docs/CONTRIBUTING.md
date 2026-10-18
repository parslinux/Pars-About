# Pars About — Katkı Sağlama Rehberi (CONTRIBUTING.md)

Pars Linux ve **Pars About** projesine katkıda bulunmak istediğiniz için teşekkür ederiz! Açık kaynak topluluğumuzun katkılarıyla sistemimiz daha kararlı, modern ve zengin donanım desteğine sahip hale gelmektedir.

---

## 1. Katkı Türleri

* **Donanım Algılama Hataları (Hardware Bug Reports)**: Sisteminizdeki bir donanım (işlemci, ekran kartı, Wi-Fi yongası, monitör EDID bilgisi vb.) eksik veya hatalı görünüyorsa, lütfen bir hata kaydı açarak `pars-about --json` çıktısını ekleyiniz.
* **Yeni Özellik Önerileri**: Sensör göstergeleri, yeni donanım kategorileri veya arayüz iyileştirmeleri.
* **Çeviri ve Yerelleştirme**: Mevcut Türkçe, Portekizce, İspanyolca çevirileri zenginleştirme veya yeni diller ekleme.
* **Dokümantasyon**: Belgeleri genişletme, teknik detayları ve rehberleri güncelleme.
* **Kod Katkısı**: Hata çözümleri, mimari sadeleştirmeler ve performans optimizasyonları.

---

## 2. Geliştirme ve Katkı İş Akışı

1. Depoyu kendi GitHub/GitLab hesabınıza çatallayın (Fork).
2. Yeni bir geliştirme dalı (branch) oluşturun:
   ```bash
   git checkout -b feature/yeni-donanim-destegi
   # veya
   git checkout -b fix/edid-cozumleme-hatasi
   ```
3. Değişikliklerinizi yapın ve yerel ortamda test edin:
   ```bash
   python3 pars-about.py
   python3 pars-about.py --json
   ```
4. Git commit mesajlarınızı Conventional Commits kurallarına uygun yazın:
   - `feat: ...` — Yeni bir özellik veya donanım algılayıcı ekleme
   - `fix: ...` — Bir hatanın düzeltilmesi
   - `docs: ...` — Dokümantasyon değişiklikleri
   - `i18n: ...` — Çeviri ve dil dosyaları güncellemeleri
   - `refactor: ...` — Kod sadeleştirme ve mimari düzenlemeler
5. Dalınızı çatalladığınız depoya itin ve ana depoya bir Çekme İsteği (Pull Request) gönderin.

---

## 3. Kod Standartları

* **PEP 8**: Kodlar PEP 8 standartlarına uymalı, temiz ve okunabilir olmalıdır.
* **İsimlendirme**: Değişkenlerde ve fonksiyonlarda `snake_case` tercih edilmelidir.
* **Widget Kimlikleri**: Glade XML ve Python kodlarında tüm GTK widget ID'leri `ui_<ad>_<tur>` standardına uygun olmalıdır (örn: `ui_hostname_button`).
* **Çoklu Dil**: Kullanıcı arayüzüne eklenen tüm metinler `_("Metin")` gettext fonksiyonu ile yazılmalıdır.
* **Güvenlik**: Kök yetkisi gerektirmeyen hiçbir işlem `pkexec` üzerinden çağrılmamalıdır; GUI her zaman standart kullanıcı yetkisiyle çalışmalıdır.
