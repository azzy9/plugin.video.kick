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

LIMIT_AMOUNT = '25'

PLAYBACK_METHOD = ADDON.getSetting('playbackMethod')

#language
LANGUAGE = ADDON.getLocalizedString

def language_get( pos, language_codes ):

    if pos:
        pos = int(pos)
        if 0 <= pos < len(language_codes):
            return language_codes[ pos ]

    return language_codes[0]

LANGUAGE_CODES = [ 'en', 'pl', 'ar', 'zh', 'fi', 'fr', 'de', 'hi', 'id', 'ja', 'ko', 'pt', 'ru', 'es', 'tr', 'vi' ]
LANG_VAL = language_get( ADDON.getSetting('site_language'), LANGUAGE_CODES )
