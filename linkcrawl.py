#!/usr/bin/env python
# work in progress - multipurpose crawler
import sys
import lxml.html    # you will need python-lxml to use this script.
from urlparse import urlparse,urljoin 
import urllib2

useragent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0C)'

def get_url(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', useragent)]
    usock = opener.open(url)
    data = usock.read()
    usock.close()
    return data

def parser(url,type="a",stype="href"):
    if url.find('http://') == -1:
        url = 'http://'+url
    content = lxml.html.fromstring(get_url(url))
    links = []
    for link in content.cssselect(type):
        links.append(urljoin(url,link.get(stype)))
    return links

def same_netloc(origin,urllist):
    if origin.find('http://') == -1:
        origin = 'http://'+origin
    outlist = []
    ourl = urlparse(origin).netloc
    for url in urllist:
        if urlparse(url).netloc == ourl:
            outlist.append(url)
    return outlist

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "usage: ./"+sys.argv[0]+" [OPTION] {,http://}some.web.site"
        print "     -o: print only those that have the same origin as the requested site\n"
    else:
        if sys.argv[1] == "-o":
            links = same_netloc(sys.argv[2],parser(sys.argv[2]))
        else:
            links = parser(sys.argv[1])
        for link in links:
            print link
