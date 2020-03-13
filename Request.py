import datetime
import json


class Request:
    def __init__(self,
                 req=['Mon', 'Jan', '1', '00:00:00', '1970', '1', '::ffff:0.0.0.0', '0', '/', 'b', '_', 'o', 'r', 'l',
                      'ftp', '0', '*', 'c']):
        # First splitting of the log string. OUTPUT => ["date + pid, user, ...", "client's ip", "empty", "empty", "requested file path", "bytes", "transfer speed"]
        self.file = req[8]  # file path requested from the client
        self.host = self.parseIp(req[6])  # ip of the client
        self.date = self.parseDate(req)  # date and hour when the request has been processed
        self.reqJson = self.getJson(self.file, self.host, self.date)

    # the date needs an elaboration to get a normal format (datetime)
    def parseDate(self, req):
        # here will be build a date in this format: year, month (in number), day (in number)
        date = [req[4], self.getMonth(req[1]), req[2]]

        # here will be build an hour in this format: hh, mm, ss

        hour = req[3].split(":")
        # converting date and hour from string to int
        date = list(map(int, date))
        hour = list(map(int, hour))

        # create a datetime object
        reqDate = datetime.datetime(date[0], date[1], date[2], hour[0], hour[1], hour[2], 0)

        return reqDate

    def parseIp(self, hostIp):
        hostIp = hostIp.split(":")
        return hostIp[3]

    # vsftpd log saves the month like string and not as number so we use a dictionary to change it
    def getMonth(self, i):
        switcher = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12,
        }
        return switcher.get(i, "Invalid month")

    def __str__(self):
        return json.dumps(self.reqJson, indent=4, sort_keys=True, default=str)

    def getJson(self, filePath, hostIp, date):
        return {"filePath": filePath, "hostIp": hostIp, "date": date}
