#!/bin/tclsh

# Common functions
source /usr/local/etc/config/addons/www/nuhome-files/common.cgi

####################
# Global vars
####################
# File Path
set filePath "/usr/local/etc/config/addons/www/nuhome-files/data"
# Return content type
set content_type "application/json"
####################

proc process { } {
    global filePath
    # Parse arguments
    parseQuery
    global args
	# Unescape filename
    set fileName [url-decode $args(fileName)]
	# Full path of the file
    set fullPath "$filePath/$fileName"
	# Remove file
    exec rm $fullPath
    return "\{\"status\":\"success\",\"msg\":\"successfully removed file\"\}"
}

# Call Process and return error 500 when a error is thrown
if [catch {process} result] {

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
	puts "Content-Type: ${content_type}"
	puts "Status: 200 OK";
	puts ""
    # print json result in stdout
    # e.g {"status":"success","msg":"success"}
    puts -nonewline $result
}
