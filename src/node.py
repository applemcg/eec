class Node(object):
    """A Node is the unit of data for an eec object.  It contains the
    NAME, HANDLER, ArgSPEC, PARENT, SLOT, and ARGLIST for an object.
    The PARENT is the runtime node for the specific instance of the 
    object, the SLOT is the list member in the ARGLIST to place a 
    return value or list.  For constants and variables, the ARGLIST
    is the (current if variable) value"""

    def __init__(self, name, handler, argspec, parent, slot):

        self.name    = name
        self.handler = handler
        self.argspec = argspec
        self.parent  = parent
        self.slot    = slot
        self.arglist = []
            
    def __str__(self):
        """show the object"""
        rtn  =   'Name:    ' + self.name 
        rtn += '\nHandler: ' + str(self.handler)
        rtn += '\nArgs:    ' + str(self.argspec)
        rtn += '\nParent:  ' + str(self.parent)
        rtn += '\nSlot:    ' + str(self.slot)
        rtn += '\nArgs:    ' + str(self.arglist)
        rtn += '\n------------------------------'
       
        return rtn

    def insertArg(self, arg):
        """Insert an arg, checking for room in the
        permissible range"""
        nargs = len(self.arglist)

        if okToAppend(self.argspec, nargs):
            self.arglist.append(arg)
        else:
            msg = str(nargs) + ' > ' + str( self.maxa)
            raise ValueError( self.name + ' arg violation ' + msg)

    def getName(self):
        return self.name
        
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


