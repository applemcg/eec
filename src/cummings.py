#!/usr/bin/env python

# ------------------------------------ python libraries	--

import os
import sys
import fileinput

# -------------------------------------------- cummings	--

import datastructure
import machine
import builtin

def toStderr( msg):   sys.stderr.write(msg + '\n')

def builtinBehavior( token, frame, thisFrame, execution):
    """handles behavior of the very few eec syntax elements
    '(' -- opens a new frame,
    ',' -- moves to the next argument, and
    ')' -- executes the frame and pops the execution stack
    """
    toStderr( 'frame     ' + str(frame))
    toStderr( 'thisFrame ' + str(thisFrame))
    toStderr( 'token     ' + token)

    if token == '(':
        toStderr( 'handle open')
        return frame
    elif token == ',':
        toStderr( 'handle argument')
        return thisFrame
    elif token == ')':
        toStderr( 'handle close this is busy')
        frame.evaluate()
        rtn = execution.remove()
        toStderr(str(rtn.getName()) + ' = builtin POP ')
        return rtn
    else:
        raise KeyError( token + ' is NOT a Builtin: "(.)"' )

def toStderr( msg):   sys.stderr.write(msg + '\n')
        
def currentScope( token):
    """ 
    """
    rtn = token in builtin.tokens:

    toStderr(str(rtn) + ' = currentScope ' +  token )

    return rtn

def expectingNewToken( frame):
    """is true for 'definition' handlers
    """
    name    = frame.getName()
    handler = frame.getHandler() 
    #  since definitions and comments DONT know whats coming! 
    rtn     = (
                handler == parser.definition or
                handler == parser.comment
              )
    toStderr( str(rtn) + ' = expectingNewToken name: ' + name )
    return rtn 

def defineNew( token, frame):
    """creates, but does not stack, a frame for the
    token, it may be a variable, constant, etc...
    it returns the frame to the environment, waiting 
    for either a PAREN or COMMA
    """
    rtn = machine.Frame( token, frame)
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
    defer   = ''

    for c in line:

        # t = len(collect)
        # r = len(defer)
        # toStderr(' '*24 + c + ' ' + str(t)  + ' ' + str(r) )

        if state == 'escape':
            collect += c
            state = ''
            continue
            
        if c in empty and not len(collect):
            continue
                
        if c == escape:
            state = 'escape'
            continue

        if c == open or c == close or c == separ:

            stream.append( collect)
            stream.append( c)
            collect = ''
            defer   = ''
            continue

        if c in empty:
            # defer empty characters, for next non-empty
            defer += c

        elif len(defer):
            collect += defer
            collect += c
            defer    = ''

        else:
            collect +=c

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

    toStderr( ' '*42 + 'TOKEN: <' + token + '>')
    
    if token in '(,)':

        # decides to push on the stack a/o append to args.
        thisFrame = builtinBehavior(token, frame, thisFrame, execution)

    elif not currentScope( token):

        frame = execution.peek()

        if expectingNewToken( frame):

            # current frame holds the operative defining word

            thisFrame = machine.Frame( token, frame)
            print str(thisFrame)

        else:
            raise KeyError( token + ' not found')

    else:

        # the token is defined, so...
        frame = machine.Frame( token, frame)
        execution.insert( frame)

#
# ------------------------------------- end of Main	--
#
