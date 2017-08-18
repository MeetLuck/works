# 7.9 Replacing Single Method Classes with Functions

try: # python 2.7
    from urllib2 import urlopen
except ImportError: # python >=3
    from urllib.request import urlopen

class UrlTemplate(object):
    def __init__(self,template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format(**kwargs))
    @staticmethod
    def test():
        yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
        for line in yahoo.open(names='DJI,IBM,AAPL,FB',fields='sl1c1v'):
            print line.decode('utf-8')  

def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format(**kwargs) )
    return opener

def urltemplate_test():
    yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
    for line in yahoo(names='^DJI,IBM,AAPL,FB',fields='snl1c1'):
        print line.decode('utf-8')  


if __name__ == '__main__':
#   UrlTemplate.test()
    urltemplate_test()


