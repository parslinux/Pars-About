#!/usr/bin/env bash
# ==============================================================================
# Pars About - Yönetim, Çalıştırma, Kurulum, Kaldırma ve Paketleme Betiği
# ==============================================================================
# Bu betik Pars About uygulamasının yerel olarak çalıştırılması, sisteme
# kurulması, kaldırılması, paketlenmesi ve test edilmesini sağlar.
# ==============================================================================

set -e

# Betiğin bulunduğu proje ana dizinine geçiş yap
PROJECT_ROOT="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
cd "$PROJECT_ROOT"

# Renkler ve Biçimlendirme
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Log ve Bilgilendirme Fonksiyonları
log_info() {
    echo -e "${CYAN}[BİLGİ]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[BAŞARILI]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[UYARI]${NC} $1"
}

log_error() {
    echo -e "${RED}[HATA]${NC} $1" >&2
}

log_step() {
    echo -e "\n${BOLD}${BLUE}==> $1${NC}"
}

# Root/Sudo yetkisi kontrolü
get_sudo() {
    if [ "$EUID" -ne 0 ]; then
        if command -v sudo >/dev/null 2>&1; then
            echo "sudo"
        else
            log_error "Root yetkisi gerekiyor ancak 'sudo' komutu bulunamadı!"
            exit 1
        fi
    else
        echo ""
    fi
}

# Dağıtım Tespiti
detect_distro() {
    if [ -f /etc/os-release ]; then
        # shellcheck disable=SC1091
        . /etc/os-release
        if [[ "$ID" =~ (arch|cachyos|manjaro|endeavouros|artix|parslinux) ]] || [[ "$ID_LIKE" =~ arch ]]; then
            echo "arch"
        elif [[ "$ID" =~ (debian|ubuntu|linuxmint|pop|elementary) ]] || [[ "$ID_LIKE" =~ (debian|ubuntu) ]]; then
            echo "debian"
        elif [[ "$ID" =~ (fedora|rhel|centos) ]] || [[ "$ID_LIKE" =~ fedora ]]; then
            echo "fedora"
        else
            echo "unknown"
        fi
    else
        echo "unknown"
    fi
}

