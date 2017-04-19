# --------------------- #
#     option group      #
# --------------------- #

# optparse
import optparse
# create OptionParser object
parser = optparse.OptionParser()
# create options group
group1 = optparse.OptionGroup(parser,'option group1')
group2 = optparse.OptionGroup(parser,'option group2')
# add option in the groups
group1.add_option('-t',help='group1 option',dest='t', action='store')
group2.add_option('-d',help='group2 option',dest='d', action='store')
# add groups to parsers
parser.add_option_group(group1)
parser.add_option_group(group2)
# parse arguments
opts, args = parser.parse_args()

# test
'''
> group.py -h
Usage: group.py [options]

Options:
      -h, --help  show this help message and exit

        option group1:
            -t T      group1 option

        option group2:
            -d D      group2 option

> group.py -t 20 -d string
opts:  {'t': '20', 'd': 'string'} args:  []
'''

print 'opts: ',opts, 'args: ',args
#print 'opts.multi: ',opts.multi
