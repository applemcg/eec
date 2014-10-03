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
# This parser reads the standard in and named file arguments of cummings
# source from the command line to produce a line-at-a-time ACTION, token
# pairs on the stdout further capable of code generation in a target
# language.
# 

import sys
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
def collection( cmmd, nargs):
    """handler stub"""
#
# ------------------------------------------- D	--
#
def decision( cmmd, nargs):
    """handler stub"""

def definition( cmmd, nargs):
    """handler stub"""

#
# ------------------------------------------- E	--
#
def empty( cmmd, nargs):
    """handler stub"""

def evaluation( cmmd, nargs):
    """handler stub"""

#
# ------------------------------------------- L	--
#
def localargs( cmmd, nargs):
    """handler stub"""

def localexec( cmmd, nargs):
    """handler stub"""

#
# ------------------------------------------------------------ builtins	--
#
#   args:
#       N   means the fixed # or permissible argument count
#    ----   -----
#       0    0
#       n    n
#     n,m    n, ..., m
#       n,   n, n+1, ...
#
#                         #args     handler       characteristics

handler = {

    'definition' : definition,
    'localargs'  : localargs,
    'localexec'  : localexec,
    'boolean'    : boolean,
    'decision'   : decision,
    'collection' : collection,
    'evaluation' : evaluation,
    'empty'      : empty
}

cummings = {

    'constant'         : [ [2],   'definition'], # immutable
    'variable'         : [ [2],   'definition'], # 
    'function'         : [ [2,3], 'definition'], # name[, args], return
    'args'             : [ [0,],  'localargs'],  # variable number
    'return'           : [ [0,],  'localexec'],  # stmt, stmt, ...
    'equal'            : [ [2],   'boolean'],    # a == b
    'not equal'        : [ [2],   'boolean'],    # a != b, string or number
    'less than'        : [ [2],   'boolean'],    # a < b
    'greater than'     : [ [2],   'boolean'],    # a > b
    'greater or equal' : [ [2],   'boolean'],    # a >= b: 
    'less or equal'    : [ [2],   'boolean'],    # a <= b: 
    'if'               : [ [2,3], 'decision'],   # boolean ,iftrue[, else]
    'while'            : [ [2],   'decision'],   # boolean, codeblock, e.g. return
    'for'              : [ [3],   'decision'],   # arg, list, body, .. return
    'list'             : [ [0,],  'collection'], # [ itema, itemb, ... ]
    'expr'             : [ [1],   'evaluation'], # arithmatic expression
    'concatenate'      : [ [2,],  'evaluation'], # strings, .. a, b, c,
    'comment'          : [ [0,],  'empty'],      # gobble input
    ''                 : [ [0],   'empty']       # end of list place-holder
    }

g_mem = []              # memory: constants, variables (incl lists), functions

def handlerFor(collect):

    if collect in cummings:
        argc = cummings[collect][0]
        name = cummings[collect][1]
        hdlr = handler[name]
        return name
    else:
        return ''

g_nest = 0
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


def interpreter(line):

    empty  = ' \t\n'
    escape = '\\'
    state  = ''
    open   = '('
    close  = ')'
    separ  = ','

    global collect
    
    for c in line:
        
        if state == 'escape':
            collect += c
            state = ''
            
        if c in empty and not collect:
            continue
                
        if c == escape:
            state = 'escape'
            continue
                    
        if c == open:
            collect = tokenis( collect,  1, 'OPEN')
            continue

        if c == close:
            collect = tokenis( collect, -1, 'CLOSE')
            continue

        if c == separ:
            collect = tokenis( collect,  0, 'SEPAR')
            continue

        collect += c

g_runtime = []		# stack: runtime nesting
g_frame = []            # frames are pushed on the runtime


def rt_frame ():
    print '========='
    print g_frame
    print '========='

def rt_runtime ():
    print "*************************"
    print len(g_runtime)
    print "*************************"

def rt_close( ):
    g_frame =  g_runtime.pop()
    rt_frame()

def rt_frameArg( arg ):
    g_frame.append( arg)
    rt_frame ()

def rt_stack( cmmd, args, handler):
    """
    push cmmd, args, handler on the frame list,
    holding a place in the fram for the args,
    push the frame stack on the runtime
    """
    g_frame.append( [cmmd, args, handler])
    g_runtime.append( g_frame)
    rt_runtime ()

def rt_init():

    global collect
    rt_stack('python', 0, interpreter)
    collect = ''

def main():
    """
    reads the stdin, parseing cummings source text,
    sending tokens and a nesting level to the tokenis function
    where the language processing may begin
    """

    rt_init() 

    for line in sys.stdin:
        interpreter(line)

main()
 
    
    
