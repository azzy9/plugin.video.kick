# -*- coding: UTF-8 -*-

import sys

import xbmcaddon

PLUGIN_ID = int(sys.argv[1])
PLUGIN_URL = sys.argv[0]
PLUGIN_NAME = PLUGIN_URL.replace('plugin://','')
ADDON = xbmcaddon.Addon()

PATH = ADDON.getAddonInfo('path')

DOMAIN = 'kick.com'
BASE_URL = 'https://' + DOMAIN

RESOURCE_URL = 'special://home/addons/' + PLUGIN_NAME + 'resources/'
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_FANART = ADDON.getAddonInfo('fanart')

KODI_VERSION = float(xbmcaddon.Addon('xbmc.addon').getAddonInfo('version')[:4])

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'

PLAYBACK_METHOD = ADDON.getSetting('playbackMethod')

#language
LANGUAGE = ADDON.getLocalizedString
