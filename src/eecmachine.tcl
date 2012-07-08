# eecmachine -- Copyright (C) 2012 -- JYATL, Just Yet Another Testing Lab
#  
proc eec_does {eec} { 

    eval [eec_parse [string trim $eec]]
}
proc eec_info arg {
    
    global eec_memory
    
    puts stderr eec_info:$arg.
    
    set res $arg
    if {[info exists eec_memory($arg)]} {
	
	set res $eec_memory($arg)
    }
    return $res
}
proc eec_biop {a op b} { 
    
    puts stderr eec_biop:$a,$op,$b.
    expr $a $op $b 
}
# BEGIN visible
proc eec_include name {
    
    if { ![file exists $name ]} {
	puts stderr "can't include $name, it's NOT a FILE."
	return
    }
    set fp [open $name r]
    eec_does [read $fp]
    close $fp
}
proc eec_set {a b} {

    global eec_memory

    set eec_memory($a) $b
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

proc eec_print    a            { puts $a }
proc eec_comment  args         { return } 
proc eec_list     args         {
    # TODO:  this needs eec_Token treatment, probably
    # at the EEC or eec_any level, before it gets here.
    # and probably a join args ","
    puts stderr eec_list:[llength $args]<$args>
    return $args
}
# END visible
proc EEC {cmd args} {

    global eec_Token

    puts stderr "$cmd WITH: $args"
    set sla  [llength $args]

    switch -- $sla {

	0   { eec_zero  $cmd                             }

	1   { eec_one   $cmd [eec_info [lindex $args 0]] }

	2   { eec_two   $cmd [eec_info [lindex $args 0]] \
                             [eec_info [lindex $args 1]] }

	3   { eec_three $cmd [eec_info [lindex $args 0]] \
                             [eec_info [lindex $args 1]] \
		             [eec_info [lindex $args 2]] }

	default { eec_any $cmd $args }
    }
}
eec_init
