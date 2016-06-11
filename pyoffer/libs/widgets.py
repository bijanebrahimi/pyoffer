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

    def update(self, loading_message='Loading Image ....'):
        if not self.image_data:
            self.setParentText(loading_message)
            thread = Thread(target=self.run)
            thread.daemon = True
            thread.start()
        else:
            self.setParentPixmap()

    def run(self):
        response = requests.get(self.url, stream=True)
        total_length = response.headers.get('content-length')
        if not total_length:
            self.image_data = response.content
        else:
            dl = 0
            image_data = b""
            total_length = int(total_length)
            for data in response.iter_content():
                dl += len(data)
                image_data += data
                done = int((dl / total_length)*100)
                self.setParentText("Loading %%%s" % done)
            self.image_data = image_data
        self.setParentPixmap()

    def setParentPixmap(self):
        if self.parent:
            self.parent.setPixmap(self.toPixmap())

    def setParentText(self, text):
        if self.parent:
            self.parent.setText(text)

    def setParent(self, parent):
        self.parent = parent
