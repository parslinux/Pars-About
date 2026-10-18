# Pars About — Kurumsal Dağıtım ve Kendi Sunucunda Barındırma Kılavuzu (SELF_HOSTING_GUIDE.md)

Bu kılavuz, kurumsal ağlarda, veri merkezlerinde veya eğitim kurumlarında **Pars About** uygulamasını merkezi olarak dağıtma, yerel depolardan sunma ve `pars-about --json` ile merkezi donanım envanteri toplama yöntemlerini açıklar.

---

## 1. Merkezi Donanım Envanteri Toplama (Fleet Inventory)

`pars-about --json` komutu ekran sunucusu gerektirmediğinden (headless), kurum içindeki yüzlerce istemci veya sunucunun donanım özellikleri tek bir merkezde toplanabilir.

### 1.1. SSH Üzerinden Uzaktan Envanter Çekme
```bash
ssh yonetici@istemci-01 "pars-about --json" > /srv/envanter/istemci-01.json
```

### 1.2. Ansible ile Otomatik Toplama Örneği
Bir Ansible playbook (`envanter.yml`) ile tüm filonun donanımını çekebilirsiniz:

```yaml
- name: Pars Linux Donanim Envanterini Topla
  hosts: all
  tasks:
    - name: Pars About JSON Ciktisini Al
      ansible.builtin.command: pars-about --json
      register: hardware_report
      changed_when: false

    - name: Raporu Yonetim Sunucusuna Kaydet
      ansible.builtin.copy:
        content: "{{ hardware_report.stdout }}"
        dest: "/srv/envanter/{{ inventory_hostname }}.json"
      delegate_to: localhost
```

---

## 2. Yerel Ağda APT / Debian Deposu Kurma

Kurum içi ağda internet erişimi kısıtlıysa veya özel Pars About paketleri dağıtılmak isteniyorsa:

```bash
# 1. Depo dizini oluşturma
mkdir -p /srv/parslinux-depo
cp ../pars-about_*.deb /srv/parslinux-depo/

# 2. Paket indeksini üretme
cd /srv/parslinux-depo
dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz

# 3. HTTP sunucusu başlatma
python3 -m http.server 8080 --directory /srv/parslinux-depo
```

İstemci bilgisayarlarda `/etc/apt/sources.list.d/kurumsal.list`:
```text
deb [trusted=yes] http://yerel-sunucu-ip:8080/ ./
```

---

## 3. İzole ve Güvenli (Air-Gapped) Ortamlar

Pars About hiçbir harici bulut servisine veya telemetri sunucusuna bağımlı değildir. Tamamen internetten yalıtılmış yüksek güvenlikli tesislerde ve askeri/endüstriyel ağlarda güvenle çalıştırılabilir.
