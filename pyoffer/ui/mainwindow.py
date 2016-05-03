#!/usr/bin/python3
# -*- coding: utf-8 -*-
# From Python
import os
import sys
# From PyQt5
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QVBoxLayout
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    """docstring for MainWindow"""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.setupConnections()
        self.loadPlugins()

    def setupUi(self):
        ui_path = os.path.join(os.path.dirname(__file__), 'mainwindow.ui')
        self.ui = loadUi(ui_path, self)
        self.setWindowTitle('PyOffer')

    def setupConnections(self):
        self.ui.plugins.currentRowChanged.connect(self.ui.widget.setCurrentIndex)

    def loadPlugins(self):
        from pyoffer.libs.plugins import plugin_manager
        for plugin in plugin_manager.getAllPlugins():
            self.ui.plugins.addItem(QListWidgetItem(plugin.name))
            plugin_object = plugin.plugin_object
            plugin_widget = plugin_object.getWidget()
            self.ui.widget.addWidget(plugin_widget)
        self.plugins.setCurrentRow(0)

        # Remove Two Widgets added by default
        self.ui.widget.removeWidget(self.ui.widget.currentWidget())
        self.ui.widget.removeWidget(self.ui.widget.currentWidget())
