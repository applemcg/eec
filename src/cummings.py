#!/usr/bin/env python

import os
import sys

import datastructure
import machine
import parser

def expectingNewToken( frame):
    """is true for 'definition' handlers
    """
    name = frame.getName()
    return parser.cummings[name][1] == 'definition'

def defineNew( token)
    """creates, but does not stack, a frame for the
    token, it may be a variable, constant, etc...
    it returns the frame to the environment, waiting 
    for either a PAREN or COMMA
    """
    rtn = Frame( token, None)
    return rtn


thisFrame = Frame('interpretr', None)

execution = Stack()
frame     = thisFrame      # THISFRAME is the working definition

execution.insert( frame)   # FRAME is the outer definition
                           #  frame( ..., thisframe [().]*, ...

for token in inputStream():

    if token in '(,)':

        # decides to push on the stack a/o append to args.
        thisFrame = builtinBehavior(token, frame, thisFrame)

    elif not currentScope( token):

        frame = execution.peek()

        if not expectingNewToken( frame):

            raise KeyError( token + ' not found')

        else:

            # the stack frame tells what the operative 
            # defining word holds
            thisFrame = defineNew( token, frame)

    else: 
        # the token is defined, so...
        frame = Frame( token, frame)
        execution.insert( frame) 
        

            

        
