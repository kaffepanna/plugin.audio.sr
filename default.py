import sys
import xbmc, xbmcgui, xbmcplugin
import urllib
from urlparse import urljoin
import util
import re

BASE_URL = "http://m.sverigesradio.se/radio.aspx"
EXTRA_URL = "http://m.sverigesradio.se/radio.aspx?extra=1"
BASE_STREAM_URL = "http://http-live.sr.se"
MODE_SHOW_MENU  = 0
MODE_PLAY_RADIO = 1

# utility functions
def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[urllib.unquote(paramSplits[0])] = urllib.unquote(paramSplits[1])
    return paramDict

def addDir(name,url,mode):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
  ok=True
  liz=xbmcgui.ListItem( name, iconImage="DefaultFolder.png")
  liz.setInfo( type="Audio", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
  return ok

def addLink(name,url):
  ok=True
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(MODE_PLAY_RADIO)+"&name="+urllib.quote_plus(name)
  liz=xbmcgui.ListItem(name, iconImage="DefaultAudio.png")
  liz.setInfo( type="audio", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
  return ok


def show_menu(url):
  doc = util.get_document_by_url(url)
  ul = util.get_elements_by_tag_class(doc, 'ul', 'channel')[0]
  lis = util.get_elements_by_tag(ul, 'li')
  if url == BASE_URL:
    addDir("Extra", EXTRA_URL, MODE_SHOW_MENU)
  for li in lis:
    a = util.get_elements_by_tag(li, 'a')[0]
    url = util.unicode(a.getAttribute('href'))
    title = util.unicode(util.get_node_text(a).strip())
    if li.getAttribute('class') == 'channel':
      url = urljoin(BASE_STREAM_URL, url.split("/")[-1])
      addLink(title, url)
    else:
      url = urljoin(BASE_URL, re.sub("^/", "", url))
      addDir(title, url, MODE_SHOW_MENU)

  xbmcplugin.endOfDirectory(handle = int(sys.argv[1]), cacheToDisc=True )

def play_radio(url, name):
  liz=xbmcgui.ListItem(name, iconImage="DefaultAudio.png")
  liz.setInfo( type="audio", infoLabels={ "Title": name } )
  xbmc.Player().play(url, liz)

params = parameters_string_to_dict(sys.argv[2])
mode = int(params.get("mode", "0"))

xbmc.log(msg='Mode = %d' % mode, level=xbmc.LOGNOTICE)

if not sys.argv[2]:
  show_menu(BASE_URL)
elif mode == MODE_SHOW_MENU:
  show_menu(params["url"])
elif mode == MODE_PLAY_RADIO:
  play_radio(params["url"], params["name"])
  
