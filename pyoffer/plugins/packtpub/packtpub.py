# From Python
import os
import re
import json
import requests
import webbrowser
from threading import Thread, Lock
from datetime import datetime, timedelta
# From PyQyeru
from pyquery import PyQuery as pq
# From PyQt5
from PyQt5.uic import loadUi
# From PyOffer
from pyoffer.libs.plugin import Plugin, PluginWidget, PluginModel
from pyoffer.libs.widgets import QRemoteImage


class PacktpubModel(PluginModel):
    """docstring for PacktpubModel"""
    def __init__(self):
        super(PacktpubModel, self).__init__()
        self.api = 'https://www.packtpub.com/packt/offers/free-learning'
        self.lock = Lock()
        self.title = ""
        self.cover_url = ""
        self.claim_url = ""
        self.expire_datetime = ""

    def update(self):
        thread = Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        with self.lock:
            self.notifyUpdating()
            try:
                dom = pq(url='https://www.packtpub.com/packt/offers/free-learning',
                         opener=lambda url, **kw: requests.get(url).content)
                title = dom('.dotd-title h2')[0].text.strip()
                relative_claim_url = dom("a.twelve-days-claim")[0].attrib['href']
                claim_url = "https://www.packtpub.com%s" % relative_claim_url
                cover_url = 'http:' + dom(".dotd-main-book-image a noscript img.bookimage")[0].attrib['src']
                expire_timestamp = int(dom('.packt-js-countdown')[0].attrib['data-countdown-to'])
                expire_datetime = datetime.fromtimestamp(expire_timestamp)
                self.title = title
                self.cover_url = cover_url
                self.claim_url = claim_url
                self.expire_datetime = expire_datetime
                self.notifyChange()
            except Exception as e:
                pass
            self.notifyUpdated()


    def getTitle(self):
        return self.title

    def getCoverUrl(self):
        return self.cover_url

    def getClaimUrl(self):
        return self.claim_url

    def getExpirationFormat(self):
        return self.expire_datetime.strftime("%A, %d %B %H:%M")


class PacktpubWidget(PluginWidget):
    """docstring for PacktpubWidget"""
    def __init__(self):
        super(PacktpubWidget, self).__init__()
        self.model = PacktpubModel()
        self.model.registerChange(self)
        self.model.registerUpdated(self)
        self.model.registerUpdating(self)

    def setupUi(self):
        ui_path = os.path.join(os.path.dirname(__file__), 'packtpub.ui')
        self.ui = loadUi(ui_path, self)
        self.ui.titleLabel.setText("")
        self.ui.expireLabel.setText("")
        self.ui.coverLabel.setText("")

    def setupConnections(self):
        self.ui.updateButton.clicked.connect(self.updateClicked)
        self.ui.claimButton.clicked.connect(self.claimClicked)

    def updateClicked(self):
        self.model.update()

    def modelChanged(self):
        self.ui.titleLabel.setText(self.model.getTitle())
        self.ui.expireLabel.setText('Expires at %s' % self.model.getExpirationFormat())
        cover_image = QRemoteImage.getInstance(self.model.getCoverUrl(), self.ui.coverLabel)
        cover_image.update()

    def modelUpdating(self):
        self.ui.claimButton.setEnabled(False)
        self.ui.updateButton.setEnabled(False)

    def modelUpdated(self):
        if self.model.getClaimUrl():
            self.ui.claimButton.setEnabled(True)
        else:
            self.ui.claimButton.setEnabled(False)
        self.ui.updateButton.setEnabled(True)

    def claimClicked(self):
        if self.model.getClaimUrl():
            webbrowser.open(self.model.getClaimUrl())


class PacktpubPlugin(Plugin):
    """docstring for PacktpubPlugin"""
    def __init__(self):
        super(PacktpubPlugin, self).__init__()
        self.widget = PacktpubWidget()

    def getWidget(self):
        return self.widget