# ------------------------------------------------------------------------------
# 1. ÇALIŞTIRMA (RUN)
# ------------------------------------------------------------------------------
check_python_deps() {
    local missing=()
    python3 -c "import gi" 2>/dev/null || missing+=("python-gobject (gi)")
    python3 -c "import requests" 2>/dev/null || missing+=("python-requests")
    python3 -c "import cairosvg" 2>/dev/null || missing+=("python-cairosvg")
    python3 -c "import cups" 2>/dev/null || missing+=("pycups (cups)")

    if [ ${#missing[@]} -gt 0 ]; then
        log_warn "Eksik Python modülleri tespit edildi: ${missing[*]}"
        local distro
        distro=$(detect_distro)
        log_info "Bu modüller olmadan uygulama çalıştırılamaz."
        if [ "$distro" = "arch" ]; then
            echo -e "  ${CYAN}Önerilen kurulum komutu:${NC} ${BOLD}sudo pacman -S --needed python-requests python-cairosvg pycups${NC}"
        elif [ "$distro" = "debian" ]; then
            echo -e "  ${CYAN}Önerilen kurulum komutu:${NC} ${BOLD}sudo apt install python3-requests python3-cairosvg python3-cups${NC}"
        fi
        echo ""
        read -r -p "Eksik bağımlılıklar şimdi otomatik kurulsun mu? [E/h]: " confirm
        confirm=${confirm:-E}
        if [[ "$confirm" =~ ^[eEyY] ]]; then
            do_check_deps
        else
            log_error "Gerekli bağımlılıklar kurulmadan devam edilemez."
            exit 1
        fi
    fi
}

do_run() {
    log_step "Pars About başlatılıyor (Kaynak koddan)..."
    if [ ! -f "pars-about.py" ]; then
        log_error "pars-about.py dosyası bulunamadı!"
        exit 1
    fi
    check_python_deps
    exec python3 pars-about.py "$@"
}

do_run_hw() {
    log_step "Pars About doğrudan Donanım sekmesinde başlatılıyor..."
    exec python3 pars-about.py --hardware "$@"
}

do_run_json() {
    log_step "Pars About Headless CLI (JSON) modunda çalıştırılıyor..."
    python3 pars-about.py --json "$@"
}

# ------------------------------------------------------------------------------
# 2. BAĞIMLILIK KONTROLÜ VE KURULUMU (DEPS)
# ------------------------------------------------------------------------------
do_check_deps() {
    log_step "Sistem bağımlılıkları kontrol ediliyor..."
    local distro
    distro=$(detect_distro)
    local SUDO
    SUDO=$(get_sudo)

    case "$distro" in
        arch)
            log_info "Tespit edilen dağıtım ailesi: Arch Linux / CachyOS / Pars Linux"
            local deps=(
                python python-gobject python-requests python-cairosvg pycups
                gtk3 glib2 libgudev libsoup3 mesa-utils pciutils lsb-release
                hwdata dconf polkit meson ninja gettext
            )
            local missing=()
            for pkg in "${deps[@]}"; do
                if ! pacman -Q "$pkg" >/dev/null 2>&1; then
                    missing+=("$pkg")
                fi
            done

            if [ ${#missing[@]} -eq 0 ]; then
                log_success "Tüm gerekli paketler sistemde kurulu!"
            else
                log_warn "Eksik paketler tespit edildi: ${missing[*]}"
                read -r -p "Eksik paketler şimdi pacman ile kurulsun mu? [E/h]: " confirm
                confirm=${confirm:-E}
                if [[ "$confirm" =~ ^[eEyY] ]]; then
                    $SUDO pacman -Syu --needed "${missing[@]}"
                    log_success "Bağımlılıklar başarıyla kuruldu."
                fi
            fi
            ;;
        debian)
            log_info "Tespit edilen dağıtım ailesi: Debian / Ubuntu"
            local deps=(
                python3 python3-gi python3-requests python3-cairosvg python3-cups
                gir1.2-gtk-3.0 gir1.2-glib-2.0 gir1.2-gudev-1.0 gir1.2-soup-2.4
                mesa-utils pciutils lsb-release hwdata dconf-cli pkexec
                meson ninja-build gettext
            )
            local missing=()
            for pkg in "${deps[@]}"; do
                if ! dpkg -s "$pkg" >/dev/null 2>&1; then
                    missing+=("$pkg")
                fi
            done

            if [ ${#missing[@]} -eq 0 ]; then
                log_success "Tüm gerekli paketler sistemde kurulu!"
            else
                log_warn "Eksik paketler tespit edildi: ${missing[*]}"
                read -r -p "Eksik paketler şimdi apt ile kurulsun mu? [E/h]: " confirm
                confirm=${confirm:-E}
                if [[ "$confirm" =~ ^[eEyY] ]]; then
                    $SUDO apt update
                    $SUDO apt install -y "${missing[@]}"
                    log_success "Bağımlılıklar başarıyla kuruldu."
                fi
            fi
            ;;
        *)
            log_warn "Bilinmeyen veya doğrudan desteklenmeyen dağıtım ($distro)."
            log_info "Gereken temel araçlar kontrol ediliyor..."
            for cmd in python3 meson ninja msgfmt pkexec; do
                if command -v "$cmd" >/dev/null 2>&1; then
                    echo -e "  ✓ $cmd bulundu"
                else
                    echo -e "  ✗ $cmd BULUNAMADI!"
                fi
            done
            ;;
    esac
}

# ------------------------------------------------------------------------------
# 3. SİSTEME KURMA (INSTALL)
# ------------------------------------------------------------------------------
do_install() {
    log_step "Pars About sisteme kuruluyor (/usr)..."
    local SUDO
    SUDO=$(get_sudo)

    if ! command -v meson >/dev/null 2>&1 || ! command -v ninja >/dev/null 2>&1; then
        log_error "Meson veya Ninja bulunamadı! Lütfen önce bağımlılıkları kurun."
        exit 1
    fi

    # Meson build directory kontrolü ve yapılandırma
    if [ ! -d "builddir" ]; then
        log_info "Meson yapılandırması hazırlanıyor (builddir)..."
        meson setup builddir --prefix=/usr
    else
        log_info "Mevcut builddir yeniden yapılandırılıyor..."
        meson setup --reconfigure builddir --prefix=/usr
    fi

    log_info "Bileşenler derleniyor (Ninja)..."
    ninja -C builddir

    log_info "Sistem dizinlerine yükleniyor (Sudo yetkisi gerekebilir)..."
    $SUDO ninja -C builddir install

    log_info "Masaüstü ve ikon önbellekleri yenileniyor..."
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        $SUDO gtk-update-icon-cache -qtf /usr/share/icons/hicolor 2>/dev/null || true
    fi
    if command -v update-desktop-database >/dev/null 2>&1; then
        $SUDO update-desktop-database -q /usr/share/applications 2>/dev/null || true
    fi

    log_success "Pars About sisteme başarıyla kuruldu!"
    log_info "Uygulamayı başlatmak için uçbirimden 'pars-about' komutunu çalıştırabilir veya uygulama menüsünden erişebilirsiniz."
}

# ------------------------------------------------------------------------------
# 4. SİSTEMDEN KALDIRMA (UNINSTALL)
# ------------------------------------------------------------------------------
do_uninstall() {
    log_step "Pars About sistemden kaldırılıyor..."
    local SUDO
    SUDO=$(get_sudo)

    # 1. Eğer builddir varsa önce ninja ile kaldır
    if [ -d "builddir" ] && [ -f "builddir/build.ninja" ]; then
        log_info "Ninja üzerinden kaldırma işlemi yürütülüyor..."
        $SUDO ninja -C builddir uninstall || true
    fi

    log_info "Kalan dosyalar ve dizinler denetlenip temizleniyor..."
    $SUDO rm -rf "/usr/share/pars/pars-about"
    $SUDO rm -f "/usr/bin/pars-about"
    $SUDO rm -f "/usr/share/applications/org.parslinux.about.desktop"
    $SUDO rm -f "/usr/share/applications/org.parslinux.about-hardware.desktop"
    $SUDO rm -f "/usr/share/metainfo/org.parslinux.about.metainfo.xml"
    $SUDO rm -f "/usr/share/polkit-1/actions/org.parslinux.pkexec.pars-about.policy"
    $SUDO rm -f "/usr/share/polkit-1/rules.d/org.parslinux.about.rules"
    $SUDO rm -f "/usr/share/icons/hicolor/scalable/apps/pars-about.svg"
    $SUDO rm -f "/usr/share/icons/hicolor/scalable/apps/pars-about-symbolic.svg"
    $SUDO rm -f "/usr/share/icons/hicolor/scalable/apps/pars-hardware-info.svg"

    # data/icons altındaki cihaz ikonlarını temizle
    if [ -d "data/icons" ]; then
        for icon in data/icons/*.svg; do
            icon_name=$(basename "$icon")
            $SUDO rm -f "/usr/share/icons/hicolor/scalable/devices/$icon_name"
        done
    fi

    # Yerelleştirme (.mo) dosyalarını temizle
    $SUDO rm -f /usr/share/locale/*/LC_MESSAGES/pars-about.mo

    log_info "Önbellekler güncelleniyor..."
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        $SUDO gtk-update-icon-cache -qtf /usr/share/icons/hicolor 2>/dev/null || true
    fi
    if command -v update-desktop-database >/dev/null 2>&1; then
        $SUDO update-desktop-database -q /usr/share/applications 2>/dev/null || true
    fi

    log_success "Pars About sistemden tamamen kaldırıldı."
}

# ------------------------------------------------------------------------------
# 5. PAKETLEME (PACKAGE)
# ------------------------------------------------------------------------------
do_package_arch() {
    log_step "Arch Linux / Pars Linux paketi (.pkg.tar.zst) hazırlanıyor..."
    if ! command -v makepkg >/dev/null 2>&1; then
        log_error "'makepkg' komutu bulunamadı! Bu işlem Arch tabanlı bir sistemde çalıştırılmalıdır."
        return 1
    fi

    if [ ! -f "PKGBUILD" ]; then
        log_error "Proje kök dizininde PKGBUILD bulunamadı!"
        return 1
    fi

    mkdir -p dist
    local arch_builddir="/tmp/pars-about-makepkg"
    rm -rf "$arch_builddir"
    mkdir -p "$arch_builddir"

    log_info "Paketleme işlemi izole ortamda ($arch_builddir) yürütülüyor..."
    BUILDDIR="$arch_builddir" PKGDEST="$PROJECT_ROOT/dist" SRCDEST="$arch_builddir" SRCPKGDEST="$PROJECT_ROOT/dist" makepkg -f --nodeps

    log_success "Arch paketi başarıyla oluşturuldu:"
    ls -lh dist/pars-about-*.pkg.tar.* 2>/dev/null || true
    rm -rf "$arch_builddir"
}

do_package_deb() {
    log_step "Debian / Ubuntu paketi (.deb) hazırlanıyor..."
    if ! command -v dpkg-buildpackage >/dev/null 2>&1; then
        log_error "'dpkg-buildpackage' bulunamadı! Lütfen 'dpkg-dev' paketini kurun."
        return 1
    fi

    if [ ! -d "debian" ]; then
        log_error "debian/ dizini bulunamadı!"
        return 1
    fi

    log_info "dpkg-buildpackage çalıştırılıyor..."
    dpkg-buildpackage -b -uc -us

    mkdir -p dist
    cp ../pars-about_*.deb dist/ 2>/dev/null || true
    log_success "Debian paketi başarıyla oluşturuldu:"
    ls -lh dist/pars-about_*.deb 2>/dev/null || ls -lh ../pars-about_*.deb 2>/dev/null || true
}

do_package_tar() {
    log_step "Kaynak kod arşiv paketi (.tar.gz) oluşturuluyor..."
    local version="0.1.0"
    if [ -f "__version__" ]; then
        version=$(cat __version__ | tr -d ' \n\r')
    fi

    mkdir -p dist
    local tarname="dist/pars-about-${version}.tar.gz"
    
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        log_info "Git arşivi kullanılarak temiz tarball üretiliyor..."
        git archive --format=tar.gz --prefix="pars-about-${version}/" HEAD -o "$tarname"
    else
        log_info "Dizin sıkıştırılıyor..."
        tar --exclude='./dist' --exclude='./builddir' --exclude='./.git' \
            --exclude='*__pycache__*' -czf "$tarname" -C .. "$(basename "$PROJECT_ROOT")"
    fi

    log_success "Kaynak paketi hazırlandı: $tarname"
}

do_package() {
    local distro
    distro=$(detect_distro)

    case "$distro" in
        arch)
            do_package_arch
            ;;
        debian)
            do_package_deb
            ;;
        *)
            log_info "Sisteminiz için uygun paket türünü seçin veya kaynak arşivi oluşturun."
            echo "1) Arch Linux (.pkg.tar.zst)"
            echo "2) Debian (.deb)"
            echo "3) Kaynak Arşivi (.tar.gz)"
            read -r -p "Seçiminiz [1-3]: " pkg_choice
            case "$pkg_choice" in
                1) do_package_arch ;;
                2) do_package_deb ;;
                3) do_package_tar ;;
                *) log_error "Geçersiz seçim!" ;;
            esac
            ;;
    esac
}

