#!/usr/bin/env bash
# Pars About - Hızlı Kaldırma Betiği

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"

if [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ "$1" = "help" ]; then
    echo "Pars About - Hızlı Kaldırma Aracı"
    echo ""
    echo "Kullanım:"
    echo "  ./uninstall.sh      Uygulamayı ve ilgili tüm masaüstü / ikon dosyalarını sistemden temizler"
    echo "  ./uninstall.sh help Bu yardım mesajını gösterir"
    exit 0
fi

exec "$SCRIPT_DIR/manage.sh" uninstall "$@"
