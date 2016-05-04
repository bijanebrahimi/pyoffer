# PyOffer

a Graphical tool to track special offers on the Internet.

## Install (root required)

Note: Installation requires you to install `pyqt5` package first. I hope we can
add it later to setup process, but for now first install it manually and then:

```
$ git clone git@github.com:bijanebrahimi/PyOffer.git
$ cd pyoffer
# python setup.py install
```

By installing the package, `pyoffer-gui` should be available from terminal.

```sh
$ pyoffer-gui
```

## Install Locally (no root required)

It is possible to install pyoffer locally using `virtualenv`. the downside is
you're going to be cut off of global python packages installed already, noticeably
`PyQt5` which is expensive to build into virtualenv. either you also have to install
`PyQt5` into your virtualenv or allow yout virtualenv to have access to outside
packages using `--system-site-packages` argument.

```
$ virtualenv --system-site-packages ~/.pip
$ source ~/.pip/bin/activate
$ git clone git@github.com:bijanebrahimi/pyoffer.git
$ python pyoffer/setup.py install
$ pyoffer-gui
```

To run `pyoffer` from desktop applications, Just
run the following command.

```
$ cat > ~/.local/share/applications/pyoffer.desktop << EOF            
[Desktop Entry]
Encoding=UTF-8
Name=Pyoffer
Comment=Track Free Offers on Internet
Exec=bash -c 'source ~/.pip/bin/activate && pyoffer-gui'
Terminal=false
Type=Application
Categories=Network;
EOF
```

# ScreenShots

![پیشنهاد شگفت‌انگیز دیجی‌کالا](http://bijanebrahimi.github.io/PyOffer/screenshots/digikala-plugin.png)

![packtpub Free Learning](http://bijanebrahimi.github.io/PyOffer/screenshots/packtpub-plugin.png)

## TODO

* Documentation
* MOAR DOCUMENTATION!
* Auto-update
* Desktop Notification
* Sys-Tray Icon

## CHANGELOG

### 0.0.2
- Plugin Interface Introduced

### 0.0.1
- Digikala Special Offers Support Added
- PacktPub Free Learning eBooks Support Added
