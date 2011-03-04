import urllib2,urllib,re
from urlparse import urljoin
from xml.dom import minidom
import unicodedata

def get_node_text(node):
  txt = ""
  for t in node.childNodes:
    if t.nodeType == node.TEXT_NODE:
      txt = txt + t.data
  r = re.compile('\s+')
  return r.sub(' ', txt)

def get_elements_by_tag(doc, tag):
  return doc.getElementsByTagName(tag)

def get_element_by_tag_id(doc, tag, id):
  elements = doc.getElementsByTagName(tag)
  for element in elements:
    if element.getAttribute("id") == id:
      return element
  return None

def get_elements_by_tag_attrib(doc, tag, attrib, value):
  elements = doc.getElementsByTagName(tag)
  result = []
  for element in elements:
    if element.getAttribute(attrib) == value:
      result.append(element)
  return result

def get_elements_by_tag_class(doc, tag, klass):
  elements = doc.getElementsByTagName(tag)
  result = []
  for element in elements:
    if element.getAttribute("class") == klass:
      result.append(element)
  return result


def get_url(url):
  req = urllib2.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response = urllib2.urlopen(req)
  data=response.read()
  response.close()
  return data

def get_document_by_url(url):
  data = get_url(url)
  document = minidom.parseString(data)
  return document

def unicode(str):
  return unicodedata.normalize('NFKD', str).encode('ascii', 'ignore')

