import string, re
allChar = string.uppercase + string.lowercase
charToSoundex = string.maketrans(allChar, "91239129922455912623919292" * 2)
isOnlyChars = re.compile('^[A-Za-z]+$').search
def soundex(source):
    'convert string to Soundex equivalent'
    # Soundex requirements:
    # source string must be at least 1 character
    # and must consist entirely of letters
    if not isOnlyChars(source):
        return '0000'
    # Soudex algorithm:
    # 1. make first character uppercase
    # 2. translate all other characters to Soundex digits
    digits = source[0].upper() + source[1:].translate(charToSoundex)
    # 3. remove consecutive duplicates
    digits2 = digits[0]
    for d in digits[1:]:
        if digits2[-1] != d:
            digits2 += d
    # 4. remove all '9's
    digits3 = digits2.replace('9','')
    # 5. pad end with '0's to 4 characters
    while len(digits3)<4:
        digits3 += '0'
    # 6. return first 4 characters
    return digits3[:4]

if __name__ == '__main__':
    from timeit import Timer
    names = ('Woo', 'Pilgrim', 'Flingjingwaller')
    for name in names:
        statement = 'soundex("%s")' % name
        t = Timer(statement, 'from __main__ import soundex')
        print name.ljust(15), soundex(name), min(t.repeat() )

