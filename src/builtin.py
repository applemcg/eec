# 

__version__ = "0.0 builtin.py"
__license__ = """Copyright (C) 2014, Marty McGowan, All rights reserved."""
__author__  = "Marty McGowan <mailto:mcgowan@alum.mit.edu>"

import sys
import machine

def toStderr( msg):   sys.stderr.write(msg + '\n')

#
# ------------------------- builtin cummings definitions, code handlers	--
#


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
#
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

#
# -------------------------------------------- working handler template	--
#
class ee_constant(object):

    def __init__(self, name):
        self.name  = name
        self.value = ''

    def assign(self, value):
        
        
    
def defining_class(name, *args):
    """handler stub"""

def executing_constant():                        
    

def defining_constant(name, *args):
    """handler stub"""
     # EDIT MARK -- add constant definition
                        
def defining_variable(name, *args):
    """handler stub"""
                            
def defining_function(name, *args):
    """handler stub"""
                                
defining_actions = {
    'class'      : defining_class,
    'constant'   : defining_constant,
    'variable'   : defining_variable,
    'function'   : defining_function
}
                                
def defining( cmmd, nargs):
    """handler stub"""
    toStderr( str(cmmd))
    try:
        defining_actions[cmmd](cummingstate, nargs)
    except KeyError:
        print 'Unavailable Definition Action: ', cmmd
#
# . . .+. . . .|. . . .+. . . .*. . . .+. . . .|. . . .+. . . .*. . . \
# --------------------------------------------- handler characteristics	--
# 
# * immediate -- like a comment, inside a definition or not, it
#   executes on the closing right paren
# 
# * defining -- it reserves memory for its instructions a/o data.
# 
# * bystate -- think of the global block as a compiled thread, laying down
#   code which is executed as if it were a comment. implies a STATE of the
#   interpreter.
#
#

interpreting = 1
compiling    = 0
cummingstate = interpreting

class builtin(object):
    """a builtin shares a state-aware method for its
    member words as builtin tokens in the language.
    a builtin supplies an argument handling specification
    and it's own method for state-dependent evalution.
    """

    def __init_(self)
        self.method = method
        self.builtin = {} 

    def insert(self, token, args, handler):
        self.builtin[token] = [args, handler]

# . . .+. . . .|. . . .+. . . .*. . . .+. . . .|. . . .+. . . .*. . . \

# -------------------------------------------- cummings language tokens	--
#
token = {
    #                      #args     handlerName     characteristics
    #                      --------  ------------    --------------------------
    'args'             : [ [0,'*'],  'bystate'],   # variable numberl
    'assert'           : [ [2,4,'*'],'bystate'],   # boolean, false message, ...
    'class'            : [ [2,3],    'defining'],  # name [, class list], members
    'comment'          : [ [0,'*'],  'immediate'], # gobble input
    'concatenate'      : [ [1,'*'],  'bystate'],   # strings, .. a, b, c,
    'constant'         : [ [2],      'defining'],  # name, immutable
    'equal'            : [ [2],      'bystate'],   # a == b
    'expr'             : [ [1],      'bystate'],   # arithmatic expression
    'for'              : [ [3],      'bystate'],   # arg, list, body, .. return
    'function'         : [ [2,3],    'defining'],  # name [, args], return
    'greater or equal' : [ [2],      'bystate'],   # a >= b: 
    'greater than'     : [ [2],      'bystate'],   # a > b
    'if'               : [ [2,3],    'bystate'],   # boolean ,iftrue[, else]
    'interpreter'      : [ [0],      'immediate'], # boolean ,iftrue[, else]
    'less or equal'    : [ [2],      'bystate'],   # a <= b: 
    'less than'        : [ [2],      'bystate'],   # a < b
    'list'             : [ [0,'*'],  'bystate'],   # itema, itemb, ...
    'not equal'        : [ [2],      'bystate'],   # a != b, string or number
    'print'            : [ [0,2],    'bystate'],   # assumes stdout, string, newline
    'printf'           : [ [0,'*'],  'bystate'],   # format, or filehandle, format, arg, ...
    'return'           : [ [0,'*'],  'bystate'],   # stmt, stmt, ...
    'variable'         : [ [2],      'defining'],  # name, value
    'while'            : [ [2],      'bystate'],   # boolean, codeblock, e.g. return
    ''                 : [ [0],      'bystate']    # end of list place-holder
}

def eetoken(Object):
    """Forth has 'words', and it seems appropriate to call
    the cummings equivalent a 'token', i.e. the elementary
    execution token of the language.  builtins, constants,
    variables, functions, and classes"""

    def __init__(self, name, type)
    	self.name = name
        self.type = type

    def getType(self):
        return self.type

    def getName(self):
        return self.name

def storage(eetoken):
    """either a constant, variable or list"""
    
    def set(self, value):
        self.value = value

    def get(self)
	return self.value

def builtin(eetoken):
    
    def property(self, args, handler):
        self.args    = args
        self.nandler = handler
    
def constant(storage):

    def __init__(self, name, type, value):
        me = storage(self, name, type)
        me.value = value

    def set(self, value):
        self.value = self.value
    


 
def eecBuiltin ():

    import node
    print dir(node)


    vocabulary = {}

    for name, value in token.iteritems():
        args  = value[0]
        hnam  = value[1]
        hdlr  = handler[hnam]
        print   name + ' ' + str(args) + ' ' + hnam + ' ' +  str(hdlr)

        vnod  = builtin(name, 'builtin')
        vnod.property( args, hdlr)
        vocabulary[name] = vnod
        
    return vocabulary