# ------------------------------------------------------------------------------
# 6. TEST VE TEMİZLİK (TEST & CLEAN)
# ------------------------------------------------------------------------------
do_test() {
    log_step "Proje birim ve doğrulama testleri yürütülüyor..."
    if [ -f "tests/run_all_tests.py" ]; then
        python3 tests/run_all_tests.py
    else
        log_error "tests/run_all_tests.py dosyası bulunamadı!"
        exit 1
    fi
}

do_clean() {
    log_step "Derleme kalıntıları ve geçici dosyalar temizleniyor..."
    rm -rf builddir dist test_builddir pkg
    rm -f *.pkg.tar.zst *.pkg.tar.xz *.pkg.tar.gz *.deb *.buildinfo *.changes
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    log_success "Temizlik tamamlandı."
}

do_capture_screenshots() {
    log_step "Ekran görüntüleri otomatik olarak yakalanıyor..."
    if [ -f "tools/capture_screenshots.py" ]; then
        python3 tools/capture_screenshots.py
    else
        log_error "tools/capture_screenshots.py bulunamadı!"
        exit 1
    fi
}

# ------------------------------------------------------------------------------
# YARDIM VE KULLANIM BİLGİSİ
# ------------------------------------------------------------------------------
show_help() {
    echo -e "${BOLD}${MAGENTA}Pars About Yönetim Aracı${NC}"
    echo -e "Kullanım: ${CYAN}./manage.sh [KOMUT] [SEÇENEKLER]${NC}\n"
    echo -e "${BOLD}Mevcut Komutlar:${NC}"
    echo -e "  ${GREEN}run, start${NC}             Uygulamayı kaynak koddan GUI modunda başlatır"
    echo -e "  ${GREEN}run-hw, hw${NC}             Uygulamayı doğrudan donanım sekmesinde başlatır"
    echo -e "  ${GREEN}run-json, json${NC}         Headless CLI modunda JSON çıktısı üretir"
    echo -e "  ${GREEN}deps, check-deps${NC}       Sistem bağımlılıklarını kontrol eder / kurar"
    echo -e "  ${GREEN}install${NC}                Meson + Ninja ile sisteme (/usr) kurar"
    echo -e "  ${GREEN}uninstall${NC}              Sistemden tamamen kaldırır"
    echo -e "  ${GREEN}package${NC}                Dağıtıma göre paket oluşturur (Arch / Debian)"
    echo -e "  ${GREEN}package-arch${NC}           Arch Linux paketi (.pkg.tar.zst) oluşturur"
    echo -e "  ${GREEN}package-deb${NC}            Debian paketi (.deb) oluşturur"
    echo -e "  ${GREEN}package-tar${NC}            Kaynak kod arşivi (.tar.gz) oluşturur"
    echo -e "  ${GREEN}screenshots, capture${NC}   Uygulamanın yeni ekran görüntülerini otomatik çeker"
    echo -e "  ${GREEN}test${NC}                   Test paketini çalıştırır"
    echo -e "  ${GREEN}clean${NC}                  Derleme ve önbellek artıklarını temizler"
    echo -e "  ${GREEN}help, -h, --help${NC}       Bu yardım mesajını gösterir\n"
    echo -e "${BOLD}Not:${NC} Hiçbir argüman vermeden çalıştırırsanız interaktif menü açılır."
}

