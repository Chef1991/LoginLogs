__author__ = 'tylercook'
import csv


class GeoIP:

    def __init__(self):
        rows, _ = self.__parse_csv("geoip.csv")
        self.records = list()
        for row in rows:
            self.records.append({'start': int(row[2]), 'end': int(row[3]), 'country': row[4]})

    def get_country(self, ip):
        ip_int = 0
        if type(ip) is type(""):
            if '.' in ip:
                ip_int = self.ip_to_int(ip)
            else:
                ip_int = int(ip)
        else:
            ip_int = ip

        for record in self.records:
            if record['start'] <= ip_int <= record['end']:
                return record['country']
        return None




    @staticmethod
    def ip_to_int(ip_str):
        ip_bytes = ip_str.split('.')
        ip_int = int(ip_bytes[0]) << 24
        ip_int |= int(ip_bytes[1]) << 16
        ip_int |= int(ip_bytes[2]) << 8
        ip_int |= int(ip_bytes[3])
        return ip_int

    @staticmethod
    def __parse_csv(filename, header_row=False):
        """
        parse a csv into a 2d list
        :param filename:        str                         the path to the csv file
        :param header_row:       bool    Default:False       (Optional) True if the first row is the headers
        :return:                Tuple   (rows, header_row)   rows: rows[i][j]: i = row, j = column
                                                            header_row   Default:None    first row of csv iff header_row = True
        """
        rows = list()
        header = None
        with open(filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        if header_row:
            header = rows.pop(0)
        return rows, header

