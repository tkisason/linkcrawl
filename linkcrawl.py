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

def GetLinks(site):
        parser = URLLister()
        parser.feed(urllib2.urlopen(site).read())
        parser.close()
        for url in parser.urls:
            if url[:4] == ("http" or "https" or "ftp"):
                Collectedlinks.append(str(url))
            else:
                Collectedlinks.append(str(sys.argv[1]+url))
        parser.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage: ./"+sys.argv[0]+" http://www.example.com\n"
    else:
        GetLinks(str(sys.argv[1]))
        for link in Collectedlinks:
            print link

