#!/usr/bin/env bash

set -e

echo "PO dosyaları güncelleniyor..."

find po -type f \( -name "*.po" -o -name "*.pot" \) | while read -r file
do
    sed -i \
        -e 's/Pardus About/Pars About/g' \
        -e 's/Pardus Linux/Pars Linux/g' \
        -e 's/PARDUS/PARS/g' \
        -e 's/Pardus/Pars Linux/g' \
        "$file"

    echo "✓ $file"
done

echo "Tamamlandı."
