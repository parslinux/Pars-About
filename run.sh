#!/usr/bin/env bash
# Pars About - Hızlı Çalıştırma Betiği

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"

if [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ "$1" = "help" ]; then
    echo "Pars About - Hızlı Çalıştırma Aracı"
    echo ""
    echo "Kullanım:"
    echo "  ./run.sh            Grafik arayüzü (GUI) başlatır"
    echo "  ./run.sh --hardware Doğrudan donanım bileşenleri sekmesini açar"
    echo "  ./run.sh --json     Headless CLI modunda JSON çıktısı üretir"
    echo "  ./run.sh help       Bu yardım mesajını gösterir"
    exit 0
fi

exec "$SCRIPT_DIR/manage.sh" run "$@"
