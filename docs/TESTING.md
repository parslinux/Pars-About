# Pars About — Test ve Kalite Güvencesi Kılavuzu (TESTING.md)

Bu doküman, **Pars About** (`org.parslinux.about`) projesinde yürütülen test stratejilerini, doğrulama adımlarını ve kalite güvence süreçlerini açıklar.

---

## 1. Test Katmanları ve Kapsamı

Pars About aşağıdaki beş temel katmanda test edilir:

```
+-----------------------------------------------------------------------------------+
| 1. Donanım ve Algılama Testleri: util/ altındaki yöneticilerin veri doğruluğu    |
+-----------------------------------------------------------------------------------+
| 2. Headless CLI ve JSON Testi: --json parametresinin X11'siz doğru JSON üretmesi  |
+-----------------------------------------------------------------------------------+
| 3. Polkit Eylem Doğrulaması: Actions.py ve ActionsAsk.py çıkış kodları            |
+-----------------------------------------------------------------------------------+
| 4. Çeviri ve Dil Bütünlüğü: po/*.po dosyalarının gettext sözdizimi doğrulaması    |
+-----------------------------------------------------------------------------------+
| 5. Arayüz Duman (Smoke) Testi: Xvfb sanal ekranı ile UI başlatma denemesi         |
+-----------------------------------------------------------------------------------+
```

---

## 2. Testleri Çalıştırma

### 2.1. Donanım Algılama ve JSON Çıktı Testi
`pars-about --json` çıktısının geçerli bir JSON olduğunu ve hata vermeden `0` koduyla çıktığını doğrulamak için:

```bash
# JSON sözdizimi ve çıktı doğrulaması
python3 -c '
import subprocess, json
proc = subprocess.run(["python3", "pars-about.py", "--json"], capture_output=True, text=True)
assert proc.returncode == 0, f"Hata Kodu: {proc.returncode}"
data = json.loads(proc.stdout)
assert "processor" in data or "memory" in data or "os" in data
print("JSON Headless Testi Başarılı!")
'
```

### 2.2. X11'siz Ortamda (Headless) Çalışma Testi
`DISPLAY` ortam değişkeni kaldırıldığında `--json` modunun çökmediğini doğrulamak için:

```bash
env -u DISPLAY python3 pars-about.py --json > /dev/null && echo "X11 Bağımsızlık Testi Geçti!"
```

### 2.3. Çeviri Dosyalarının Sözdizim Testi
Tüm `.po` dosyalarının gettext standartlarına uygun olduğunu ve bozuk karakter içermediğini kontrol etmek için:

```bash
for po in po/*.po; do
    echo "Denetleniyor: $po"
    msgfmt -c -v "$po" -o /dev/null || exit 1
done
```

### 2.4. PolicyKit Eylem Testleri
`Actions.py` betiğinin parametreleri doğru algıladığını sınamak için:

```bash
python3 src/Actions.py acpi
echo "ACPI çıkış kodu: $?"
```

### 2.5. Sanal Ekranda Arayüz Duman Testi (Smoke Test)
Grafik arayüzü sanal X11 ekranında (`Xvfb`) 2 saniye çalıştırıp kapatarak çökme olmadığını test etmek için:

```bash
xvfb-run -a timeout 3s python3 pars-about.py || true
```

### 2.6. Kod Stili ve PEP 8 Doğrulaması
```bash
python3 -m pycodestyle src/ --max-line-length=120 --ignore=E402,W503 || true
```

---

## 3. Donanım Raporlama Hata Ayıklama (Debugging)

Bir cihazda donanım bilgisi eksik veya yanlış geliyorsa:

1. Ham sistem çıktılarını kontrol edin:
   - `lspci -nnvv` (PCI cihazları)
   - `lsusb -v` (USB cihazları)
   - `lsblk -f` (Diskler)
   - `/sys/class/drm/*/edid` (Ekranlar)
2. `src/util/ComputerManager.py` dosyasını Python etkileşimli kabuğunda doğrudan test edin:
   ```python
   from util import ComputerManager
   cm = ComputerManager.ComputerManager()
   print(cm.get_all_device_info())
   ```
