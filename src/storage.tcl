proc storage {name {value {}}} {
	# storage:
	#
	#   ~ name          creates a proc named "name" 
	#   ~ name value    creates and stores "value"
	#
	# the "name" interface is:
	#   name  Value;        stores "Value", such that
	#   name;               returns the Value
	#
	# basically, it 
	#    a. hides the global reference to the name, since
	#       all procs (sans the ugly namespace) are global, and
	#    b. tucks the value in a global connoting the process
	# 

	global storage_name
	puts [errout] storage:name,$name.

	eval [storage_proc $name $storage_name [storage_errmsg $name]] 

	if { $value != "" } {

			$name $value
	}
}
proc storage_errmsg name {

	switch -- $name {
		errout	{ return "" }
		default	{ format {puts [errout] %s,$value.} $name }
	}
}
proc storage_proc {name storage {err ""}} {

	puts stderr storage_proc:name,$name,storage,$storage,err,$err.

	format 	"
	proc %s {{value \"\"}} {
		global %s
		%s
		if { \$value != \"\" } {
			set %s(%s)  \$value
		}
		return \$%s(%s)
	}
	" $name $storage   $err   $storage $name    $storage $name
}
proc errout {}    { return stderr }        ;# egg hatches

proc storage_init { {name storage_global} }  {
	# storage_init:
	#   ~  [name {storage_global}]  -- the name of your storage unit
	#
	global storage_name
	puts  [errout] storage_init:name,$name.

	set storage_name   $name
}
proc storage_test {} {

	global test_glob

	storage_init test_glob

	storage STUNIT test_glob  		;#   think of a chain, or hierarchy

	storage ERRNAM storage_test.log

	storage errout [open [ERRNAM] a]

	storage OBJECT storage
	storage SPROCS "errout [info commands storage*]"

	close [errout]
	
	parray  test_glob
	puts stderr "unset test_glob "
}

  storage_init