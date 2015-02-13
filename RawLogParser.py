#!/usr/bin/python

import re
import csv
import sys

class Log:
    def __init__(self, user, terminal, ip):
        self.ip = ip
        self.user = user
        self.terminal = terminal

    def asRow(self):
        return "%s,%s,%s" % (self.user, self.terminal, self.ip)

class CsvReport:
    header = ["Username","IP Address","Terminal"]
    def __init__(self, logs):
        self.logs = logs

    def __log2row(self, log):
        return [log.user, log.ip, log.terminal]

    def writeCSV(self, filename):
        with open(filename, "w") as csvfile:
            logwriter = csv.writer(csvfile)
            logwriter.writerow(self.header)
            for log in self.logs:
                logwriter.writerow(self.__log2row(log))


def getLines(filename):
    lines = list()
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines

def parseLog(lines):
    logs = list()
    r1 = "^(\w+)\s+([\w\d\/:]+)\s+([\d\.\w\-]+)"
    for line in lines:
        if "system boot" not in line and "wtmp" not in line and "btmp" not in line and len(line) > 0:
            match = re.search(r1, line)
            if match is not None:
                #print(match.group(1) + " -- " + match.group(2))
                log = Log(match.group(1), match.group(2), match.group(3))
                logs.append(log)
    if len(logs) > 0:
        return logs
    else:
        return None


def main():
    if len(sys.argv) is not 3:
        print("useage: %s log_file csv_file")
        exit()
    log_file = sys.argv[1]
    csv_file = sys.argv[2]

    lines = getLines(log_file)
    logs = parseLog(lines)
    report = CsvReport(logs)
    report.writeCSV(csv_file)

    """
    sLines = getLines("./success.log")
    fLines = getLines("./fail.log")
    
    s_logs = parseLog(sLines)
    s_report = CsvReport(s_logs)
    s_report.writeCSV("./reports/success.csv")

    f_logs = parseLog(fLines)
    f_report = CsvReport(f_logs)
    f_report.writeCSV("./reports/fail.csv")
    """

if __name__ == '__main__':
    main()
