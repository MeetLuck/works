''' Chapter 8. HTML Processing
>>> 8.1 Diving in
>>> 8.2 Introducing sgmllib.py
>>> 8.3 Extracting data from HTML documents
>>> 8.4 Introducing BaseHTMLProcessor.py
>>> 8.5 locals and globals
>>> 8.6 Dictionary-based string formatting
>>> 8.7 Quoting attribute values
>>> 8.8 Introducing dialect.py
>>> 8.9 Putting it all together
>>> 8.10 Summary
'''

'''
>>> SGMLParser parses HTML into userful pieces, like start tags and end tags.
    As soon as it succeeds in breaking down some data into a useful piece,
    it calls a method on itself based on what it found.
>>> In order to use the parser, you subclass the SGMLparser class and override these methods.
>>> SGMLParser parses HTML into 8 kinds of data, cand calls a seperate method for each of them

>>> 1. Start tag
    An HTML tag that starts a block like <html>,<head>,<body>, or <pre>, or a standalone tag
    like <br> or <img>.
>>> When it finds a start tag 'tagname', SGMLParser will look for a method called 'start_tagname' or 'do_tagname' 
    For instance, when it finds a <pre> tag, it will look for a start_pre or do_pre method.
    If found, SGMLParser calls this method with a list of the tag's attributes;
>>> otherwise, it calls 'unknown_starttag' with 'the tag name' and 'list of attributes'

>>> 2. End tag  :  'end_tagname'
>>> 3. Character reference : 'handle_charref'
>>> 4. Entity reference : 'handle_entityref'
>>> 5. Comment : 'handle_comment'
>>> 6. Processing instruction '<? ... >' : 'handle_pi'
>>> 7. Declaration '<! DOCTYPE html ..>' : 'handle_decl'
>>> 8. Text data  'A block of text'  Anything that does not into the other 7 categories : 'handle_data'



'''
