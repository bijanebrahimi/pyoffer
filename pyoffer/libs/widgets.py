# From python
import requests
from threading import Thread
# From PyQt5
from PyQt5.QtGui import QPixmap, QImage


class QRemoteImage(QImage):
    """docstring for QRemoteImage"""
    instances = dict()

    def __init__(self, url, parent):
        super(QRemoteImage, self).__init__()
        self.url = url
        self.image_data = None
        self.parent = parent

    @staticmethod
    def getInstance(url, parent):
        if not url in QRemoteImage.instances.keys():
            QRemoteImage.instances[url] = QRemoteImage(url, parent)
        return QRemoteImage.instances[url]


    def toPixmap(self):
        if self.image_data:
            image = QImage()
            image.loadFromData(self.image_data)
            pixmap = QPixmap.fromImage(image)
        else:
            pixmap = QPixmap()
        return pixmap

    def update(self, loading_message='Loading Image ...'):
        if not self.image_data:
            self.parent.setText(loading_message)
            thread = Thread(target=self.run)
            thread.daemon = True
            thread.start()
        else:
            self.setParentPixmap()

    def run(self):
        res = requests.get(self.url)
        self.image_data = res.content
        self.setParentPixmap()

    def setParentPixmap(self):
        self.parent.setPixmap(self.toPixmap())
