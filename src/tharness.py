#!/usr/bin/env python

import os
import sys

import datastructure
import machine
import parser

# print dir(machine)
# print dir(parser)

# print "="*52
# print parser.cummings
# print parser.handler

def framer( name, parent, slot, *args):

    c = machine.Frame(name, parent, slot)
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

thisFrame = Frame('interpretr', None)
print thisFrame

framer( 'comment', thisFrame, 'this is a comment', 'this is another')
