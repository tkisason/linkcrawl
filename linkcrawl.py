#!/usr/bin/env python
# work in progress - multipurpose crawler
from sys import argv
import lxml.html    # you will need python-lxml to use this script.
from urlparse import urlparse, urljoin
import urllib2

useragent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) '\
            'Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0C)'


def get_url(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', useragent)]
    usock = opener.open(url)
    data = usock.read()
    usock.close()
    return data


def parser(url, type="a", stype="href"):
    if url.find('http://') == -1:
        url = 'http://'+url
    content = lxml.html.fromstring(get_url(url))
    links = []
    for link in content.cssselect(type):
        links.append(urljoin(url, link.get(stype)))
    return links


def class_parse(url, cls):
    if url.find('http://') == -1:
        url = 'http://'+url
    text = []
    content = lxml.html.fromstring(get_url(url))
    for cont in content.find_class(cls):
        text.append(cont.text_content())
    return text


def same_netloc(origin, urllist):
    if origin.find('http://') == -1:
        origin = 'http://'+origin
    outlist = []
    ourl = urlparse(origin).netloc
    for url in urllist:
        if urlparse(url).netloc == ourl:
            outlist.append(url)
    return outlist


def extract_url_arg(urllist, arg):
    args = []
    if arg.find("=") == -1:
        arg = arg+"="
    for elem in urllist:
        s = elem.find(arg) + len(arg)
        e = s + elem[s:].find("&")
        if len(elem[s:e]) > 0:
            args.append(elem[s:e])
    return args

if __name__ == '__main__':
    if len(argv) == 1:
        print "usage: ./"+argv[0]+" [OPTION] {,http://}some.web.site"
        print "     -o: print only those that have the same origin as the "\
              "requested site\n"
    else:
        if argv[1] == "-o":
            links = same_netloc(argv[2], parser(argv[2]))
        else:
            links = parser(argv[1])
        for link in links:
            print link
