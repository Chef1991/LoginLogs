#!/bin/bash

date="/usr/bin/date"
last="/usr/bin/last"
parser="./logParser.py"

btmp="/var/log/btmp"

sLog="./success.log"
fLog="./fail.log"

lastRun=`$date --date="1 day ago" +"%F %T"`
#loginS=$($last -isw "$lastRun")
#loginF=$($last -if /var/log/btmp -s "$lastRun")

$last -s "$lastRun" > $sLog
$last -f $btmp -s "$lastRun" > $fLog

$parser
