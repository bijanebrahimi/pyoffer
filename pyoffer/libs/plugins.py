from yapsy.PluginManager import PluginManager


plugin_manager = PluginManager()
plugin_manager.setPluginPlaces(["pyoffer/plugins/"])
plugin_manager.collectPlugins()
