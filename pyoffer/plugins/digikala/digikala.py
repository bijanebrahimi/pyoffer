# From Python
import os
import re
import json
import requests
import webbrowser
from threading import Thread, Lock
from dateutil import parser, tz
from datetime import datetime
# From PyQt5
from PyQt5.uic import loadUi
# From PyOffer
from pyoffer.libs.plugin import Plugin, PluginWidget, PluginModel
from pyoffer.libs.widgets import QRemoteImage


class DigikalaItem(object):
    """docstring for DigikalaItem"""
    def __init__(self, product_id, title, image_url, expire_datetime, features, price=0, discounted=0):
        super(DigikalaItem, self).__init__()
        self.product_id = product_id
        self.title = title
        self.image_url = image_url
        self.features = features
        self.price = price
        self.discounted = discounted
        self.expire_datetime = expire_datetime

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getProductId(self):
        return self.product_id

    def setProductId(self, product_id):
        self.product_id = product_id

    def getLink(self):
        return "http://www.digikala.com/Product/DKP-%s" % self.getProductId()

    def getImageUrl(self):
        return self.image_url

    def setImageUrl(self, image_url):
        self.image_url = image_url

    def getExpireDatetime(self):
        return self.expire_datetime

    def setExpireDatetime(self, expire_datetime):
        self.expire_datetime = expire_datetime

    def getFormattedExpiration(self):
        return self.expire_datetime.strftime("%A, %d %B %H:%M")


class DigikalaModel(PluginModel):
    """docstring for DigikalaModel"""
    def __init__(self):
        super(DigikalaModel, self).__init__()
        self.api = "http://search.digikala.com/api2/Data/Get?incredibleOnly=true"
        self.lock = Lock()
        self.offers = []
        self.current_position = None

    def update(self):
        thread = Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        with self.lock:
            self.notifyUpdating()
            # try:
            response = requests.get(self.api)
            response_json = json.loads(response.content.decode('utf-8'))
            offers_list = response_json['responses'][0]['hits']['hits']
            offers = []
            for offer in offers_list:
                product_id = offer['_source']['ProductId']
                title = offer['_source']['FaTitle']
                features = offer['_source']['KeyFeatures']
                price = int(int(offer['_source']['Price']) / 10000)
                discounted = int(price - int(offer['_source']['Discount']) / 10000)
                title = offer['_source']['FaTitle']
                image = 'http://file.digikala.com/Digikala/%s' % offer['_source']['ProductImagePath']
                image = image.replace('/Original/', '/220/')
                expiration_endtime = offer['_source']['EndDateTime']
                expiration_utc = parser.parse(expiration_endtime)
                if not expiration_endtime.endswith('Z'):
                    expiration = expiration_utc
                else:
                    expiration = expiration_utc.astimezone(tz.tzlocal())

                offers.append(DigikalaItem(product_id,
                                           title,
                                           image,
                                           expiration,
                                           features,
                                           price,
                                           discounted))
            self.offers = offers
            self.current_position = None
            self.notifyChange()
            # except:
            #     pass
            self.notifyUpdated()


class DigikalaWidget(PluginWidget):
    """docstring for DigikalaWidget"""
    def __init__(self):
        super(DigikalaWidget, self).__init__()
        self.model = DigikalaModel()
        self.model.registerChange(self)
        self.model.registerUpdated(self)
        self.model.registerUpdating(self)

        self.product_image = None

    def setupUi(self):
        ui_path = os.path.join(os.path.dirname(__file__), 'digikala.ui')
        self.ui = loadUi(ui_path, self)

    def setupConnections(self):
        self.ui.updateButton.clicked.connect(self.updateClicked)
        self.ui.nextButton.clicked.connect(self.nextClicked)
        self.ui.prevButton.clicked.connect(self.prevClicked)
        self.ui.shopButton.clicked.connect(self.shopClicked)
        self.ui.comboBox.currentIndexChanged.connect(self.setCurrentOfferIndex)

    def updateClicked(self):
        self.model.update()

    def modelChanged(self):
        self.ui.comboBox.clear()
        for offer in self.model.offers:
            self.ui.comboBox.addItem(offer.getTitle())
        self.ui.comboBox.setCurrentIndex(0)

    def modelUpdated(self):
        self.ui.updateButton.setEnabled(True)
        if self.model.offers:
            self.ui.nextButton.setEnabled(True)
            self.ui.prevButton.setEnabled(True)
            self.ui.shopButton.setEnabled(True)
            self.ui.comboBox.setEnabled(True)

    def modelUpdating(self):
        self.ui.nextButton.setEnabled(False)
        self.ui.prevButton.setEnabled(False)
        self.ui.shopButton.setEnabled(False)
        self.ui.updateButton.setEnabled(False)
        self.ui.comboBox.setEnabled(False)

    def setCurrentOfferIndex(self, index=0):
        item = self.model.offers[index]
        self.ui.titleLabel.setText(item.getTitle())
        self.ui.priceLabel.setText(str(item.price))
        self.ui.discountedLabel.setText(str(item.discounted))
        self.ui.featuresLabel.setText(str(item.features))
        self.ui.expirationLabel.setText(item.getFormattedExpiration())
        # FIXME: remove current QRemoteImage's parent to stop updating imageLabel
        if self.product_image:
            self.product_image.setParent(parent=None)
        self.product_image = QRemoteImage.getInstance(item.getImageUrl(), self.ui.imageLabel)
        self.product_image.setParent(parent=self.ui.imageLabel)
        self.product_image.update()

    def nextClicked(self):
        index = self.ui.comboBox.currentIndex()
        count = self.ui.comboBox.count()
        next_index = (index + 1) % count
        self.ui.comboBox.setCurrentIndex(next_index)

    def prevClicked(self):
        next_index = self.ui.comboBox.currentIndex() - 1
        count = self.ui.comboBox.count()
        if next_index < 0 and count:
            next_index = count - 1
        self.ui.comboBox.setCurrentIndex(next_index)

    def shopClicked(self):
        index = self.ui.comboBox.currentIndex()
        item = self.model.offers[index]
        product_lilnk = item.getLink()
        webbrowser.open(product_lilnk)


class DigikalaPlugin(Plugin):
    """docstring for DigikalaPlugin"""
    def __init__(self):
        super(DigikalaPlugin, self).__init__()
        self.widget = DigikalaWidget()

    def getWidget(self):
        return self.widget
