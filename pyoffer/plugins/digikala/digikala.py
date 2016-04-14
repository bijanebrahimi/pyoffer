# From Python
import os
import json
import requests
import tempfile
import webbrowser
from dateutil.parser import parse as datetime_parser
from datetime import datetime
# From Yapsi
from yapsy.IPlugin import IPlugin
# From PyQt5
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
# From PyOffer
from pyoffer.libs.utils import json_serial

def showError(text, title="Error"):
    mes = QMessageBox(text=text)
    mes.setWindowTitle('Eroooooor')
    mes.exec()


class Digikala(object):
    """docstring for Digikala"""
    def __init__(self, api_url=None, static_relative_path=None):
        super(Digikala, self).__init__()

        self.__api_url = api_url if api_url else 'http://search.digikala.com/api2/Data/Get?incredibleOnly=true'
        self.__static_relative_path = static_relative_path if static_relative_path else 'http://file.digikala.com/Digikala'
        self.__cache_dir = '/tmp/digikala'

        self.__offers = []
        if not os.path.exists(self.__cache_dir):
            os.mkdir(self.__cache_dir)
        if os.path.exists(os.path.join(self.__cache_dir, 'offers.json')):
            with open(os.path.join(self.__cache_dir, 'offers.json'), 'r') as f:
                self.__offers = json.load(f)

    def load(self, disable_cache=False):
        success = False
        if not disable_cache:
            success = self.loadFromCache()
        if not success or disable_cache:
            success = self.loadFromAPI()
        return success

    def loadFromAPI(self):
        response = requests.get(self.__api_url)
        json_response = json.loads(response.content.decode('UTF-8'))
        json_offers = json_response['responses'][0]['hits']['hits']
        parsed_offers = self.__parse_offers(json_offers)
        self.__save_cache(parsed_offers)
        self.__offers = parsed_offers

    def loadFromCache(self):
        cached_request = os.path.join(self.__cache_dir, 'offers.json')
        if os.path.exists(cached_request):
            with open(cached_request, 'r') as f:
                json_offers = json.load(f)
            self.__offers = json_offers
            return True
        return False

    def __parse_offers(self, offers):
        parsed_offers = []
        for offer in offers:
            offer_source = offer['_source']
            offer_source['ImageLocalPath'] = self.__retrieve_url(offer_source['ImagePath'])
            offer_source['StartDateTime'] = datetime_parser(offer_source['StartDateTime'])
            offer_source['EndDateTime'] = datetime_parser(offer_source['EndDateTime'])
            parsed_offers.append(offer_source)
        return parsed_offers

    def __retrieve_url(self, url):
        base_name = os.path.basename(url)
        file_path = os.path.join(self.__cache_dir, base_name)
        url = self.__static_relative_path + '/' + url
        # try:
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                response = requests.get(url)
                f.write(response.content)
        return file_path
        # except:
        #     print(ur)
        # finally:
        #     return None

    def __save_cache(self, offers):
        try:
            if offers:
                with open(os.path.join(self.__cache_dir, 'offers.json'), 'w') as f:
                    json.dump(offers, f, default=json_serial)
        finally:
            return True

    def getOffer(self, index=0):
        return self.__offers[index]

    def count(self):
        if not self.__offers:
            return -1
        return len(self.__offers)

    def is_expired(self):
        for offer in self.__offers:
            if offer['EndDateTime'] <= datetime.now():
                return True
        return False

    def expire(self):
        for offer in self.__offers:
            return offer['EndDateTime'].strftime("%H:%M")
        return ''


class DigikalaWidget(QWidget):
    """docstring for DigikalaWidget"""
    def __init__(self, parent=None):
        super(DigikalaWidget, self).__init__(parent=parent)
        self.setupUi()
        self.setupConnections()

        self.__digikala = Digikala()
        self.__digikala_index = 0
        if self.__digikala.loadFromCache():
            self.setupWidgets()

    def setupUi(self):
        ui_path = os.path.join(os.path.dirname(__file__), 'digikala.ui')
        loadUi(ui_path, self)

    def setupConnections(self):
        self.updateBtn.clicked.connect(self.updateClicked)
        self.nextBtn.clicked.connect(self.nextClicked)
        self.prevBtn.clicked.connect(self.prevClicked)
        self.openBtn.clicked.connect(self.openClicked)
        self.comboBox.currentIndexChanged.connect(self.setCurrentOfferIndex)

    def updateClicked(self):
        try:
            self.updateBtn.setEnabled(False)
            # self.__digikala.load(disable_cache=self.__digikala.is_expired())
            self.__digikala.load(disable_cache=False)
            self.setupWidgets()
        except:
            pass
        finally:
            self.updateBtn.setEnabled(True)

    def setupWidgets(self):
        if self.__digikala.count():
            self.nextBtn.setEnabled(True)
            self.prevBtn.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.openBtn.setEnabled(True)
            self.setCurrentOfferIndex(index=0)
            self.comboBox.clear()
            for index in range(self.__digikala.count()):
                offer = self.__digikala.getOffer(index)
                self.comboBox.addItem(offer['Title'])
        else:
            self.nextBtn.setEnabled(False)
            self.openBtn.setEnabled(False)
            self.prevBtn.setEnabled(False)
            self.comboBox.setEnabled(False)

    def setCurrentOfferIndex(self, index=0):
        if index >= self.__digikala.count():
            index = 0
        elif index < 0:
            index = self.__digikala.count() -1
        self.__digikala_index = index
        offer = self.__digikala.getOffer(index)
        image_path = offer['ImageLocalPath']

        self.ImageLbl.setPixmap(QPixmap(image_path))
        self.comboBox.setCurrentIndex(index)

    def nextClicked(self):
        self.setCurrentOfferIndex(index=self.__digikala_index+1)

    def prevClicked(self):
        self.setCurrentOfferIndex(index=self.__digikala_index-1)

    def openClicked(self):
        index = self.__digikala_index
        offer = self.__digikala.getOffer(index)
        url = 'http://www.digikala.com/Product/DKP-%s' % offer['ProductId']
        webbrowser.open(url)


class DigikalaPlugin(IPlugin):
    """docstring for DigikalaPlugin"""
    def __init__(self):
        super(DigikalaPlugin, self).__init__()
        self.widget = DigikalaWidget()
