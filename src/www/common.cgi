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