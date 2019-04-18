#!/bin/tclsh

# Common functions
source /usr/local/etc/config/addons/www/nuhome-files/common.cgi

#packages
package require http
package require logger

####################
# Global vars
####################
# Enviroment array
global env
# Return content type
set content_type "application/json"
# Log file full path
set logFile "/tmp/nuhome-files.log"
# File Path
set filePath "/usr/local/etc/config/addons/www/nuhome-files/data"
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

#######################
# Procedures #
#######################
proc logQuery {} {
    global env
    global log
    #print each entry to log
    foreach key [array names env] {
        ${log}::info  "ENV : $key=$env($key)"
    }
}
# Check if request method is POST
proc isPost {} {
    global env

    if { [info exists env(REQUEST_METHOD)] } {

        set reqMethod $env(REQUEST_METHOD)
        set result [string equal $reqMethod "POST"]

        if { $result == 1 } {
            return true
        }
    }
    return false
}

# Processes POST
proc process { } {

    global log
    ${log}::info "inserting log"

    # Define globals in current scope
    ${log}::info "inserting env"
    global env
    ${log}::info "inserting filePath"
    global filePath
    
    ${log}::info "Starting Execution"
    # Check if request is a post
    set isPostVar [isPost]
    # If it isnt return a json error
    if { $isPostVar == "false" } {
        return "\{\"status\":\"error\",\"msg\":\"unsupported request method use post\",\"code\":\"500\"\}"
    }

    # Parse arguments
    parseQuery
    ${log}::info "query parsed"
    # parseQuery processes args
    # use args from global scope
    global args

    # Unescape filename
    set fileName [url-decode $args(fileName)]
	# Full path of the file
    set fullPath "$filePath/$fileName"

    # Check if file already exists
    # throw error with msg "file already exists"
    if { [file exists $fullPath] == 1} {
        set jsonResult "Datei existiert bereits"
        return "\{\"status\":\"error\",\"msg\":\"${jsonResult}\"\}"
    }

	catch {fconfigure stdin -translation binary}
	catch {fconfigure stdin -encoding binary}
	set out [open $fullPath w]
	catch {fconfigure $out -translation binary}
	catch {fconfigure $out -encoding binary}
    # Write from stdin to file
	
	set data [read stdin]
	 
	# Cut off first 4 Lines, because they're header data, and not actual Filedata
	set data [join [lrange [split $data \n] 4 end] \n] 
	
	#Cutt off last Line, because thats the closing line of the Data
	set index [string last "\n" $data end-1]
	set data [string range $data 0 $index]
	 
	 
	# Write rest to file
	puts -nonewline $out $data

	close $out

    # return result
    set jsonResult "successfully uploaded file"
    return "\{\"status\":\"success\",\"msg\":\"${jsonResult}\"\}"
}
#########################
#########################
# Start #
#########################

# Create directory if it doesnt exist yet
exec mkdir -p $filePath

${log}::info "processing"
# Call Process and return error 500 when a error is thrown
if [catch {process} result] {

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
	puts "Content-Type: ${content_type}"
	puts "Status: 200 OK";
	puts ""
     # print json result in stdout
    # e.g {"status":"success","msg":"success"}
	puts -nonewline $result
}

${log}::info "Stopping Execution"