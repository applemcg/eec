# 
# ---------------------------------------------- parser	-- 
#
#  (C) 2014, JYATL 
#
# Author: Marty McGowan, mcgowan@alum.mit.edu
# 
# This is the python-based cummings language parser.
# 
# cummings
# ========
# 
# The language is as syntax-free as one can make it.
# This 0.5 version parses cummings input into its
# four syntactic components:
# 
#   TOKEN
#   OPEN
#   SEPARATOR
#   CLOSE
# 
# as well as recognizing it's single escape mechanism,
# the backslash.   In the language, it is only possible
# to escape the syntactic elements:
# 
#   space        -- see following note
#   comma        -- the separator
#   left paren   -- the OPEN 
#   right paren  -- the CLOSE
# 
# the escape character may be used to capture other characters int a
# literal definition.  (see below)
# 
# a major feature of the language permits spaces in a token.
# 
# tokens
# ======
# 
# A Token is the longest sequence of (possibly escaped) characters,
# trimmed of its leading and trailing spaces, otherwise delimited by the
# non-space syntactic elements.  For parsing purposes a tab character is
# treated as a space.  so, for example,
# 
#   define ( TAB , \{literal tab} )   
#   define( ascii tab, TAB)
# 
# taken together, where "{literal tab}" is the single tab character, are
# two definitions of the tab character
# 
# syntax
# ======
# 
# The language syntax will look quite a bit like lisp or scheme, in that
# the function or operator appears first, followed by it's arguments:
# 
#    function ( arg, two-word arg, ... )
# 
# where arguments may be familiar single-word tokens or tne cummings
# innovation of the multi-word token.   Similarly function names may be
# multi-word.  
# 
# philosophy
# ==========
# 
# the language design builds the idea that all language features are 
# invoked, not by syntax, but by a word of meaningful sematics.
# i'm troubled by the modern profusion of what i'm calling syntactic
# noise.   e.g. python's substring operations  string[x:y] or 
# the object notation of object.method( arg, ...).  The former is
# better represented:
# 
#     substring( string, x, x)    comment ( and the latter)
#     method( object, arg, ...)
# 
# there's little excuse with today's smart editors to require noisy
# syntax, when the same helper could supply a simple mnemonic.
#
# the user will quickly realize the need for quotation marks is greatly
# reduced:
#
#    define( message, this message is available for timely display. )
#
# escaping leading or trailing spaces will retain them.
# 
# usage
# =====
#
#  This parser reads the standard input for cummings source to produce
#  a token-at-a-time behavior
#  ... as such, a work in progress
# 

import sys

def toStderr( msg):   sys.stderr.write(msg + '\n')

#
# ------------------------------------------------------------ handlers	--
#
# ------------------------------------------- B	--
#
def boolean( cmmd, nargs):
    """handler stub"""

#
# ------------------------------------------- C	--
#
def comment( cmmd, nargs):
    """ throw out the comment's args
    """
    toStderr( str(cmmd))
    toStderr('throwing away args: ' + str(nargs))
    

def collection( cmmd, nargs):
    """handler stub"""
#
# ------------------------------------------- D	--
#
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

#
# ------------------------------------------- E	--
#
def empty( cmmd, nargs):
    """handler stub"""

    sys.stderr.write( str(cmmd))
    sys.stderr.write('throwing away args: ' + str(nargs))


def evaluation( cmmd, nargs):
    """handler stub"""

#
# ------------------------------------------- I	--
#
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

#
# ------------------------------------------- L	--
#
def localargs( cmmd, nargs):
    """handler stub"""

def localexec( cmmd, nargs):
    """handler stub"""

#
# ------------------------------------------- M	--
#
def machine( cmmd, nargs):
    """handler stub"""

#
# ------------------------------------------------------------ builtins	--
#

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

cummings = {
#                           #args     handlerName     characteristics
#                          --------  ------------     --------------------------
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

#  where #args are describe in machine.py

g_nest = 0

def handlerFor(collect):

    if collect in cummings:
        argc = cummings[collect][0]
        name = cummings[collect][1]
        hdlr = handler[name]
        return name
    else:
        return ''


def nests(n):

    global g_nest
    if n:
        g_nest +=n
    
    return g_nest

def deliver( element, collect):

    print '%-6s %2d %12s %s' % ( element, nests(0), handlerFor(collect), collect)

def tokenis( collect, n, next):

    deliver( 'TOKEN', collect)

    # the TOKEN lives at the Current level

    if collect in cummings:
        argc = cummings[collect][0]
        name = cummings[collect][1]
        rt_stack( collect, argc, name)

    if n>0:
        nests(n)
    elif n == 0:
        rt_frameArg( collect)

    deliver( next,    '')

    # this is the place to POP the runtime stack
    if n<0:
        rt_close()
        nests(n)

    return ''

def openToken( collect):
    """open a frame for the collected token, 
    save the current token's frame argument as the parent of the new frame
    """

    if collect in cummings:
        frame = Frame(collect,"")    

def main():
    """
    reads the stdin, parseing cummings source text,
    sending tokens and a nesting level to the tokenis function
    where the language processing may begin
    """

    rt_init() 

    for line in sys.stdin:
        interpreter(line)

# main()
 
    
    
