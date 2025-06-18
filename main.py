# -*- coding: UTF-8 -*-

from lib.constants import *
from lib.general import *

import xbmcgui
import xbmcplugin
import xbmc

def add_dir( name, mode='', url='', images={}, info_labels={}, category='', context_menu=None, playable=False, folder=False ):

    """ Adds directory items """

    art_dict = {
        'thumb': images.get( 'thumb', ADDON_ICON ),
        'poster': images.get( 'thumb', ADDON_ICON ),
        'banner': images.get( 'thumb', ADDON_ICON ),
        'fanart': images.get( 'fanart', ADDON_FANART ),
    }

    link_params = {
        'url': url,
        'mode': str( mode ),
        'name': name,
        'thumb': art_dict[ 'thumb' ],
        'fanart': art_dict[ 'fanart' ],
        'plot': info_labels.get( 'plot', '' ),
        'category': category,
    }

    list_item = xbmcgui.ListItem(label=name)

    if playable:
        list_item.setProperty('IsPlayable', 'True')
        xbmcplugin.setContent(PLUGIN_ID, 'videos')

    if not info_labels:
        info_labels={'title': name}

    item_set_info( list_item, info_labels )
    list_item.setArt(art_dict)

    if context_menu:
        out=context_menu
        list_item.addContextMenuItems(out, replaceItems=True)

    xbmcplugin.addDirectoryItem(
        handle=PLUGIN_ID,
        url = build_url(link_params),
        listitem=list_item,
        isFolder=folder
    )

def to_unicode( text, encoding='utf-8', errors='strict' ):

    """ Forces text to unicode """

    if isinstance(text, bytes):
        return text.decode(encoding, errors=errors)

    return text

def get_search_string( heading='', message='' ):

    """ Ask the user for a search string """

    search_string = None

    keyboard = xbmc.Keyboard(message, heading)
    keyboard.doModal()

    if keyboard.isConfirmed():
        search_string = to_unicode(keyboard.getText())

    return search_string

def home_menu():

    """ Creates the home menu """

    add_dir( 'Livestreams', 'livestream_list', folder=True )
    add_dir( 'Categories', 'category_list', folder=True )
    add_dir( 'Search', 'search', folder=True )
    add_dir( 'Settings', 'settings' )

    xbmcplugin.endOfDirectory(PLUGIN_ID)

def livestream_list( page, category='' ):

    """ method to retrieve livestreams """

    if page:
        page = int(page)
    else:
        page = 1

    url = BASE_URL + '/stream/livestreams/' + LANG_VAL + \
        '?limit=' + LIMIT_AMOUNT + '&page=' + str(page)

    if category:
        url += '&sort=desc&subcategory=' + category
    else:
        url += '&sort=featured'

    js_data = request_get(url).json()
    data = js_data.get('data', {})

    if data:
        for row in data:

            session_title = row.get('session_title', '').replace('\n', ' ')

            channel_slug = row.get('channel', {}).get('slug', '')
            channel_name = row.get('channel', {}).get('user', {}).get( 'username', channel_slug )
            viewers = row.get('viewers', None)
            video_title = '[COLOR gold]' + channel_name + '[/COLOR] ' + \
                session_title + ' [COLOR palegreen](' + str(viewers) + ')[/COLOR]'

            url = '/api/v2/channels/' + channel_slug + '/livestream'

            images = {}
            images[ 'thumb' ] = row.get('channel', {}).get('user', {}).get( 'profilepic', ADDON_ICON )
            images[ 'fanart' ] = row.get('thumbnail', {}).get('src', ADDON_FANART)

            info_labels = { 'title': video_title, 'plot': video_title }

            add_dir( video_title, 'play', url, images, info_labels, playable=True )

        if js_data.get('next_page_url', None):

            page += 1

            images = { 'thumb': RESOURCE_URL + 'next.png' }
            add_dir( 'Next Page', 'livestream_list', str(page), images, category=category, folder=True )

    xbmcplugin.endOfDirectory(PLUGIN_ID)