# ------------------------------------------------------------------------------
# İNTERAKTİF MENÜ
# ------------------------------------------------------------------------------
interactive_menu() {
    while true; do
        clear 2>/dev/null || true
        echo -e "${BOLD}${CYAN}=====================================================${NC}"
        echo -e "${BOLD}${MAGENTA}           PARS ABOUT YÖNETİM MERKEZİ                ${NC}"
        echo -e "${BOLD}${CYAN}=====================================================${NC}"
        echo -e " ${BOLD}1)${NC} ${GREEN}Çalıştır${NC} (GUI Arayüz Modu)"
        echo -e " ${BOLD}2)${NC} ${GREEN}Çalıştır${NC} (Donanım Sekmesi - Hardware)"
        echo -e " ${BOLD}3)${NC} ${GREEN}Çalıştır${NC} (Headless CLI - JSON Çıktısı)"
        echo -e " ${BOLD}4)${NC} ${YELLOW}Bağımlılıkları Kontrol Et ve Kur${NC}"
        echo -e " ${BOLD}5)${NC} ${BLUE}Sisteme Kur${NC} (Meson / Ninja -> /usr)"
        echo -e " ${BOLD}6)${NC} ${RED}Sistemden Kaldır${NC} (Uninstall)"
        echo -e " ${BOLD}7)${NC} ${CYAN}Paketle (Arch Linux: .pkg.tar.zst)${NC}"
        echo -e " ${BOLD}8)${NC} ${CYAN}Paketle (Debian / Ubuntu: .deb)${NC}"
        echo -e " ${BOLD}9)${NC} ${CYAN}Kaynak Arşivi Oluştur (.tar.gz)${NC}"
        echo -e " ${BOLD}10)${NC} ${MAGENTA}Testleri Çalıştır (run_all_tests.py)${NC}"
        echo -e " ${BOLD}11)${NC} ${YELLOW}Temizlik Yap (builddir ve önbellekler)${NC}"
        echo -e " ${BOLD}12)${NC} ${GREEN}Ekran Görüntülerini Otomatik Güncelle (PNG)${NC}"
        echo -e " ${BOLD}0)${NC} Çıkış"
        echo -e "${BOLD}${CYAN}=====================================================${NC}"
        read -r -p "Lütfen bir işlem seçin [0-12]: " choice
        echo ""

        case "$choice" in
            1) do_run ;;
            2) do_run_hw ;;
            3) do_run_json ;;
            4) do_check_deps ;;
            5) do_install ;;
            6) do_uninstall ;;
            7) do_package_arch ;;
            8) do_package_deb ;;
            9) do_package_tar ;;
            10) do_test ;;
            11) do_clean ;;
            12) do_capture_screenshots ;;
            0)
                log_info "Çıkış yapılıyor. İyi çalışmalar!"
                exit 0
                ;;
            *)
                log_warn "Geçersiz seçenek!"
                ;;
        esac

        echo ""
        read -r -p "Menüye dönmek için Enter tuşuna basın..." _
    done
}

