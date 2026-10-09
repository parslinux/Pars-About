project('pars-about')

subdir('po')
subdir('debian')

# install sources
install_subdir('src', install_dir : '/usr/share/pars/pars-about')
install_subdir('data', install_dir : '/usr/share/pars/pars-about')
install_subdir('ui', install_dir : '/usr/share/pars/pars-about')
install_subdir('css', install_dir : '/usr/share/pars/pars-about')
install_subdir('data/icons', install_dir : '/usr/share/icons/hicolor/scalable/devices', strip_directory: true)

# icons
install_data('pars-hardware-info.svg', install_dir : '/usr/share/icons/hicolor/scalable/apps')
install_data('pars-about.svg', install_dir : '/usr/share/icons/hicolor/scalable/apps')
install_data('pars-about-symbolic.svg', install_dir : '/usr/share/icons/hicolor/scalable/apps')

# polkit rule
subdir('polkit')

# desktop files
install_data('org.parslinux.about.desktop', install_dir : '/usr/share/applications/')
install_data('org.parslinux.about-hardware.desktop', install_dir : '/usr/share/applications/')

# command
install_data('pars-about.py', install_dir : '/usr/bin', rename: 'pars-about')

