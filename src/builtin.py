# 

__version__ = "0.0 builtin.py"
__license__ = """Copyright (C) 2014, Marty McGowan, All rights reserved."""
__author__  = "Marty McGowan <mailto:mcgowan@alum.mit.edu>"

import sys
import machine

# def toStderr( msg):   sys.stderr.write(msg + '\n')
#
# ------------------------- builtin cummings definitions, code handlers	--
#

def ee_args( cmmd, nargs):
    """ handler stub"""

def ee_boolean( cmmd, nargs):
    """ handler stub"""

def ee_class( cmmd, nargs):
    """ handler stub"""

def ee_comment( cmmd, nargs):
    """ handler stub"""

def ee_constant( cmmd, nargs):
    """ handler stub"""

def ee_for( cmmd, nargs):
    """ handler stub"""

def ee_function( cmmd, nargs):
    """ handler stub"""

def ee_if( cmmd, nargs):
    """ handler stub"""

def ee_list( cmmd, nargs):
    """ handler stub"""

def ee_print( cmmd, nargs):
    """ handler stub"""

def ee_return( cmmd, nargs):
    """ handler stub"""

def ee_variable( cmmd, nargs):
    """ handler stub"""

def ee_while( cmmd, nargs):
    """ handler stub"""
#
# -------------------------------------------- working handler template	--
# 
# --------------------------------------------- handler characteristics	--
#
#
# . . .+. . . .|. . . .+. . . .*. . . .+. . . .|. . . .+. . . .*. . . \
# -------------------------------------------- cummings language tokens	--
#
token = {
    #                      argspec     handler        characteristics
    #                      --------  ------------  --------------------------
    'args'             : [ [0,'*'],  ee_args],     # variable number
    'boolean'          : [ [2],      ee_boolean],  # name [, class list], members
    'class'            : [ [2,3],    ee_class],    # name [, class list], members
    'comment'          : [ [0,'*'],  ee_comment],  # gobble input
    'constant'         : [ [2],      ee_constant], # name, immutable
    'for'              : [ [3],      ee_for],      # arg, list, body, .. return
    'function'         : [ [2,3],    ee_function], # name [, args], return
    'if'               : [ [2,3],    ee_if],       # boolean ,iftrue[, else]
    'list'             : [ [0,'*'],  ee_list],     # itema, itemb, ...
    'print'            : [ [0,2],    ee_print],    # assumes stdout, string, newline
    'return'           : [ [0,'*'],  ee_return],   # stmt, stmt, ...
    'variable'         : [ [2],      ee_variable], # name, value
    'while'            : [ [2],      ee_while],    # boolean, codeblock, e.g. return
}
#    compare 'token' to ../tst/starting.eec
# --------------------------------------------------- move to functions	--
#
#   'assert'           : [ [2,4,'*'],'bystate'],   # boolean, false message, ...
#   'concatenate'      : [ [1,'*'],  'bystate'],   # strings, .. a, b, c,
#   'expr'             : [ [1],      'bystate'],   # arithmatic expression
#   'equal'            : [ [2],      'bystate'],   # a == b
#   'greater or equal' : [ [2],      'bystate'],   # a >= b: 
#   'greater than'     : [ [2],      'bystate'],   # a > b
#   'less or equal'    : [ [2],      'bystate'],   # a <= b: 
#   'less than'        : [ [2],      'bystate'],   # a < b
#   'not equal'        : [ [2],      'bystate'],   # a != b, string or number
#   'printf'           : [ [0,'*'],  'bystate'],   # format, or filehandle, format, arg, ...
#

class old_builtin(object):
    """a builtin shares a state-aware method for its
    member words as builtin tokens in the language.
    a builtin supplies an argument handling specification
    and it's own method for state-dependent evalution.
    """

    def __init__(self, name, method):
        self.name    = namd
        self.method  = method
        self.builtin = {} 

    def insert(self, token, args, handler):
        self.builtin[token] = [args, handler]

class eetoken(object):
    """Forth has 'words', and it seems appropriate to call
    the cummings equivalent a 'token', i.e. the elementary
    execution token of the language.  builtins, constants,
    variables, functions, and classes"""

    def __init__(self, name, type):
    	self.name = name
        self.type = type

    def getType(self):
        return self.type

    def getName(self):
        return self.name

class storage(object):
    """either a constant, variable or list"""
    
    def set(self, value):
        self.value = value

    def get(self):
	return self.value

class builtin(eetoken):
    
    def property(self, args, handler):
        self.args    = args
        self.handler = handler

    def getArgs(self):
        return self.args

    def getHandler(self):
        return self.handler
    
class constant(storage):

    def __init__(self, name, type, value):
        me = storage(self, name, type)
        me.value = value

    def set(self, value):
        self.value = self.value

def Vocab():
    """returns the builtin vocabulary to the runtime environment"""

    vocabulary = {}

    for name, value in token.iteritems():

        args  = value[0]
        hdlr  = value[1]
        print   name + ' ' + str(args) + ' ' +  str(hdlr)

        vnod  = builtin(name,value)

        vnod.property( args, hdlr)
        vocabulary[name] = vnod

    for name in vocabulary:

        print 'type', str(vocabulary[name].getType()), 'name', name

    return vocabulary


