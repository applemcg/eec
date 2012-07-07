# eecparse -- Copyright (C) 2012 -- JYATL, Just Yet Another Testing Lab
# bkup: appleton.home./Users/applemcg/eec/src 2012_0707 114501;
#  
proc doeec {eec} { 

    eval [eec_parse [string trim $eec]]
}
proc eec_init {} { 
    #   the key here is the eec_Token.  it starts with a non-blank,
    # may contain blanks and must end with a non-blank
    # leading and trailing spaces are trimmed of any blank-space.

    set tcl_precision 8

    global eec_Token
    global firstSub
                                  # 2 nesting levels

    set eec_Token { *([_a-zA-Z0-9.:;$&*/+-]([ _a-zA-Z0-9.:;*/+-]*[_a-zA-Z0-9.:;])*) *} 
    
    set    firstSub $eec_Token   ;# puts EEC<$exp>
    append firstSub "\\("        ;# puts EEC<$exp>
}
proc eec_parse { eec {cmd eec_emit} {start eec_start}} {

    puts stderr eec_parse:$eec,$cmd,$start.

    global eec_Token
    global firstSub

    # set up the sub-expresssions
    
    regsub -all $firstSub $eec { EEC {\1} }        res
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

    set fp [open $name r]
    doeec [read $fp]
    close $fp
}
proc EEC {cmd args} {

    global eec_memory
    global eec_Token

    puts stderr "$cmd WITH: $args"
    set sla  [llength $args]

    # IDEA:   switch on SLA with N args expanded, then switch on command.

    switch -regex -- $cmd.$sla {

	comment.* { return }

	set.2   {
	    $cmd eec_memory([lindex $args 0]) [lindex $args 1]
	}
    include.1 {

        eec_include [lindex $args 0]
    }
	print.1 {
	    puts [eec_info [lindex $args 0]]
	}
	add.2 {
	    eec_biop [eec_info [lindex $args 0]] + [eec_info [lindex $args 1]]
	}
	multiply.2 {
	    eec_biop [eec_info [lindex $args 0]] * [eec_info [lindex $args 1]]
	}
	default { puts stderr "EEC has NO handle for <$cmd> with $sla ARGS." }

    }
}

proc eec_emit  { cmmd lval rval }  {

    puts stderr eec_emit:$cmmd,$lval,$rval.

    if { $cmmd == "" } {

	return $rval
    }
    puts stderr "$cmmd $lval $rval"
    global      $lval
    uplevel 1   "$cmmd $lval $rval"
}

  eec_init
