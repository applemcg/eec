# inputstream.py

__license__ = """Copyright (C) 2014, Marty McGowan, All rights reserved."""
__author__  = "Marty McGowan <mailto:mcgowan@alum.mit.edu>"

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
            stream.append( c)
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
    for line in fileinput.input():
        tokens.append( eectokenizer(line))

    return sum(tokens, [])

def nextToken():
    """return the next token from the command line files.
    this will get more clever when we can:
      a. include files, and 
      b. executed defined functions, ..."""
    return commandLineFileTokens()

