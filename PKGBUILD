# Maintainer: Pars Linux Developers <dev@parslinux.org>
pkgname=pars-about
pkgver=0.1.0_alpha
pkgrel=1
pkgdesc="Pars Linux system summary and comprehensive hardware information viewer"
arch=('any')
url="https://github.com/parslinux/Pars-About"
license=('GPL-3.0-or-later')
depends=(
    'python'
    'python-gobject'
    'gtk3'
    'python-requests'
    'python-cairosvg'
    'pycups'
    'libgudev'
    'libsoup3'
    'mesa-utils'
    'pciutils'
    'lsb-release'
    'hwdata'
    'dconf'
    'polkit'
)
makedepends=(
    'meson'
    'ninja'
    'gettext'
)
source=("$pkgname-$pkgver.tar.gz::https://github.com/parslinux/Pars-About/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$srcdir/$pkgname-$pkgver" 2>/dev/null || cd "$startdir"
    meson setup builddir --prefix=/usr
    ninja -C builddir
}

package() {
    cd "$srcdir/$pkgname-$pkgver" 2>/dev/null || cd "$startdir"
    DESTDIR="$pkgdir" ninja -C builddir install
}
