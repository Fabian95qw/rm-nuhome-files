package require http

proc json_string {str} {
	set replace_map {
		"\"" "\\\""
		"\\" "\\\\"
		"\b"  "\\b"
		"\f"  "\\f"
		"\n"  "\\n"
		"\r"  "\\r"
		"\t"  "\\t"
	}
	return "[string map $replace_map $str]"
}

# Store parameters from QUERY_STRING in a key value array
proc parseQuery {} {
    global env
    global args

    set args("firstEntry") "a value"
	set query [array names env]
	if { [info exists env(QUERY_STRING)] } {
		set query $env(QUERY_STRING)
	}
	
	foreach item [split $query &] {
		if { [regexp {([^=]+)=(.+)} $item dummy key value] } {
			set args($key) $value
		}
	}
}

proc url-decode str {
    # rewrite "+" back to space
    # protect \ from quoting another '\'
    set str [string map [list + { } "\\" "\\\\"] $str]

    # prepare to process all %-escapes
    regsub -all -- {%([A-Fa-f0-9][A-Fa-f0-9])} $str {\\u00\1} str

    # process \u unicode mapped chars
    return [subst -novar -nocommand $str]
}

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

proc check_session { } {
	parseQuery
	global args
	
	if { [info exists args(sid)]} {
		set url "http://127.0.0.1/pages/index.htm?sid=$args(sid)"

		set httpresult [::http::geturl $url]
		set code [::http::code $httpresult]
		::http::cleanup $httpresult
		if { [string equal $code "HTTP/1.0 200 OK"] } {
			return 200;
		} else {
			return $code
		}
	} else {
		return -code error "authentication failed"
	}
} 
