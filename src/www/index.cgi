#!/bin/tclsh

package require logger
source /usr/local/etc/config/addons/www/nuhome-files/common.cgi

# Return content type
set content_type "application/json"
set logFile "/tmp/nuhome-files.log"
####################
####################
# Logger #
####################
# Writes log message to file
# alias for the logger functions
proc log_to_file {lvl txt} {
    global logFile
    set msg "\[[clock format [clock seconds]]\] $txt"
    set f [open $logFile {WRONLY CREAT APPEND}] ;# instead of "a"
    fconfigure $f -encoding utf-8
    puts $f $msg
    close $f
}
# Initialize logger
set log [logger::init global]
# Set alias to log_to_file; e.g calls to ${log}::info execute log_to_file
foreach lvl [logger::levels] {
    interp alias {} log_to_file_$lvl {} log_to_file $lvl
    ${log}::logproc $lvl log_to_file_$lvl
}
#######################


if [catch {check_session} result] {

    ${log}::info $result
	set status 500
	if { $errorCode != "NONE" } {
	    set status $errorCode
	}
	puts "Content-Type: ${content_type}"
	puts "Status: $status";
	puts ""
	set result [json_string $result]
    # print json result in stdout
    # e.g {"status":"error","msg":"file already exists"}
	puts -nonewline "\{\"status\":\"error\",\"msg\":\"${result}\"\}"

# Return Code 200 if successful
} else {
	set content [loadFile index.html]
	puts "Content-type: text/html\n"
	puts $content
}



