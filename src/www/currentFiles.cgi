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

# Parse arguments
parseQuery
global args

if [catch {check_session} result] {
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
	# Call Process and return error 500 when a error is thrown
	# Exec ls $filepath, and return list to Web
	if [catch { set response [exec ls $filePath] } result] {

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
		set result [json_string $result]
		puts -nonewline "\{\"status\":\"success\",\"msg\":\"${result}\"\}"
	}
}

