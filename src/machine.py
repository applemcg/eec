# machine.py

__license__ = """Copyright (C) 2014, Marty McGowan, All rights reserved."""
__author__  = "Marty McGowan <mailto:mcgowan@alum.mit.edu>"

# ------------------------------------------------- the argspec	--
# #args 
#
#       N   means the fixed # or permissible argument count
#    ----   -----
#       0    0
#       n    n
#     n,m    n, ..., m
#       n,   n, n+1, ...
#      ,m    0, ..., m
#     n,m,   n,m,m+i*(m-n),... 0 <= i <= ...
#

import parser
import sys

def toStderr( msg):   sys.stderr.write(msg + '\n')

def minArgs( nargs):
    """returns integer minimum number of permissible arguments
    or None from an argspec defined above.
    """
    return nargs[0]

def maxArgs( nargs):
    """returns integer maximum number of permissible argments
    or None from an argspec defined above.
    """
    t = nargs[-1]
    if t == '*':
        # unlimited number
        return None
    else:
        return t

def speArgs( nargs):
    """Detects open-ended (varargs) 
    """
    if len(nargs) < 3:
        # n, or m,n
        return None
    else:
        # m, n, n+i*(n-m), ... 0 <= i <= ...
        return 'function handling ' + str(nargs[0]) + ', ' + str(nargs[1])

def okToAppend( argspec, nargs):
    maxa = maxArgs(argspec)
    return (nargs < maxa or maxa == None)
