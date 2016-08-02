
def strong(text):
      return "<strong>{0}</strong>".format(text)
def p(text):
      return "<p>{0}</p>".format(text)

def get_text():
    return raw_input('enter text: ')

text = get_text()
decorated_text =  strong(text)
print decorated_text
#strong_decorated = strong_decorate()('it is paraggraph')
#print strong_decorated
#p_decorated = p_decorate()(strong_decorated)
#print p_decorated
