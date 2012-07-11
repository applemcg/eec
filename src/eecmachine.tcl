# eecmachine -- Copyright (C) 2012 -- JYATL, Just Yet Another Testing Lab
#  
proc eec_machinit {} {
    # TODO 9: find a use for the eec_var

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

    eec_perf mem
    puts stderr eec_mem:$cmd,$arg,$a.
    
    global eec_memory
    
    switch -- $cmd {
	
	set    { set  eec_memory($arg) $a }
	incr   { incr eec_memory($arg) $a }
	info   {
	    set res $arg
	    if {[info exists eec_memory($arg)]} {
		
		set res $eec_memory($arg)
	    }
	    return [string trim $res "{}"]
	}
    }
}
proc eec_info       arg       { eec_mem info $arg}
# BEGIN visible
proc eec_set       {a b}      { eec_mem set  $a $b }
proc eec_increment {a {b 1}}  { eec_mem incr $a $b }
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
    # TODO  2:  get the \X by the parser, so among others \n works

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

    switch -glob -- cmd.$sla {

	*.0   { eec_zero  $cmd                             }

	literal.1 {
	    eec_one   $cmd [lindex $args 0]
	}
	# TODO 1: increment isn't working, fix shud B simpel
	increment.1 { eec_increment      [lindex $args 0]  }

	increment.2 { eec_increment      [lindex $args 0] 
                               [eec_info [lindex $args 1]] } 

	*.1   { eec_one   $cmd [eec_info [lindex $args 0]] }

	*.2   { eec_two   $cmd [eec_info [lindex $args 0]] \
                             [eec_info [lindex $args 1]] }

	*.3   { eec_three $cmd [eec_info [lindex $args 0]] \
                             [eec_info [lindex $args 1]] \
		             [eec_info [lindex $args 2]] }

	default { eec_any $cmd [join $args ,]}
    }
}
eec_machinit
