# eecmachine -- Copyright (C) 2012 -- JYATL, Just Yet Another Testing Lab
#  
proc eec_machinit {} {
    # TODO: find a use for the eec_var

    global eec_var

    # set eec_var(OUTPUT) stdout; bad idea!
}
proc eec_does {eec} { 

    eval [eec_parse [string trim $eec]]
}
proc eec_biop {a op b} { 
    
    puts stderr eec_biop:$a,$op,$b.
    expr $a $op $b 
}
# -------------------------------------------------- eec_memory	--
#
proc eec_info arg {
    
    global eec_memory
    
    puts stderr eec_info:$arg.
    
    set res $arg
    if {[info exists eec_memory($arg)]} {
	
	set res $eec_memory($arg)
    }
    return [string trim $res "{}"]
}
# BEGIN visible
proc eec_set {a b} {

    global eec_memory

    set eec_memory($a) $b
}
# ---------------------------------------------- END eec_memory	--
proc eec_include name {
    
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

proc eec_not      {a}          { expr ! $a         }

proc eec_print    {a args}     { 
    # TODO:  get the \X by the parser,
    #   so among others \n works

    global eec_var

    if {[llength $args]} {

	puts $a [eec_info [lindex $args 0]]

    } else {

	puts $a
    }
}
proc eec_comment  args         { return } 
proc eec_list     args         {
    # TODO:  this needs eec_Token treatment, probably
    # at the EEC or eec_any level, before it gets here.

    puts stderr eec_list:[llength $args]<$args>
    join $args ,
}
# END visible
proc EEC {cmd args} {

    global eec_Token

    set sla  [llength $args]
    puts stderr EEC.$cmd.n:$sla:$args

    switch -- $sla {

	0   { eec_zero  $cmd                             }

	1   { eec_one   $cmd [eec_info [lindex $args 0]] }

	2   { eec_two   $cmd [eec_info [lindex $args 0]] \
                             [eec_info [lindex $args 1]] }

	3   { eec_three $cmd [eec_info [lindex $args 0]] \
                             [eec_info [lindex $args 1]] \
		             [eec_info [lindex $args 2]] }

	default { eec_any $cmd [join $args ,]}
    }
}
eec_machinit
