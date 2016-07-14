''' Convert to and from Roman numerals '''

# Define exceptions
class RomanError(Exception):pass
class OutOfRangeError(RomanError):pass
class NotIntegerError(RomanError):pass
class InvalidRomanNumeralError(RomanError):pass

# Define digit mapping
romanNumeralMap = ( ('M',1000),
                    ('CM',900),
                    ('D',500),
                    ('CD',400),
                    ('C',100),
                    ('XC',90),
                    ('L',50),
                    ('XL',40),
                    ('X',10),
                    ('IX',9),
                    ('V',5),
                    ('IV',4),
                    ('I',1) )

def toRoman(n):
    ''' convert integer to Roman numeral '''
    if not (0<n<4000):
        raise OutOfRangeError,' number out of range (must be 1...3999)'
    if int(n) <> n:
        raise NotIntegerError, 'non-integers can not be converted'

    result =''
    for numeral, integer in romanNumeralMap:
        while n>=integer:
            result += numeral
            n -= integer
#           print 'substracting', integer, 'from input, adding', numeral,'to output'
    return result


def fromRoman(s):
    ''' convert Roman numeral to integer '''

    result = 0
    index = 0
    for numeral, integer in romanNumeralMap:
        while s[ index:index+len(numeral) ] == numeral:
            result += integer
            index += len(numeral)
#           print 'found',numeral, 'of length',len(numeral),',adding', integer
    return result


if __name__ == '__main__':
    print fromRoman('MCMLXXII')
