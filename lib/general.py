# -*- coding: utf-8 -*-
import sys
import requests

import ssl

import xbmc
import xbmcaddon

from six.moves import urllib_parse

import six
from six.moves import urllib

try:
    import json
except ImportError:
    import simplejson as json

from lib.constants import *

# Disable urllib3's "InsecureRequestWarning: Unverified HTTPS request is being made" warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter

class TLS11HttpAdapter(HTTPAdapter):

    """Transport adapter" that allows us to use TLSv1.1"""

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize, block=block, ssl_version=ssl.PROTOCOL_TLSv1_1
        )


class TLS12HttpAdapter(HTTPAdapter):

    """Transport adapter" that allows us to use TLSv1.2"""

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize, block=block, ssl_version=ssl.PROTOCOL_TLSv1_2
        )

reqs = requests.session()
tls_adapters = [TLS12HttpAdapter(), TLS11HttpAdapter()]

def request_get( url, data=None, extra_headers=None ):

    """ makes a request """

    try:

        # headers
        my_headers = {
            'Accept-Language': 'en-gb,en;q=0.5',
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': url,
            'Cache-Control': 'max-age=0',
        }

        # add extra headers
        if extra_headers:
            my_headers.update(extra_headers)

        # get stored cookie string
        cookies = ADDON.getSetting('cookies')

        # split cookies into dictionary
        if cookies:
            cookie_dict = json.loads( cookies )
        else:
            cookie_dict = None

        # make request
        uri = urllib_parse.urlparse(url)
        domain = uri.scheme + '://' + uri.netloc

        status = 0
        i = 0
        while status != 200 and i < 2:
            if data:
                response = reqs.post(
                    url, data=data, headers=my_headers, verify=False, cookies=cookie_dict, timeout=10
                )
            else:
                response = reqs.get(
                    url, headers=my_headers, verify=False, cookies=cookie_dict, timeout=10
                )

            status = response.status_code
            if status != 200:
                if status == 403 and response.headers.get('server', '') == 'cloudflare':
                    reqs.mount(domain, tls_adapters[i])
                i += 1

        if response.cookies.get_dict():
            if cookie_dict:
                cookie_dict.update( response.cookies.get_dict() )
            else:
                cookie_dict = response.cookies.get_dict()

            # store cookies
            ADDON.setSetting('cookies', json.dumps(cookie_dict))

        return response

    except Exception:
        return ''

def build_url(query):

    """
    Helper function to build a Kodi xbmcgui.ListItem URL
    :param query: Dictionary of url parameters to put in the URL
    :returns: A formatted and urlencoded URL string
    """

    return PLUGIN_URL + '?' + urllib_parse.urlencode(query)

def ensure_full_url( base_url, url ):

    """ returns a full url """

    if url:
        if url.startswith('http'):
            return url
        if url.startswith('//'):
            return 'https:' + url
        if url.startswith('/'):
            return base_url + url

    return url

def notify( message, name=False, iconimage=False, time_shown=5000 ):

    """ Show notification to user """

    if not name:
        name = ADDON_NAME

    if not iconimage:
        iconimage = ADDON_ICON

    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (name, message, time_shown, iconimage))

def get_string( string_id ):

    """ gets language string based upon id """

    if string_id >= 30000:
        return LANGUAGE( string_id )
    return xbmc.getLocalizedString( string_id )

def get_params():

    """ gets params from request """

    return dict(urllib.parse.parse_qsl(sys.argv[2][1:], keep_blank_values=True))

def item_set_info( list_item, properties ):

    """ line item set info """

    if KODI_VERSION > 19.8:
        vidtag = list_item.getVideoInfoTag()
        if properties.get( 'year' ):
            vidtag.setYear( int( properties.get( 'year' ) ) )
        if properties.get( 'episode' ):
            vidtag.setEpisode( properties.get( 'episode' ) )
        if properties.get( 'season' ):
            vidtag.setSeason( properties.get( 'season' ) )
        if properties.get( 'plot' ):
            vidtag.setPlot( properties.get( 'plot' ) )
        if properties.get( 'title' ):
            vidtag.setTitle( properties.get( 'title' ) )
        if properties.get( 'studio' ):
            vidtag.setStudios([ properties.get( 'studio' ) ])
        if properties.get( 'writer' ):
            vidtag.setWriters([ properties.get( 'writer' ) ])
        if properties.get( 'duration' ):
            vidtag.setDuration( int( properties.get( 'duration' ) ) )
        if properties.get( 'tvshowtitle' ):
            vidtag.setTvShowTitle( properties.get( 'tvshowtitle' ) )
        if properties.get( 'mediatype' ):
            vidtag.setMediaType( properties.get( 'mediatype' ) )
        if properties.get('premiered'):
            vidtag.setPremiered( properties.get( 'premiered' ) )

    else:
        list_item.setInfo('video', properties)
