# eestring.tcl -- the string handling functions

# BEGIN visible
proc eec_string {cmd string args} {

    puts stderr string:$cmd,$string,[llength $args],$args.

    switch -- $cmd {

	length    { string length $string }
	default   { puts stderr "string ( $cmd , string ... ) not implemented" }
    }
}

# END visible