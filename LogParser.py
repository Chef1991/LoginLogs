#!/usr/bin/python
import os

__author__ = 'tylercook'
import csv
import sys
import time
from PageGen import Table, Template

def get_lines(filename):
    lines = list()
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines

def parse_csv(filename, headerRow=False):
    """
    parse a csv into a 2d list
    :param filename:        str                         the path to the csv file
    :param headerRow:       bool    Default:False       (Optional) True if the first row is the headers
    :return:                Tuple   (rows, headerRow)   rows: rows[i][j]: i = row, j = column
                                                        headerRow   Default:None    first row of csv iff headerRow = True
    """
    rows = list()
    header = None
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    if headerRow:
        header = rows.pop(0)
    return (rows, header)

def get_ip_list(logs, descending=True, ip_index=1):
    """
    get a list of ips that appear in the logs and how many times they appear
    :param logs:            list(list)                  list of logs
    :param descending:      bool        Default:True    order the logs are sorted
    :param ip_index:        int         Default:1       index of the ip address in the log
    :return:                list(list)                  list[i][j], j=0: ip, j=1 count
    """
    ips = dict()
    for log in logs:
        ip = log[ip_index]
        if ip in ips:
            ips[ip] += 1
        else:
            ips[ip] = 1
    rtn = list()
    for ip, count in ips.items():
        rtn.append([ip, count])
    rtn = sorted(rtn, key=lambda l: l[1],reverse=descending)
    rtn.append(["Total", len(logs)])
    return rtn

def get_user_list(logs, uname_index=0):
    """
    get a list of usernames that appear in the logs and how many times they appear
    :param logs:            list(list)                  list of logs
    :param uname_index:     int         Default:0       index of the username in the log
    :return:                list(list)                  list[i][j], j=0: username, j=1 count
    """
    usernames = dict()
    for log in logs:
        user = log[uname_index]
        if user in usernames:
            usernames[user] += 1
        else:
            usernames[user] = 1
    rtn = list()
    for user, count in usernames.items():
        rtn.append([user, count])
    rtn = sorted(rtn, key=lambda l: l[1], reverse=True)
    rtn.append(["Total", len(logs)])
    return rtn

def __get_defaults():
    """
    returns a tuple of the defaults.
    Defaults:
        date: the current date.  Format: "mm/dd/yyyy"
        outputFile: $reports/logs.html, where reports is the reports directory
    :return:    Tuple   (date, outputFile)
    """
    date = time.strftime("%m/%d/%Y")
    base_dir = os.path.dirname(os.path.realpath(__file__))
    report_dir = "%s/reports" % base_dir
    output = "%s/logs.html" % report_dir
    return date, output

def __parse_args():
    """
    get variables that can be passed as arguments.  Returns the default
        from __get_defaults() if the argument is not specified
    :return:
    """
    date, out_file = __get_defaults()

    if '-h' in sys.argv or '--help' in sys.argv:
        print("TODO: help message")
        exit()
    if '-d' in sys.argv:
        index = sys.argv.index('-d') + 1
        if len(sys.argv) > index:
            date = sys.argv[index]
    if '-o' in sys.argv:
        index = sys.argv.index('-o') + 1
        if len(sys.argv) > index:
            out_file = sys.argv[index]
    return date, out_file



def __main():
    base_dir = os.path.dirname(os.path.realpath(__file__))
    report_dir = "%s/reports" % base_dir
    template_dir = "%s/templates" % base_dir

    template_file = "%s/loginReport.html" % template_dir
    success_file = "%s/success.csv" % report_dir
    fail_file = "%s/fail.csv" % report_dir

    date, out_file = __parse_args()


    success_data, success_header = parse_csv(success_file, True)
    success_table = Table(success_data, success_header)

    fail_data, fail_header = parse_csv(fail_file, True)
    fail_table = Table(fail_data, fail_header)

    s_ip_data = get_ip_list(success_data)
    s_ip_table = Table(s_ip_data, ["IP Address", "Count"])

    f_ip_data = get_ip_list(fail_data)
    f_ip_table = Table(f_ip_data, ["IP Address", "Count"])

    s_user_data = get_user_list(success_data)
    s_user_table = Table(s_user_data, ["Username", "Count"], t_class="userTable", css_id="sUserTable", style="color: green")

    f_user_data = get_user_list(fail_data)
    f_user_table = Table(f_user_data, ["Username", "Count"], t_class="userTable", css_id="fUserTable", style="color: red")
    keys = [
        {'key': '#DATE#', 'text': date},
        {'key': '#STABLE#', 'text': success_table.getHtml()},
        {'key': '#FTABLE#', 'text': fail_table.getHtml()},
        {'key': '#STABLE_IP#', 'text': s_ip_table.getHtml()},
        {'key': '#FTABLE_IP#', 'text': f_ip_table.getHtml()},
        {'key': '#STABLE_USER#', 'text': s_user_table.getHtml()},
        {'key': '#FTABLE_USER#', 'text': f_user_table.getHtml()},


    ]

    s_template = Template(template_file, keys)
    s_template.render(out_file)


if __name__ == '__main__':
    __main()

