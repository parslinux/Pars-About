# Pars About — Çeviri ve Yerelleştirme Kılavuzu (TRANSLATION_GUIDE.md)

`pars-about`, standart **GNU gettext** altyapısını kullanarak çoklu dil ve yerelleştirme (i18n / l10n) desteği sunar.

---

## 1. Dizin ve Dosya Yapısı

* `po/files`: Çevrilebilir dizgelerin taranacağı kaynak dosyaların listesi (`src/MainWindow.py`, `src/Main.py`, `src/widget/HardwareDetailRow.py` vb.).
* `po/pars-about.pot`: Tüm çevrilebilir dizgeleri içeren ana gettext şablon dosyası.
* `po/tr.po`: Türkçe çeviriler.
* `po/pt.po`: Portekizce çeviriler.
* `po/es.po`: İspanyolca çeviriler.
* `po/LINGUAS`: Aktif dillerin kod listesi (`tr pt es`).
* `update-translations.sh`: Şablon ve dil dosyalarını otomatik yenileyen kabuk betiği.
* `fix-po.sh`: Bozuk veya geçersiz dizgeleri onaran bakım betiği.

---

## 2. Çevirileri Güncelleme İş Akışı

1. Kaynak Python veya Glade dosyalarına yeni metinler veya çevrilebilir dizgeler (`_("Metin")`) eklendiğinde:
   ```bash
   ./update-translations.sh
   ```
2. Bu betik:
   - `xgettext` komutunu çalıştırarak `po/pars-about.pot` şablonunu günceller.
   - `msgmerge` aracıyla mevcut `po/*.po` dil dosyalarını yeni şablonla otomatik birleştirir.

3. Eğer dosyalarda sözdizimsel bir sorun oluşursa onarmak için:
   ```bash
   ./fix-po.sh
   ```

---

## 3. Yeni Bir Dil Ekleme

Örneğin Azerbaycan Türkçesi (`az`) veya Almanca (`de`) desteği eklemek için:

1. `update-translations.sh` dosyasındaki `langs` dizisine dil kodunu ekleyin:
   ```bash
   langs=("tr" "pt" "es" "az")
   ```
2. `po/LINGUAS` dosyasına yeni dil kodunu ekleyin:
   ```text
   tr pt es az
   ```
3. Şablon dosyasından yeni bir `.po` dosyası üretin:
   ```bash
   cp po/pars-about.pot po/az.po
   ```
4. **Poedit**, **Gtranslator** veya herhangi bir metin düzenleyici ile `po/az.po` dosyasındaki dizgeleri çevirin.
5. Meson derleme dizininde çevirileri derleyin:
   ```bash
   ninja -C builddir
   ```

---

## 4. Çevirileri Yerel Olarak Test Etme

Uygulamayı sisteme kurmadan belirli bir dil ortamında test etmek için `LANGUAGE` veya `LANG` değişkenini belirterek çalıştırabilirsiniz:

```bash
# Portekizce olarak çalıştırma
LANGUAGE=pt_PT.UTF-8 python3 pars-about.py

# İspanyolca olarak çalıştırma
LANGUAGE=es_ES.UTF-8 python3 pars-about.py

# Türkçe olarak çalıştırma
LANGUAGE=tr_TR.UTF-8 python3 pars-about.py
```
