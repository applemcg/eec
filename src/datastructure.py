class Queue(object):
    """A Queue is an order list set elements where
    objects are inserted at the tail of the list and 
    removed at the head of the list.  Queues are often
    called FIFOs: First In, First Out data structures."""

    def __init__(self):
        """Create an empty list"""
        self.vals = []

    def insert(self, e):
        """e can be any type -- can't it?
        and stores at the end"""
        self.vals.append(e)

    def remove(self):
        """removes the  head from  the list, restores  the list  with the
        former head removed, and  returns the head.  Raises ValueError
        if list is empty.
        """

        if len (self.vals) < 1:
            raise ValueError('Queue is empty')
        else:
            rtn = self.vals[0]
            self.vals = self.vals[1:]
            return rtn

    def __str__(self):
        """Returns a string representation of self"""
        return '(' + str(self.vals) + ')'

class Stack(object):
    """A Stack is an ordered list  of elements where objects are inserted
    at the top of  the stack and removed by 'popping'  the top off the
    stack.  Stacks are  often called  LIFOs: Last  In, First  Out data
    structures.
    """

    def __init__(self):
        """Create an empty Stack"""
        self.vals = []

    def isempty(self):
        """is the Stack empty"""
        return len (self.vals) < 1

    def insert(self, e):
        """e can be any type -- can't it?
        and stores at the end"""
        self.vals.append(e)

    def peek(self):
        """inspect the top of the stack without removing it.
        """
        if len (self.vals) < 1:
            raise ValueError('Stack is empty')
        else:
            return self.vals[-1]

    def remove(self):
        """pops the top element from the stack,
        Raises ValueError if the stack is empty"""
        if len (self.vals) < 1:
            raise ValueError('Stack is empty')
        else:
            return self.vals.pop()

    def __str__(self):
        """Returns a string representation of self"""
        return '(' + str(self.vals) + ')'
