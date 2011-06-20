#!/usr/bin/env tclsh
 
source	tclmklib

set	buildingLog building.tmp

state	running

obsolete	    eecMklib

doit	comment STATE $STATE

doit	comment	buildingLog $buildingLog

comment	NOT YET indir .hide glob ../*

set	CSource ""
set 	OBJECT ""

set 	SOURCE_C [list builtin compileobj dictionary main parserobj runtime string]

proc	c_one  { co cc } {
    global CSource;	lappend CSource $cc
    global OBJECT;	lappend OBJECT $co
    
  	  if { ! [newest $co $cc] } { puts stderr "time to recompile $cc" }
}

foreach	c $SOURCE_C { c_one $c.o $c.c }

puts	"here is CSource: $CSource.\nObj: $OBJECT"

punchin	goodtest

