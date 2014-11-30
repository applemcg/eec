#
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

class Frame(object):
    """A Frame  is a unit of data  for an eec object.  It  holds the name
    text  string or  None  for local  instantiations, the  permissible
    number of arguments, the handler function, a slot in the parent for
    a return value and a list of the actual arguments
    """

    def __init__(self, name, parent):
        """Create the frame for the next token"""

        import cummings

        self.name    = name
        self.parent  = parent
        self.slot    = None
        
        isParent = (not parent == None)
        toStderr('Frame.init: ' + name + ' parent: ' + str(isParent))
        # EDIT MARK.  time to referee the NODE and the FRAME.
        #   see the picture.
        if isParent:

            self.slot    = parent.getParentSlot()

        if not cummings.currentScope(name):

            try:
                name = parent.getName()
                toStderr('Frame.init: ' + name )

            except AttributeError:
                print str(parent)
                print name + ' has no parent' 

            except KeyError:
                print str(parent)

        toStderr( name)

        nargs = parser.cummings[name][0]
        
        self.mina    = minArgs(nargs)
        self.maxa    = maxArgs(nargs)
        self.argr    = speArgs(nargs)
        self.hnam    = parser.cummings[name][1]
        self.handler = parser.handler[self.hnam]
        
        self.args    = []
        
    def insertArg(self, arg):
        """Insert an arg, checking for room in the
        permissible range"""
        nargs = len(self.args)

        if nargs < self.maxa or self.maxa == None:
            self.args.append(arg)
        else:
            msg = str(nargs) + ' > ' + str( self.maxa)
            raise ValueError( self.name + ' arg violation ' + msg)

    def getName(self):
        return self.name
        
    def getHandleName(self):
        return self.hnam

    def getHandler(self):
        return self.handler

    def setParent(self, parent):
        """Allows the parent frame to attach separately
        """
        self.parent = parent

    def getParentSlot(self):
        """returns the arg# which receives the update
        """
        return len(self.args)

    def evaluate(self):
        """if the minimum arg count and any special arg handling, eg. 
        even, triplets, ... is reached evaluate the frame with the handler
        """
        nargs = len(self.args)

        if self.argr != None:
            if self.argr(self.args):
                self.parent = self.handler( name, handler, args)
            else:
                msg = str(nargs) + ' violates constraint ' + str( self.maxa)
                raise ValueError( self.name + ' arg violation ' + msg)

        elif self.mina <= nargs or self.mina == None:
            # this is where it happens!!
            self.parent = self.handler( self.name, self.args)
        else:
            msg = str(nargs) + ' > ' + str( self.maxa)
            raise ValueError( self.name + ' arg violation ' + msg)
            
    def __str__(self):
        """show the object"""
        rtn  =   'Name:    ' + self.name 
        # rtn += '\nParent:  ' + str(self.parent)
        rtn += '\nSlot:    ' + str(self.slot)
        rtn += '\nMina:    ' + str(self.mina)
        rtn += '\nMaxa:    ' + str(self.maxa)
        rtn += '\nArgr:    ' + str(self.argr)
        rtn += '\nHandler: ' + str(self.hnam)
        rtn += '\nArgs:    ' + str(self.args)
        rtn += '\n---------'
       
        return rtn



