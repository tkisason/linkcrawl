#!/usr/bin/python

import linkcrawl
import urllib2
import sys

def pastie_gen_url(query,page=1):
    links = []
    if type(page) == list:
        for id in page:
            links.append("http://pastie.org/search?commit=Start+Search&page="+str(id)+"&q="+query.replace(" ","+"))
        return links
    return "http://pastie.org/search?commit=Start+Search&page="+str(page)+"&q="+query.replace(" ","+")


def pastie_find(query,raw="y"):
    urls = linkcrawl.same_netloc("http://pastie.org",linkcrawl.parser(pastie_gen_url(query)))
    ids = linkcrawl.extract_url_arg(urls,"page")
    big = int(ids[0])
    for elem in ids:
        if int(elem) > int(big):
            big = int(elem)
    ids = range(1,int(big)+1)
    links = []
    for item in pastie_gen_url(query,ids):
        links += (linkcrawl.same_netloc("http://pastie.org",linkcrawl.parser(item)))
    olinks = []
    for link in links:
        if link.find("pastes/") != -1:
            if link.find("/new") == -1:
                if raw == "y":
                    olinks.append(link+"/text")
                else:
                    olinks.append(link)
    return olinks

if __name__ == '__main__':
    q = raw_input("[+] LinkCrawl: Enumerate pastie.org, enter query: ")
    OF = raw_input("[+] Enter output file name: ")
    delimiter = "EOF EOF EOF"
    links = pastie_find(q)
    print "[+] Got " +str(len(links)) +  " links dumping content to file, delimiter is: " + str(delimiter)
    OF = OF+".html"
    FILE = open((OF),"w")
    sys.stdout.write("[+] Working: ")
    for link in links:
        FILE.write(urllib2.urlopen(link).read())
        FILE.write("\n\n\n"+delimiter+"\n\n\n")
        sys.stdout.write(".")
        sys.stdout.flush()
        FILE.flush()
    print "\n"
    FILE.close()
    print "[+] Enumeration done, output is in: " + OF
        