# ------------------------------------------------------------------------------
# ANA ÇAĞRI MANTIĞI
# ------------------------------------------------------------------------------
if [ $# -eq 0 ]; then
    interactive_menu
else
    case "$1" in
        run|start)
            shift
            do_run "$@"
            ;;
        run-hw|hw|--hardware|-h)
            shift
            do_run_hw "$@"
            ;;
        run-json|json|--json|-j)
            shift
            do_run_json "$@"
            ;;
        deps|check-deps)
            do_check_deps
            ;;
        install)
            do_install
            ;;
        uninstall)
            do_uninstall
            ;;
        package)
            shift
            if [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
                echo -e "${BOLD}${MAGENTA}Pars About Paketleme${NC}"
                echo -e "Kullanım: ${CYAN}./manage.sh package [arch|deb|tar]${NC}"
                echo -e "  ${GREEN}arch${NC}  Arch Linux (.pkg.tar.zst) paketi oluşturur"
                echo -e "  ${GREEN}deb${NC}   Debian/Ubuntu (.deb) paketi oluşturur"
                echo -e "  ${GREEN}tar${NC}   Kaynak kod (.tar.gz) arşivi oluşturur"
                echo -e "  (boş)  Dağıtıma göre otomatik belirler"
                exit 0
            elif [ "$1" = "arch" ]; then
                do_package_arch
            elif [ "$1" = "deb" ]; then
                do_package_deb
            elif [ "$1" = "tar" ]; then
                do_package_tar
            else
                do_package
            fi
            ;;
        package-arch)
            do_package_arch
            ;;
        package-deb)
            do_package_deb
            ;;
        package-tar)
            do_package_tar
            ;;
        screenshots|screenshot|capture)
            do_capture_screenshots
            ;;
        test)
            do_test
            ;;
        clean)
            do_clean
            ;;
        help|--help)
            show_help
            ;;
        *)
            log_error "Bilinmeyen komut: $1"
            show_help
            exit 1
            ;;
    esac
fi
