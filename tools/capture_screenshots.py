#!/usr/bin/env python3
# ==============================================================================
# Pars About - Otomatik Ekran Görüntüsü Yakalama Aracı
# ==============================================================================
# Bu betik Pars About arayüzünü modern Pars Linux teması ile çalıştırarak:
#   1. screenshots/pars-about-1.png (Sistem Özeti)
#   2. screenshots/pars-about-2.png (Donanım Ayrıntıları)
#   3. screenshots/pars-about-3.png (Rapor ve Menü)
# ekran görüntülerini tam piksel kalitesinde otomatik olarak üretir ve günceller.
# ==============================================================================

import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")

sys.path.insert(0, SRC_DIR)

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, Gio
import MainWindow


def main():
    print("Pars About ekran görüntüleri yakalanıyor...")
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    # Koyu tema tercihini aktif et
    settings = Gtk.Settings.get_default()
    settings.set_property("gtk-application-prefer-dark-theme", True)

    app = Gtk.Application.new("org.parslinux.screenshot_capture", Gio.ApplicationFlags.FLAGS_NONE)
    app.register(None)
    app.args = {}

    mw = MainWindow.MainWindow(app)

    # Ekran görüntüsü için şık Pars Linux başlığı
    mw.ui_distro_id_label.set_text("Pars Linux")
    mw.ui_distro_version_label.set_text("2026.1")
    mw.ui_distro_codename_label.set_text("Bilge")

    mw.ui_main_window.show_all()

    # Donanım bilgilerinin yüklenmesini bekle
    print("-> Donanım verilerinin yüklenmesi bekleniyor...")
    start = time.time()
    while time.time() - start < 15:
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        if mw.computer_manager is not None and getattr(mw, "hardware_info", None) is not None:
            for _ in range(20):
                while Gtk.events_pending():
                    Gtk.main_iteration_do(False)
                time.sleep(0.04)
            break
        time.sleep(0.1)

    # Gizlilik için yerel ve genel IP adreslerini maskele
    try:
        if hasattr(mw, "ui_private_ip_label") and mw.ui_private_ip_label:
            mw.ui_private_ip_label.set_text("192.168.1.***")
        if hasattr(mw, "ui_public_ip_label") and mw.ui_public_ip_label:
            mw.ui_public_ip_label.set_text("88.253.***.***")
    except Exception as e:
        print("IP maskeleme notu:", e)

    for _ in range(15):
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        time.sleep(0.02)

    gdk_win = mw.ui_main_window.get_window()
    w, h = gdk_win.get_width(), gdk_win.get_height()

    # --------------------------------------------------------------------------
    # 1. Sistem Özeti (pars-about-1.png)
    # --------------------------------------------------------------------------
    shot1_path = os.path.join(SCREENSHOTS_DIR, "pars-about-1.png")
    pix1 = Gdk.pixbuf_get_from_window(gdk_win, 0, 0, w, h)
    pix1.savev(shot1_path, "png", [], [])
    print(f"✓ 1/3 Kaydedildi: {shot1_path} ({w}x{h})")

    # --------------------------------------------------------------------------
    # 2. Donanım Ayrıntıları (pars-about-2.png)
    # --------------------------------------------------------------------------
    mw.ui_info_stack.set_visible_child_name("hardware_details")
    mw.ui_hardware_info_button.set_label("Show Summary")

    # İlk 4 donanım kategorisini aç (Genişletilmiş görünüm)
    for row in mw.ui_hardware_details_box.get_children()[:4]:
        if hasattr(row, "revealer") and row.revealer:
            row.revealer.set_reveal_child(True)

    for _ in range(30):
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        time.sleep(0.03)

    shot2_path = os.path.join(SCREENSHOTS_DIR, "pars-about-2.png")
    w, h = gdk_win.get_width(), gdk_win.get_height()
    pix2 = Gdk.pixbuf_get_from_window(gdk_win, 0, 0, w, h)
    pix2.savev(shot2_path, "png", [], [])
    print(f"✓ 2/3 Kaydedildi: {shot2_path} ({w}x{h})")

    # --------------------------------------------------------------------------
    # 3. Rapor ve Teşhis Menüsü (pars-about-3.png)
    # --------------------------------------------------------------------------
    mw.ui_popover_menu.popup()

    for _ in range(30):
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        time.sleep(0.03)

    shot3_path = os.path.join(SCREENSHOTS_DIR, "pars-about-3.png")
    w, h = gdk_win.get_width(), gdk_win.get_height()
    pix3 = Gdk.pixbuf_get_from_window(gdk_win, 0, 0, w, h)
    pix3.savev(shot3_path, "png", [], [])
    print(f"✓ 3/3 Kaydedildi: {shot3_path} ({w}x{h})")

    mw.ui_main_window.destroy()
    print("\n🎉 Tüm ekran görüntüleri başarıyla güncellendi!")


if __name__ == "__main__":
    main()
