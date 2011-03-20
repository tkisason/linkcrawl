#!/usr/bin/python

import urllib2  
from sgmllib import SGMLParser
import sys

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
                Collectedlinks.append(str(url))
            elif url[0] == "/":
                Collectedlinks.append(str(site+url))
            elif clean == "-e":
                Collectedlinks.append(url)
        parser.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "usage: ./"+sys.argv[0]+" [-e] http://www.example.com"
        print "     -e: print everything: links including javascripts and mailto attributes...\n"
    else:
        if sys.argv[1] == "-e":
            GetLinks(str(sys.argv[2]),"-e")
        else:
            GetLinks(str(sys.argv[1]),"")
        for link in Collectedlinks:
            print link

