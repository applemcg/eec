# 

__version__ = "0.0 builtin.py"
__license__ = """Copyright (C) 2014, Marty McGowan, All rights reserved."""
__author__  = "Marty McGowan <mailto:mcgowan@alum.mit.edu>"

import sys
import machine

def toStderr( msg):   sys.stderr.write(msg + '\n')

#
# Here are the builtin cummings definitions and their 
# code handlers.


def boolean( cmmd, nargs):
    """handler stub"""
    
def comment( cmmd, nargs):
    """ throw out the comment's args
    """
    toStderr( str(cmmd))
    toStderr('throwing away args: ' + str(nargs))
        
def collection( cmmd, nargs):
    """handler stub"""
                
def decision( cmmd, nargs):
    """handler stub"""
                    
def definition_class(name, *args):
    """handler stub"""
                        
def definition_constant(name, *args):
    """handler stub"""
     # EDIT MARK -- add constant definition
                        
def definition_variable(name, *args):
    """handler stub"""
                            
def definition_function(name, *args):
    """handler stub"""
                                
definition_actions = {
    'class'      : definition_class,
    'constant'   : definition_constant,
    'variable'   : definition_variable,
    'function'   : definition_function
}
                                
def definition( cmmd, nargs):
    """handler stub"""
    toStderr( str(cmmd))
    try:
        definition_actions[cmmd]( nargs)
    except KeyError:
        print 'Unavailable Definition Action: ', cmmd
        
def empty( cmmd, nargs):
    """handler stub"""
        
    sys.stderr.write( str(cmmd))
    sys.stderr.write('throwing away args: ' + str(nargs))
        
def evaluation( cmmd, nargs):
    """handler stub"""
        
def io_print(*args):
    msg = ''
    if len(args) > 0:
        msg = args[0][0]
        print msg
            
def io_printf(fmt,*args):
    print fmt, args 
        
    
io_actions = {
    'print' : io_print,
    'printf': io_printf
}
                                                            
def io( cmmd, nargs):
    toStderr('\ncmmd: ' + cmmd)
    toStderr('\nnargs: ' + str(nargs))
        
    try:
        io_actions[cmmd]( nargs)
    except KeyError:
            print 'Unavailable IO Action: ', cmmd

def localargs( cmmd, nargs):
    """handler stub"""

def localexec( cmmd, nargs):
    """handler stub"""

def machine( cmmd, nargs):
    """handler stub"""

handler = {
    #     Name          handler
    'boolean'    : boolean,
    'comment'    : comment,
    'collection' : collection,
    'decision'   : decision,
    'definition' : definition,
    'empty'      : empty,
    'evaluation' : evaluation,
    'io'         : io,
    'localargs'  : localargs,
    'localexec'  : localexec,
    'machine'    : machine,
    ''           : None
}
# formerly cummings, now "token"
token = {
    #                      #args     handlerName      characteristics
    #                      --------  ------------     --------------------------
    'args'             : [ [0,'*'],  'localargs'],  # variable number
    'assert'           : [ [2,4,'*'],'decision'],   # boolean, false message, ...
    'class'            : [ [2,3],    'definition'], # name [, class list], members
    'comment'          : [ [0,'*'],  'comment'],    # gobble input
    'concatenate'      : [ [1,'*'],  'evaluation'], # strings, .. a, b, c,
    'constant'         : [ [2],      'definition'], # name, immutable
    'equal'            : [ [2],      'boolean'],    # a == b
    'expr'             : [ [1],      'evaluation'], # arithmatic expression
    'for'              : [ [3],      'decision'],   # arg, list, body, .. return
    'function'         : [ [2,3],    'definition'], # name [, args], return
    'greater or equal' : [ [2],      'boolean'],    # a >= b: 
    'greater than'     : [ [2],      'boolean'],    # a > b
    'if'               : [ [2,3],    'decision'],   # boolean ,iftrue[, else]
    'interpreter'      : [ [0],      'machine'],    # boolean ,iftrue[, else]
    'less or equal'    : [ [2],      'boolean'],    # a <= b: 
    'less than'        : [ [2],      'boolean'],    # a < b
    'list'             : [ [0,'*'],  'collection'], # itema, itemb, ...
    'not equal'        : [ [2],      'boolean'],    # a != b, string or number
    'print'            : [ [0,2],    'io'],         # assumes stdout, string, newline
    'printf'           : [ [0,'*'],  'io'],         # format, or filehandle, format, arg, ...
    'return'           : [ [0,'*'],  'localexec'],  # stmt, stmt, ...
    'variable'         : [ [2],      'definition'], # name, value
    'while'            : [ [2],      'decision'],   # boolean, codeblock, e.g. return
    ''                 : [ [0],      'empty']       # end of list place-holder
}
def eecBuiltin ():

    import node
    print dir(node)


    vocabulary = []

    for name, value in token.iteritems():
        args  = value[0]
        hnam  = value[1]
        hdlr  = handler[hnam]
        print   name + ' ' + str(args) + ' ' + hnam + ' ' +  str(hdlr)
        vnod  = node.Node(name, hdlr, args, None, 0)
        print   str(vnod)
        vocabulary.append( vnod)
        
    return vocabulary
