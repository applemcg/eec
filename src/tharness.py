

import parser
import machine
import datastructure
# print dir(machine)
# print dir(parser)

# print "="*52
# print parser.cummings
# print parser.handler
print "="*52

def framer( name, parent, *args):

    c = machine.Frame(name, parent)
    # print "="*52
    # print c
    # print "="*52

    for a in args:
        # print a
        c.insertArg(a)
        
    print "="*52
    print str(c)
    print "="*52

    c.evaluate()

framer( 'comment', 'interpreter', 'this is a comment', 'this is another')
