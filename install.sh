#!/usr/bin/env bash
# Pars About - Hızlı Kurulum Betiği

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"

if [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ "$1" = "help" ]; then
    echo "Pars About - Hızlı Kurulum Aracı"
    echo ""
    echo "Kullanım:"
    echo "  ./install.sh        Uygulamayı Meson & Ninja ile derler ve sisteme (/usr) kurar"
    echo "  ./install.sh help   Bu yardım mesajını gösterir"
    exit 0
fi

exec "$SCRIPT_DIR/manage.sh" install "$@"
