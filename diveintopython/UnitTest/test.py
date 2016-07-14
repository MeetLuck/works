# Roman numerals must be less than 5000
MAX_ROMAN_NUMERAL = 26 

# Define digit mapping
romanNumeralMap = ( ('M',1000),
                    ('CM',900), ('D',500), ('CD',400), ('C',100),
                    ('XC',90), ('L',50), ('XL',40), ('X',10),
                    ('IX',9), ('V',5), ('IV',4), ('I',1) )
'''
>>> I  '1' >>> X  '10' >>> C  '100' >>> M '1000'
>>> IV '4' >>> XL '40' >>> CD '400'
>>> V  '5' >>> L  '50' >>> D  '500' 
>>> IX '9' >>> XC '90' >>> CM '900' 

>>> I       X-I     XX-I   XXX-I   XL-I   L-I
>>> II      X-II
>>> III     X-III
>>> IV      X-IV
>>> V       X-V 
>>> VI      X-VI 
>>> VII     X-VII
>>> VIII    X-VIII
>>> IX      X-IX 


'''

# Create tables for fast conversion of roman numerals
# See fillLookupTables() below
toRomanTable = [None] # Skip an index since Roman numerals have no zero
fromRomanTable = dict()

def toRomanDynamic(n):
    ''' convert integer to Roman numeral using dynamic programming'''
    no = n
    result = ''
    for numeral,integer in romanNumeralMap:
        if n >= integer:
            result = numeral
            n -= integer
            print '<result,no,n> : (%s,%s,%s)' %(result,no,n)
            break
    if n > 0:
        result += toRomanTable[n]
    print '\n<<<result,no,n>>> : (%s,%s,%s)\n' %(result,no,n)
    return result
def fillLookupTables():
    ''' compute all the possible roman numerals '''
    # Save the values in two global tables to convert to and from integers
    for integer in range(1, MAX_ROMAN_NUMERAL + 1):
        romanNumber = toRomanDynamic(integer)
        toRomanTable.append(romanNumber)
        fromRomanTable[romanNumber] = integer
#       print toRomanTable, fromRomanTable

fillLookupTables()

if __name__ == '__main__':
    print toRomanTable
    print fromRomanTable
