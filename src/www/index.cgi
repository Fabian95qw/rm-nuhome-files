#!/bin/tclsh

proc loadFile { fileName } {
	set content ""
	set fd -1
	
	set fd [ open $fileName r]
	if { $fd > -1 } {
		set content [read $fd]
		close $fd
	}
	
	return $content
}

# Just load index.html

set content [loadFile index.html]
puts "Content-type: text/html\n"
puts $content