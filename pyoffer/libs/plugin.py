# From Yapsi
from yapsy.IPlugin import IPlugin
# From PyQt5
from PyQt5.QtWidgets import QWidget


class Plugin(IPlugin):
    """docstring for Plugin"""
    def __init__(self):
        super(Plugin, self).__init__()

    def getWidget(self):
        pass

    def update(self):
        pass

    def notify(self):
        pass


class PluginWidget(QWidget):
    """docstring for PluginWidget"""
    def __init__(self):
        super(PluginWidget, self).__init__()
        self.setupUi()
        self.setupConnections()

    def setupUi(self):
        pass

    def setupConnections(self):
        pass

    def modelChanged(self):
        pass

    def modelUpdating(self):
        pass

    def modelUpdated(self):
        pass


class PluginModel(object):
    """docstring for PluginModel"""
    def __init__(self):
        super(PluginModel, self).__init__()
        self.change_observers = []
        self.updating_observers = []
        self.updated_observers = []

    def registerChange(self, observer):
        self.change_observers.append(observer)

    def removeChange(self, observer):
        self.change_observers.remove(observer)

    def notifyChange(self):
        for observer in self.change_observers:
            observer.modelChanged()

    def registerUpdating(self, observer):
        self.updating_observers.append(observer)

    def removeUpdating(self, observer):
        self.updating_observers.remove(observer)

    def notifyUpdating(self):
        for observer in self.updating_observers:
            observer.modelUpdating()

    def registerUpdated(self, observer):
        self.updated_observers.append(observer)

    def removeUpdated(self, observer):
        self.updated_observers.remove(observer)

    def notifyUpdated(self):
        for observer in self.updated_observers:
            observer.modelUpdated()
