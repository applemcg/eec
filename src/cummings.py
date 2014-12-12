#!/usr/bin/env python

__version__ = "cummings 0.07"
__license__ = "Copyright (C) 2014, Marty McGowan, All rights reserved."
__author__  = "Marty McGowan <mailto:mcgowan@alum.mit.edu>"

# ------------------------------------ python libraries	--

import os
import sys
import fileinput

# -------------------------------------------- cummings	--

import datastructure
import machine
import builtin
import stackframe

def toStderr( msg):   sys.stderr.write(msg + '\n')
        
def currentScope( token):
    """ 
    """
    global vocabulary

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
    rtn = stackframe.Frame( token, frame)
    print str(rtn)

    return rtn

def ee_interpreter():
    """the main loop. the default execution token.
    exits when all tokens are read and executed"""

    import inputstream
    
    for token in inputstream.nextToken():

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

        elif currentScope( token):        

            # the token is defined, so...
            frame = machine.Frame( token, frame)
            execution.insert( frame)
        else:
            # decides to push on the stack a/o append to args.
            # thisFrame = behavior(token, frame, thisFrame, execution)

            frame = execution.peek()

            if expectingNewToken( frame):

                # current frame holds the operative defining word

                thisFrame = machine.Frame( token, frame)
                print str(thisFrame)

            else:
                raise KeyError( token + ' not found')

#
# ------------------------------------------------ Main	--
#

def startup(name, args, hdlr):

    global vocabulary
    # EDIT MARK -- this looks like a bug, not a proper factor of args, hdlr, type?
    #
    # default hdlr is ee_interpreter
    #
    interp           = builtin.builtin(name, hdlr)
    interp.property( args, hdlr)
    runtime          = stackframe.Frame(name, hdlr)    
    vocabulary[name] = interp
    return runtime

vocabulary = builtin.Vocab()
runtime    = startup( 'interpreter', [0], ee_interpreter)


