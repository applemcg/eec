#!/usr/bin/env python
# ./tds.py

from datastructure import *

s1 = Stack()
s1.insert( 'me')
s1.insert( 'myself')
s1.insert( 'If')

print s1

print s1.remove()
print s1.remove()

if not s1.isempty():  print s1.remove()
if not s1.isempty():  print s1.remove()
