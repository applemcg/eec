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

def toStderr( msg):   sys.stderr.write(msg + '\n')
        
def currentScope( token):
    """ 
    """
    rtn = token in vocabulary

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

def ee_interpreter():
    """the main loop. the default execution token.
    exits when all tokens are read and executed"""
    
    for token in nextToken():

        toStderr( ' '*42 + 'TOKEN: <' + token + '>')
    
        if token == '(':
            toStderr( 'handle open')
            thisFrame = frame
        elif token == ',':
            toStderr( 'handle argument')
            thisFrame = thisFrame
        elif token == ')':
            toStderr( 'handle close this is busy')
            frame.evaluate()
            rtn = execution.remove()
            toStderr(str(rtn.getName()) + ' = builtin POP ')
            thisFrame =  rtn

            # decides to push on the stack a/o append to args.
            # thisFrame = behavior(token, frame, thisFrame, execution)

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
# ------------------------------------------------ Main	--
#
import builtin

def startup(name, args, hdlr, vocabulary):

    interp           = builtin.builtin(name)
    interp.property( args, hdlr)
    runtime          = Frame(name, None)    
    vocabulary[name] = interp
    return (runtime, vocabulary)

(runtime, vocabulary) = startup( 'interpreter', [0], ee_interpreter, builtin.Vocab())

