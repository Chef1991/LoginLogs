#!/bin/bash

_script="$(readlink -f ${BASH_SOURCE[0]})"
_base="$(dirname $_script)"
_reports="$_base/reports"
_export="/shares/share1/reports"

date="/usr/bin/date"
last="/usr/bin/last"
lastb="/usr/bin/lastb"
rawParser="$_base/RawLogParser.py"
csvParser="$_base/LogParser.py"

sLog="$_base/success.log"
fLog="$_base/fail.log"
sCsv="$_reports/success.csv"
fCsv="$_reports/fail.csv"

lastRun=`$date --date="1 day ago" +"%F %T"`
runDay=`$date --date="1 day ago" +"%F"`
#loginS=$($last -isw "$lastRun")
#loginF=$($last -if /var/log/btmp -s "$lastRun")

$last -is "$lastRun" > $sLog
$lastb -is "$lastRun" > $fLog

$rawParser $sLog $sCsv
$rawParser $fLog $fCsv


$csvParser -d $runDay -o $_reports/login_$runDay.html

mkdir $_export/login_$runDay
mv $_reports/* $_export/login_$runDay