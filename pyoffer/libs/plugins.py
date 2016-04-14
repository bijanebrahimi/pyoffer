# From Python
import os
# From Yapsy
from yapsy.PluginManager import PluginManager

plugins_path = os.path.join(os.path.dirname(__file__), '../plugins')

plugin_manager = PluginManager()
plugin_manager.setPluginPlaces([plugins_path])
plugin_manager.collectPlugins()
