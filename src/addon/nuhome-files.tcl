#!/bin/tclsh

load tclrpc.so

##
# Hauptprogramm.
##
proc main { } 
{
	startup
}

##
# Startet die Zusatzsoftware.
# Stellt sicher, dass die Zusatzsoftware nur einmal ausgefüht wird und erstellt
# die PID-Datei.
##
proc startup { } {
  if {[isRunning]} then {
    error "already running"
  }

  writePidFile
	log "started"
}

#*******************************************************************************
# Einsprungpunkt
#*******************************************************************************

if { [catch { main } errorMessage] } then {
  log $errorMessage
  exit 1
}
