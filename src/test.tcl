source eecparse.tcl

proc comment {args} { }

comment  {
    eec_emit set  a   1
    eec_emit set  b   5
    eec_emit expr {} {$a + $b}
    eec_emit expr {} {$a - $b}
    
    eec_emit {}   {}  $a
    eec_emit {}   {}   a
    eec_emit {}   {}  $a
    
    eec_emit "puts stdout" {} {$a}
    eec_emit "puts stdout" {} {[eec_emit expr {} {$a + $b}]}
    
    eec_emit "puts stdout" {} {{a trimmed string}}
    
    eec_emit "proc"  {} {name {x y z} {expr $x + $y + $z}}

    eec_parse {
	
	set( a, 1)
	set( b, 2)
	print(stdout ,add (a, b))
    }
    
    # the key here is the eecToken.  it starts with a non-blank,
    #  alphanumeric, may contain blanks and must end with an
    #  alphanumeric.  leading and trailing spaces are trimmed
    #  of any blank-space.
    # nesting levels
    set eecToken { *([a-z0-9]([ a-z0-9]*[a-z0-9])*) *}  ;#     2
    set eecStart { *([,\(])*}                           ;#     1
    set eecEnd   {([,\)]) *}  
    ;#     1
    set exp      $eecStart$eecToken$eecEnd
    
    # set sub "1<\\1>2<\\2>4<\\4>"
    set sub "\\1\\2\\4"
    
    puts "Working: -------------"
    regsub      $exp " ( this )"       $sub that; puts $that
    regsub      $exp " , that )"       $sub that; puts $that
    regsub -all $exp " ( this, that )" $sub that; puts $that
    regsub -all $exp " ( this, 1 ) "   $sub that; puts $that
    regsub -all $exp " ( this , 1 ) "  $sub that; puts $that
    regsub -all $exp " ( th , 1 ) "    $sub that; puts $that
    regsub -all $exp " ( ok, now for a real challenge )" $sub that; puts $that
    regsub -all $exp " (or,is this, any tougher)" $sub that; puts $that
    regsub -all $exp " ( and, ( nested, expressions ) )" $sub that; puts $that
    
    regsub -all $exp " ( t , 1 ) "     $sub that; puts $that
    
    regsub -all $exp " ( a , 1 ) "     $sub that; puts $that
    
    puts "Real EEC: -------------"
    
    doeec { set ( a, 7)}
    doeec { fetch ( a) }
    doeec { define ( multi word token,   its replacement text  ) }
    doeec { set ( b, add(a,a))}
    doeec { set ( c, add(b,2,mult(a,a)))}
    
    puts "NOT Yet: -------------"
}
eec_include firstCircle.eec

