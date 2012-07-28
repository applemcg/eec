# eecparse -- Copyright (C) 2012 -- JYATL, Just Yet Another Testing Lab
#  
proc eec_init {} { 
    #   the key here is the eec_Token.  it starts with a non-blank,
    # may contain blanks and must end with a non-blank
    # leading and trailing spaces are trimmed of any blank-space.

    set tcl_precision 8

    global eec_Token
    global eec_firstSub
                                  # 2 nesting levels

    set eec_Token { *([_a-zA-Z0-9.:;$&*/+-]([ _a-zA-Z0-9.:;*/+-]*[_a-zA-Z0-9.:;])*) *} 
    
    set    eec_firstSub $eec_Token
    append eec_firstSub "\\("
}
proc eec_parse { eec } { 

    puts stderr eec_parse:$eec.
    
    global eec_firstSub

    set eec_REa  {, *EEC}     
    set eec_REb  "(\}) *EEC"

    # set up the sub-expresssions
    
    regsub -all $eec_firstSub $eec { EEC {\1} }       res
    
    # --- opportunity for a little RE learning ---
    
    puts stderr [format "\nBEFORE  SubExpression:\n%s<" $res]
    
    regsub -all $eec_REa           $res {    SubExpressionEEC} res
    regsub -all $eec_REb           $res {\1  SubExpressionEEC} res

    regsub -all {SubExpressionEEC ([^)]+)\)} $res {[EEC \1]} res
    regsub -all {SubExpressionEEC ([^)]+)\)} $res {[EEC \1]} res

    puts stderr [format "\nAFTER .. SubExpression:\n%s<" $res]

    eec_remain $res

} 
proc eec_remain {res} { 

    global eec_Token 

    # protect the blank-embedded EEC tokens
    
    regsub -all $eec_Token  $res { {\1} } res
    regsub -all "{ {($eec_Token)} }" $res {{\1}} res
    
    # trim the remaining stuff from the EEC syntax
    # TODO 3: Investigate Tcl Newline treatment, make multi-line cmmds.
    puts stderr [format "\nBEFORE Paren Strip:\n%s<" $res]
    regsub -all { *\) *}  $res ";"  res    
    puts stderr [format "\nAFTER  Paren Strip:\n%s<" $res]
    regsub -all { *, *}    $res " " res
    
    return $res
}
eec_init
