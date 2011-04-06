#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
import urllib2  
from sgmllib import SGMLParser
import sys
from urlparse import urlparse

Collectedlinks = []

class URLLister(SGMLParser):        # Simple SGML Parser for html href extraction
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []
    def start_a(self, attrs):
        href = [v for k, v in attrs if k=='href']
        if href:
            self.urls.extend(href)

def GetLinks(site,clean):
        parser = URLLister()
        parser.feed(urllib2.urlopen(site).read())
        parser.close()
        for url in parser.urls:
            if len(url) <= 1:
                pass
            elif url.find("://") != -1:
                if clean == "-o":
                    site1 = urlparse(site)
                    url1 = urlparse(url)
                    if site1.netloc == url1.netloc:
                        Collectedlinks.append(str(url))
                else:
                    Collectedlinks.append(str(url))
            elif url[0] == "/":
                Collectedlinks.append(str(site+url))
            elif clean == "-e":
                Collectedlinks.append(url)
            elif clean == "-r": #seems legit
                site2 = urlparse(site)
                url2 = urlparse(url)
                if site2.netloc == url2.netloc:
                    for url3 in Collectedlinks:
                        GetLinks(url3,"")
        parser.close()

def h_pref(param):
    if param.find('http://') != -1:
        return str(param)
    else:
        return str('http://'+param)

def h_origin(param1, param2):
    param1 = urlparse(param1)
    param2 = urlparse(param2)
    if param1.netloc == param2.netloc:
        return 1
    else:
        return 0

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "usage: ./"+sys.argv[0]+" [OPTION] {,http://}some.web.site"
        print "     -e: print everything: links including javascripts and mailto attributes...\n"
        print "     -o: print only those that have the same origin as the requested site\n"
        print "     -r: wannabe recursive parsing option\n"
    else:
        if sys.argv[1] == "-e":
            GetLinks(h_pref(str(sys.argv[2])),"-e")
        elif sys.argv[1] == "-o":
            GetLinks(h_pref(str(sys.argv[2])),"-o")
        elif sys.argv[1] == "-r":
            GetLinks(h_pref(str(sys.argv[2])),"")
            GetLinks(h_pref(str(sys.argv[2])),"-r")
        else:
            GetLinks(h_pref(str(sys.argv[1])),"")
        for link in Collectedlinks:
            print link
