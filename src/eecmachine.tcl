# eecmachine -- Copyright (C) 2012 -- JYATL, Just Yet Another Testing Lab
#  
#    starts with
#         eec ... file ...
#                  eec_include   file ...
#                  ... eec_does
#                      ... eval  eec_parse
#
proc eec_machinit {} {
    # TODO 7: find a use for the eec_var

    global eec_var

    # set eec_var(OUTPUT) stdout; bad idea!
}
proc eec_perf p     { 

    global eec_perfcount
    incr eec_perfcount($p)
}
proc eec_does {eec} { 

    eec_perf does
    eval [eec_parse [string trim $eec]]
}
proc eec_biop {a op b} { 

    eec_perf biop

    puts stderr eec_biop:$a,$op,$b.
    expr $a $op $b 
}
# -------------------------------------------------- eec_memory	--
#
proc eec_mem {cmd arg {a ""}} {
    # TODO 6: model eec_mem after lspproc's "storage" model,
    #  and add an inital value, e.g. storage name value,
    #  and create an "integer"  based on storage.

    eec_perf mem
    puts stderr eec_mem:$cmd,$arg,$a.
    
    global eec_memory
    
    switch -- $cmd {
	
	chk    { parray eec_memory }
	incr   { incr eec_memory($arg) $a }
	info   {
	    set res $arg
	    if {[info exists eec_memory($arg)]} {
		
		set res $eec_memory($arg)
	    }
	    return [string trim $res "{}"]
	}
	set    { set  eec_memory($arg) $a }
    }
}
proc eec_info       arg       { eec_mem info $arg}
# BEGIN visible
proc vocabulary    {a b}      {
    # TODO 4: vocabulary, see comments
    #  + its a stack,
    #  global ( sectional)
    #  vocabulary ( [ global ,] sectional
    #    pops the stack to the outer level
    # function address, sectional vars
    #    set ( name, "")
}
proc eec_set       {a b}      { eec_mem set  $a $b }
proc {eec_check memory} {}    { eec_mem chk  "" "" }
proc eec_increment {a {b 1}}  { 
    puts stderr eec_increment:a=$a,b=$b.
    eec_mem incr $a $b 
}
# ---------------------------------------------- END eec_memory	--
proc eec_include name {
    eec_perf include
    if { ![file exists $name ]} {
	puts stderr "can't include $name, it's NOT a FILE."
	return
    }
    set fp [open $name r]
    eec_does [read $fp]
    close $fp
}
# END visible

proc eec_zero     {cmd}        { eec_$cmd }
proc eec_one      {cmd a}      { eec_$cmd $a }
proc eec_two      {cmd a b}    { eec_$cmd $a $b       }
proc eec_three    {cmd a b c}  { eec_$cmd $a $b $c    }
proc eec_any      {cmd args}   { eec_$cmd $args       }

# BEGIN visible

proc eec_add      {a b}        { eec_biop $a +  $b }
proc eec_subtract {a b}        { eec_biop $a -  $b }
proc eec_multiply {a b}        { eec_biop $a *  $b }
proc eec_divide   {a b}        { eec_biop $a /  $b }
proc eec_greater  {a b}        { eec_biop $a >  $b }
proc eec_lessthan {a b}        { eec_biop $a <  $b }
proc eec_equal    {a b}        { eec_biop $a == $b }
proc eec_and      {a b}        { eec_biop $a && $b }
proc eec_or       {a b}        { eec_biop $a || $b }

proc eec_not       {a}          { expr ! $a        }
proc eec_literal    a           { return $a }

proc eec_print    {a args}     { 
    # TODO  1:  get the \X by the parser, so among others \n works

    eec_perf print

    global eec_var

    if {[llength $args]} {

	puts $a [eec_info [lindex $args 0]]

    } else {

	puts $a
    }
}
proc eec_comment  args         { return } 
proc eec_list     args         {

    puts stderr eec_list:[llength $args]<$args>
    join $args ,
}
# END visible
proc EEC {cmd args} {

    eec_perf EEC
    global eec_Token

    set sla  [llength $args]
    puts stderr EEC.$cmd.n:$sla:$args

    switch -- $sla {
	1   { set a [lindex $args 0] }
	2   {
	    set a [lindex $args 0]
	    set b [lindex $args 1]
	}
	3   {
	    set a [lindex $args 0]
	    set b [lindex $args 1]
	    set c [lindex $args 2]
	}	
    }

    switch -glob -- $cmd.$sla {

	*.0   { eec_zero  $cmd                      }

	literal.1 {
	    eec_one   $cmd $a
	}
	increment.1 { eec_increment $a              }

	increment.2 { eec_increment $a  [eec_info $b]}

	*.1   { eec_one   $cmd [eec_info $a]         }

	*.2   { eec_two   $cmd [eec_info $a]         \
                               [eec_info $b]         }

	*.3   { eec_three $cmd [eec_info $a]         \
		               [eec_info $b]         \
   		               [eec_info $c]         }

	default { eec_any $cmd [join $args ,]}
    }
}
eec_machinit
