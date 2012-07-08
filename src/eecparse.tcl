# eecparse -- Copyright (C) 2012 -- JYATL, Just Yet Another Testing Lab
# bkup: appleton.home./Users/applemcg/eec/src 2012_0707 114501;
#  
proc eec_does {eec} { 

    eval [eec_parse [string trim $eec]]
}
proc eec_init {} { 
    #   the key here is the eec_Token.  it starts with a non-blank,
    # may contain blanks and must end with a non-blank
    # leading and trailing spaces are trimmed of any blank-space.

    set tcl_precision 8

    global eec_Token
    global eec_firstSub
                                  # 2 nesting levels

    set eec_Token { *([_a-zA-Z0-9.:;$&*/+-]([ _a-zA-Z0-9.:;*/+-]*[_a-zA-Z0-9.:;])*) *} 
    
    set    eec_firstSub $eec_Token   ;# puts EEC<$exp>
    append eec_firstSub "\\("        ;# puts EEC<$exp>
}
proc eec_parse { eec } { 

    puts stderr eec_parse:$eec.

    global eec_Token
    global eec_firstSub

    # set up the sub-expresssions
    
    regsub -all $eec_firstSub $eec { EEC {\1} }        res
    regsub -all {, EEC}   $res { SubExpressionEEC} res
    
    # --- opportunity for a little RE learning ---
    
    regsub -all {SubExpressionEEC ([^)]+)\)} $res {[EEC \1]} res
    regsub -all {SubExpressionEEC ([^)]+)\)} $res {[EEC \1]} res
    
    # protect the blank-embedded EEC tokens
    
    regsub -all $eec_Token  $res { {\1} } res
    regsub -all "{ {($eec_Token)} }" $res {{\1}} res
    
    # trim the remaining stuff from the EEC syntax

    # puts stderr [format "BEFORE Paren Strip:\n%s<" $res]
    regsub -all { *\) *}  $res ";"  res       ;# N.B.   Investigate Tcl Newline treatment
    # puts stderr [format "AFTER  Paren Strip:\n%s<" $res]

    regsub -all { *, *}    $res " " res

    puts stderr [format "%-54s =>\n%s" $eec $res]

    return $res
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

proc eec_one      {cmd a}      { eec_$cmd $a }
proc eec_two      {cmd a b}    { eec_$cmd $a $b       }
proc eec_three    {cmd a b c}  { eec_$cmd $a $b $c    }
proc eec_any      {cmd args}   { eec_$cmd $args       }

proc eec_add      {a b}        { eec_biop $a + $b }
proc eec_subtract {a b}        { eec_biop $a - $b }
proc eec_multiply {a b}        { eec_biop $a * $b }
proc eec_divide   {a b}        { eec_biop $a / $b }

proc eec_print    a            { puts $a }
proc eec_comment  args         { return } 
proc eec_list     args         {
    # TODO:  this needs eec_Token treatment, probably
    # at the EEC or eec_any level, before it gets here.
    # and probably a join args ","
    puts stderr eec_list:[llength $args]<$args>
    return $args
}

proc EEC {cmd args} {

    global eec_Token

    puts stderr "$cmd WITH: $args"
    set sla  [llength $args]

    switch -- $sla {

	1   { eec_one $cmd [eec_info [lindex $args 0]]  }

	2   { eec_two $cmd [eec_info [lindex $args 0]]  [eec_info [lindex $args 1]] }

	default { eec_any $cmd $args }
    }
}

eec_init