def category_list( page ):

    """ method to view a category """

    if page:
        page = int(page)
    else:
        page = 1

    url = BASE_URL + '/api/v1/subcategories?limit=' + LIMIT_AMOUNT + '&page=' + str( page )

    js_data = request_get(url).json()
    data = js_data.get('data', {})

    if data:
        for row in data:

            category_slug = row.get('slug', '')
            category_name = row.get('name', category_slug)
            viewers = row.get('viewers', None)
            title = category_name + ' [COLOR palegreen](' + str( viewers ) + ')[/COLOR]'

            images = {}
            images[ 'thumb' ] = row.get('banner', {}).get('url', ADDON_ICON)
            images[ 'fanart' ] = row.get('banner', {}).get('url', ADDON_FANART)

            info_labels = { 'title': title, 'plot': title }

            add_dir( title, 'livestream_list', '', images, info_labels, category_slug, folder=True )

        if js_data.get('next_page_url', None):

            page += 1
            images = { 'thumb': RESOURCE_URL + 'next.png' }
            add_dir( 'Next Page', 'category_list', str( page ), images, folder=True )

    xbmcplugin.endOfDirectory(PLUGIN_ID)

def search_items():

    """ Searches the site """
    
    search_str = get_search_string(heading='Search')

    if not search_str:
        return

    title = urllib.parse.quote_plus( search_str )

    url = BASE_URL + '/api/search?searched_word=' + search_str.replace(' ','+')
    response = request_get(url).json()
    xbmc.log( url, xbmc.LOGWARNING )

    channels = response.get('channels', None)
    categories = response.get('categories', None)

    if channels:
        for row in channels:
            channel_slug = row.get('slug', None)
            user = row.get('user', None)
            username = user.get('username', None)
            profile_pic = user.get('profilePic', None)
            profile_pic = profile_pic if profile_pic else ADDON_ICON
            description = user.get('bio', None)
            if description:
                description = description.replace("\n",' ')
            description = description if description else username

            info_labels = { 'title': username, 'plot': description }
            images = { 'thumb': profile_pic }

            if row.get('is_live', False):
                url = '/api/v2/channels/' + channel_slug + '/livestream'
                add_dir( username, 'play', url, images, info_labels )

    if categories:
        for row in categories:
            title = row.get('name', None)
            slug = row.get('slug', None)
            description = row.get('description', None)

            viewers = row.get('viewers', None)
            title += ' [COLOR palegreen](' + str( viewers ) + ')[/COLOR]'
            description = description if description else title
            info_labels={ 'title': title, 'plot': description }

            images = {}
            images[ 'thumb' ] = row.get('banner', {}).get('src', ADDON_ICON)
            images[ 'fanart' ] = row.get('banner', {}).get('src', ADDON_FANART)

            add_dir( title, 'livestream_list', '', images, info_labels, slug, folder=True )

    if channels or categories:
        xbmcplugin.endOfDirectory(PLUGIN_ID)
    else:
        notify( 'Nothing found' )

def play( url ):

    """ plays a video from url """

    url = ensure_full_url( BASE_URL, url )

    if url.endswith('.mp4') or url.endswith('.m3u8'):
        link = url
    else:
        js_data = request_get(url).json()
        link = js_data.get('data', None).get('playback_url', None)

    play_item = xbmcgui.ListItem(path=link)
    play_item.setProperty('IsPlayable', 'true')
    play_item.setPath(link)

    # Disable Kodi's MIME-type request, since we already know what it is.
    play_item.setContentLookup(False)
    play_item.setMimeType('application/x-mpegURL')

    if KODI_VERSION < 19:
        play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
    else:
        play_item.setProperty('inputstream', 'inputstream.adaptive')

    if KODI_VERSION < 22:
        play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
    play_item.setProperty('inputstream.adaptive.original_audio_language', 'en')

    if PLAYBACK_METHOD == '2':
        play_item.setProperty('inputstream.adaptive.stream_selection_type', 'ask-quality')
    else:
        play_item.setProperty('inputstream.adaptive.stream_selection_type', 'adaptive')

    xbmcplugin.setResolvedUrl( PLUGIN_ID, True, listitem=play_item )

def main():

    """ main method """

    params = get_params()

    if params:

        mode = params.get('mode', None)
        url = params.get('url', '')
        category = params.get('category', '')

        if mode == 'settings':
            ADDON.openSettings()
        elif mode == 'livestream_list':
            livestream_list( url, category )
        elif mode == 'category_list':
            category_list( url )
        elif mode == 'search':
            search_items()

        elif mode == 'play':
            play( url )

    else:
        home_menu()

if __name__ == '__main__':
    main()
