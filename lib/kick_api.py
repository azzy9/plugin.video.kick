"""
Kick API Class
Created by Azzy9
Class to handle all the kick API calls
"""

import xbmcaddon

from lib.general import request_get

ADDON = xbmcaddon.Addon()

class KickAPI:

    """ main kick user class """

    base_url = 'https://kick.com'
    lang_val = ''
    limit_amount = '25'
    language_codes = [ 'en', 'pl', 'ar', 'zh', 'fi', 'fr', 'de', 'hi', 'id', 'ja', 'ko', 'pt', 'ru', 'es', 'tr', 'vi' ]

    def __init__( self ):

        """ Construct to get the saved details """

        self.lang_val = self.language_get( ADDON.getSetting('site_language') )

    def language_get( self, pos ):

        if pos:
            pos = int(pos)
            if 0 <= pos < len(self.language_codes):
                return self.language_codes[ pos ]

        return self.language_codes[0]
    
    def page_int(self, page=None):

        if page:
            return int(page)

        return 1

    def streams_livestreams( self, page=None, category=None ):

        """ method to get livestreams """

        page = self.page_int( page )

        url = self.base_url + '/stream/livestreams/' + self.lang_val + \
            '?limit=' + self.limit_amount + '&page=' + str(page)

        if category:
            url += '&sort=desc&subcategory=' + category
        else:
            url += '&sort=featured'

        data = request_get(url)

        if data:
            streams_livestreams = data.json()
            if streams_livestreams:
                return streams_livestreams

        return {}

    def subcategories( self, page=None ):

        """ method to get subcategories """

        page = self.page_int( page )

        url = self.base_url + '/api/v1/subcategories?limit=' + self.limit_amount + '&page=' + str( page )

        data = request_get(url)

        if data:
            subcategories = data.json()
            if subcategories:
                return subcategories

        return {}

    def search( self, search_str ):

        """ method to make a search request"""

        url = self.base_url + '/api/search?searched_word=' + search_str.replace(' ','+')

        data = request_get(url)

        if data:
            search = data.json()
            if search:
                return search

        return {}

