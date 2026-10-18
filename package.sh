#!/usr/bin/env bash
# Pars About - Hızlı Paketleme Betiği

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"

if [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ "$1" = "help" ]; then
    echo "Pars About - Hızlı Paketleme Aracı"
    echo ""
    echo "Kullanım:"
    echo "  ./package.sh         Sistem dağıtımına göre uygun paketi oluşturur"
    echo "  ./package.sh arch    Arch Linux paketi (.pkg.tar.zst) oluşturur"
    echo "  ./package.sh deb     Debian / Ubuntu paketi (.deb) oluşturur"
    echo "  ./package.sh tar     Temiz kaynak kod arşivi (.tar.gz) oluşturur"
    echo "  ./package.sh help    Bu yardım mesajını gösterir"
    exit 0
fi

exec "$SCRIPT_DIR/manage.sh" package "$@"
