import linkcrawl

def pastie_gen_url(query,page=1):
    links = []
    if type(page) == list:
        for id in page:
            links.append("http://pastie.org/search?commit=Start+Search&page="+str(id)+"&q="+query.replace(" ","+"))
        return links
    return "http://pastie.org/search?commit=Start+Search&page="+str(page)+"&q="+query.replace(" ","+")


def pastie_find(query):
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
                olinks.append(link+"/text")
    return olinks
