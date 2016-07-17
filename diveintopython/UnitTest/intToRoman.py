romanNumeralMap = \
[ ('M',1000), ('CM',900),('D',500),('CD',400),('C',100),
  ('XC',90),('L',50),('XL',40),('X',10),
  ('IX',9),('V',5),('IV',4),('I',1) ]

def int_to_roman(n):
    ''' convert an n to Roman numerals '''
    result,r = '',n
    for numeral, i in romanNumeralMap:
        q, r = divmod(r,i)
        result += numeral * q
#       print numeral, i,' -> ', q,result,r
    return result

def toRoman(n):
    result = ''
    for numeral, i in romanNumeralMap:
        while n >= i:
            result += numeral
            n -= i
    return result
def main():
    ''' doctest for integer To Roman Numerals
    >>> import roman
    >>> assert int_to_roman(3520) == roman.toRoman(3520) 
    >>> assert int_to_roman(2940) == roman.toRoman(2940) 
    >>> assert int_to_roman(1024) == roman.toRoman(1024) 
    >>> assert int_to_roman(540) == roman.toRoman(540) 
    >>> assert int_to_roman(95) == roman.toRoman(95) 
    >>> assert int_to_roman(53) == roman.toRoman(53) 
    >>> assert int_to_roman(25) == roman.toRoman(25) 
    >>> assert int_to_roman(9) == roman.toRoman(9) 
    >>> assert toRoman(3520) == roman.toRoman(3520) 
    >>> assert toRoman(2940) == roman.toRoman(2940) 
    >>> assert toRoman(1024) == roman.toRoman(1024) 
    >>> assert toRoman(540) == roman.toRoman(540) 
    >>> assert toRoman(95) == roman.toRoman(95) 
    >>> assert toRoman(53) == roman.toRoman(53) 
    >>> assert toRoman(25) == roman.toRoman(25) 
    >>> assert toRoman(9) == roman.toRoman(9) 
    '''
if __name__ == '__main__':
    import doctest
    doctest.testmod()
#   int_to_roman(3520)
#   int_to_roman(1024)
#   int_to_roman(510)


