#!/usr/bin/env python

# ------------------------------------ python libraries	--

import os
import sys
import fileinput

# -------------------------------------------- cummings	--

import datastructure
import machine
import parser

def builtinBehavior( token, frame, thisFrame):
    """handles behavior of the very few eec syntax elements
    '(' -- opens a new frame,
    ',' -- moves to the next argument, and
    ')' -- executes, closes, and pops the frame
    """
    print 'frame     ', str(frame)
    print 'thisFrame ', str(thisFrame)
    print 'token     ', token
    if token == '(':
        print 'handle open'
        return frame
    elif token == ',':
        print 'handle argument'
        return thisFrame
    elif token == ')':
        print 'handle close this is busy'
        frame.evaluate()
        return frame.pop()
    else:
        raise KeyError( token + ' is NOT a Builtin: "(.)"')

def toStderr( msg):   sys.stderr.write(msg + '\n')

        
def currentScope( token):
    """ 
    """
    rtn = token in parser.cummings

    toStderr(str(rtn) + ' = currentScope ' +  token )

    return rtn

def expectingNewToken( frame):
    """is true for 'definition' handlers
    """
    name     = frame.getName()
    handName = frame.getHandleName() 
    rtn      = handName == 'definition'

    toStderr( str(rtn) + ' = expectingNewToken,name ' + name )
    return rtn 

def defineNew( token, frame):
    """creates, but does not stack, a frame for the
    token, it may be a variable, constant, etc...
    it returns the frame to the environment, waiting 
    for either a PAREN or COMMA
    """
    rtn = machine.Frame( token, None)
    print str(rtn)

    return rtn

def eectokenizer(line):
    """parses the cummings tokens from a 
    line of text, returning the tokens in a list
    TBD: try this on a arbitrary stream of text.
    """
    empty  = ' \t\n'
    escape = '\\'
    state  = ''
    open   = '('
    close  = ')'
    separ  = ','

    stream = []

    collect = ''
    for c in line:
        
        if state == 'escape':
            collect += c
            state = ''
            continue
            
        if c in empty and not collect:
            continue
                
        if c == escape:
            state = 'escape'
            continue

        if c == open or c == close or c == separ:

            stream.append( collect)
            stream.append( c)
            collect = ''

        else:
            collect += c

    return stream

def inputStream():
    """reads STDIN and named files from argv[1:],
    treating a filename - as an alias for STDIN,
    returning the cummings tokens in a flattend list
    """
    # https://docs.python.org/2/library/fileinput.html
    tokens = []
    for line in fileinput.input():
        tokens.append( eectokenizer(line))

    return sum(tokens, [])
#
# ------------------------------------------------ Main	--
#

thisFrame = machine.Frame('interpreter', None)

execution = datastructure.Stack()
frame     = thisFrame      # THISFRAME is the working definition

execution.insert( frame)   # FRAME is the outer definition
                           #  frame( ..., thisframe [().]*, ...

for token in inputStream():

    if token in '(,)':

        # decides to push on the stack a/o append to args.
        thisFrame = builtinBehavior(token, frame, thisFrame)

    elif not currentScope( token):

        frame = execution.peek()

        if expectingNewToken( frame):

            raise KeyError( token + ' not found')

        else:

            # the stack frame tells what the operative 
            # defining word holds
            thisFrame = defineNew( token, frame)

    else:

        # the token is defined, so...
        frame = machine.Frame( token, frame)
        execution.insert( frame)


    #
    # ------------------------------------- end of Main	--
    #
