from sgmllib import SGMLParser
class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = list()
    def start_a(self, attrs):
        href = [ v for k,v in attrs if k=='href']
        if href:
            self.urls.extend(href)


if __name__ == '__main__':
    import urllib
    usock = urllib.urlopen('http://www.diveintopython.net')
    parser = URLLister()
    parser.feed( usock.read() )
    usock.close()
    parser.close()
    for url in parser.urls : print url
