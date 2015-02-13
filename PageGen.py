__author__ = 'tylercook'

import csv


class Table:
    def __init__(self, data, headerRow=None, t_class=None, css_id=None, style=None):
        """

        :param data:            list(list)                  data[i][j] = cell at row i, col j
        :param headerRow:       list        Default:None    list of header elements
        :param t_class:         str         Default:None    the class of the table
        :param css_id:              str         Default:None    the css_id of the table
        :param style:           str         Default:None    the style for the table
        :return:
        """
        self.data = data
        self.headerRow = headerRow
        if t_class is None:
            self.css_class = ""
        else:
            self.css_class = "class=\"%s\"" % t_class
        if css_id is None:
            self.css_id = ""
        else:
            self.css_id = "id=\"%s\"" % css_id
        if style is None:
            self.style = ""
        else:
            self.style = "style=\"%s\"" % style

    def getHtml(self):
        html = "<table %s %s %s>" % (self.css_class, self.css_id, self.style)
        if self.headerRow is not None:
            html += self.__getHeader()
        for row in self.data:
            html += self.__getTR(row)
        return html + "</table>"

    def __getTR(self, row):
        html = "<tr>"
        for td in row:
            html += "<td>%s</td>" % td
        return html + "</tr>"

    def __getHeader(self):
        if self.headerRow is None:
            return ""
        html = "<tr>"
        for th in self.headerRow:
            html += "<th>%s</th>" % th
        return html + "</tr>"

class Template:
    def __init__(self, filename, keys):
        """

        :param filename:    str             the path to the template file
        :param keys:        list(dict)      key = the string to look for, value = the string to substitute
        :return:
        """
        self.filename = filename
        self.keys = keys
        self.templateLines = self.__getLines()

    def render(self, outFilename=None):
        """
        renders the template
        :param outFilename:     str     if specified will write the output to the specified file
        :return:                str     the rendered template
        """
        html = ""
        for line in self.templateLines:
            for key in self.keys:
                if key['key'] in line:
                    line = line.replace(key['key'], key['text'])
            html += line
        if outFilename is not None:
            self.__writeFile(html, outFilename)
        return html


    def __getLines(self):
        lines = list()
        with open(self.filename, "r") as f:
            lines = f.readlines()
        return lines

    def __writeFile(self, html, filename):
        with open(filename, "w") as f:
            f.write(html)






