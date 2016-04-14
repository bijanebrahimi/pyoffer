# From Python
import os
import re
import json
import requests
import webbrowser
from datetime import datetime, timedelta
# From Yapsi
from yapsy.IPlugin import IPlugin
# From PyQyeru
from pyquery import PyQuery as pq
# From PyQt5
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap

class Packtpub(object):
    """docstring for Packtpub"""
    def __init__(self):
        super(Packtpub, self).__init__()
        self.__url = 'https://www.packtpub.com/packt/offers/free-learning'
        self.__cache_dir = '/tmp/packtpub'
        if not os.path.exists(self.__cache_dir):
            os.mkdir(self.__cache_dir)

    def update(self):
        dom = pq(url='https://www.packtpub.com/packt/offers/free-learning',
                 opener=lambda url, **kw: requests.get(url).content)
        img = dom(".dotd-main-book-image a noscript img.bookimage")[0]
        timestamp = int(dom('.packt-js-countdown')[0].attrib['data-countdown-to'])
        link = dom("a.twelve-days-claim")[0]
        href = link.attrib['href']
        url = 'https://www.packtpub.com%s' % href
        expires = datetime.fromtimestamp(timestamp)


        image_src = 'http:' + img.attrib['src']
        image_basename = os.path.basename(image_src)
        image_path = os.path.join(self.__cache_dir, image_basename)
        if not os.path.exists(image_path):
            with open(image_path, 'wb') as f:
                response = requests.get(image_src)
                f.write(response.content)
        return image_path, url, expires


class PacktpubWidget(QWidget):
    """docstring for PacktpubWidget"""
    def __init__(self):
        super(PacktpubWidget, self).__init__()
        self.__packtpub = Packtpub()
        self.setupUi()
        self.setupConnections()

    def setupUi(self):
        ui_path = os.path.join(os.path.dirname(__file__), 'packtpub.ui')
        loadUi(ui_path, self)

    def setupConnections(self):
        self.updateBtn.clicked.connect(self.updateClicked)
        self.openBtn.clicked.connect(self.openClicked)

    def updateClicked(self):
        image_path, url, expire_datetime = self.__packtpub.update()
        self.url = url
        self.openBtn.setEnabled(True)
        if image_path:
            self.image.setPixmap(QPixmap(image_path))
        self.expire.setText(expire_datetime.strftime('%A %d %B %H:%M'))

    def openClicked(self):
        # Download PDF directly?
        # book_id = re.search(r"https://www.packtpub.com/freelearning-claim/(\d+)/\d+", self.url).groups()[0]
        # url = "https://www.packtpub.com/ebook_download/%s/pdf" % book_id
        webbrowser.open(self.url)

class PacktpubPlugin(IPlugin):
    """docstring for PacktpubPlugin"""
    def __init__(self):
        super(PacktpubPlugin, self).__init__()
        self.widget = PacktpubWidget()
