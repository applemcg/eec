# inputstream.py

__license__ = """Copyright (C) 2014, Marty McGowan, All rights reserved."""
__author__  = "Marty McGowan <mailto:mcgowan@alum.mit.edu>"

# ------------------------------------ python libraries	--

import fileinput
import os.path
import sys

def nestlevel( c, n):
    return c

    
def eectokenizer(line):
    """parses the cummings tokens from a 
    line of text, returning the tokens in a list
    TBD: try this on a arbitrary stream of text.
    """
    empty  = ' \t\n'
    escape = '\\'
    state  = empty
    open   = '('
    close  = ')'
    separ  = ','
    nada   = '' 
    nests  = 0
    nestc  = { open: 1, separ: 0, close: -1 }

    stream = []

    collect = nada
    defer   = nada

    for c in line:

        # t = len(collect)
        # r = len(defer)
        # toStderr(' '*24 + c + ' ' + str(t)  + ' ' + str(r) )

        if state == escape:
            collect += c
            state = empty
            continue
            
        if c in empty and not len(collect):
            # trim the leading space
            continue
                
        if c == escape:
            state = escape
            continue

        if c == open or c == close or c == separ:

            stream.append( collect)

            nests += nestc[c]
            stream.append( nestlevel(c, nests))
            collect = nada
            defer   = nada
            continue

        if c in empty:
            # defer empty characters, for next non-empty
            defer += c

        elif len(defer):
            collect += defer
            collect += c
            defer    = nada

        else:
            collect +=c

    return stream

def commandLineFileTokens():
    """reads STDIN and named files from argv[1:],
    treating a filename - as an alias for STDIN,
    returning the cummings tokens in a flattend list
    """
    # https://docs.python.org/2/library/fileinput.html

    tokens = []
    fname  = sys.argv[1]
    if (not os.path.isfile(fname)):
        fname = "stdin"

    for line in fileinput.input():
        tokens.append( eectokenizer(line))

    stream( sum(tokens, []), fname)

def nextToken():
    """return the next token from the command line files.
    this will get more clever when we can:
      a. include files, and 
      b. executed defined functions, ..."""
    
    return stream.current.getToken()

class stream(object):
    """to return cummings tokens from input files.
    these may include other files and token streams.
    the prev is the parent stream, the one invoking
    the new stream"""

    # http://www.diveintopython.net/object_oriented_framework/class_attributes.html
    current = None

    def __init__(self, tokens, file):

        self.tokens            = tokens
        self.file              = file
        self.next              = 0
        self.prev              = self.__class__.current
        self.__class__.current = self

    def getFile(self):
        return self.__class__.current.file

    def getToken(self):

        next = self.next
        self.next += 1

        try:
            return self.tokens[next]

        except:
            if (self.prev):
                self.__class__.current = self.prev
                return self.prev.getToken()

            else:
                exit ()


    

