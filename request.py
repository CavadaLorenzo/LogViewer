import datetime
import json


def get_json(filePath, hostIp, date):
    """
    this method will create a JSON with this format
    {
        filePath: "/etc",
        hostIp: "0.0.0.0"
        date: "2020-03-16 14:07:13"
    }
    """
    return {"filePath": filePath, "hostIp": hostIp, "date": date}


class Request:
    def __init__(self, req=['Mon', 'Jan', '1', '00:00:00', '1970', '1', '::ffff:0.0.0.0', '0', '/', 'b', '_', 'o', 'r', 'l', 'ftp', '0', '*', 'c']):
        """
        Expected a req like the default one

        There are 4 attributes:
        - file: which represents the requested file
        - host: which represents the IP of the client
        - date: which represents the date when the request was made
        - reqJson: which is a JSON with all this three information stored
        """
        self.file = req[8]  # file path requested from the client
        self.host = self.parseIp(req[6])  # ip of the client
        self.date = self.parseDate(req)  # date and hour when the request has been processed
        self.req_json = get_json(self.file, self.host, self.date)

    # ///the date needs an elaboration to get a normal format (datetime)
    def parseDate(self, req_date):
        """
        This method will elaborate the req_date an will return a normal date format (datetime)
        """
        # here will be build a date in this format: year, month (in number), day (in number)
        date = [req_date[4], self.getMonth(req_date[1]), req_date[2]]

        # here will be build an hour in this format: hh, mm, ss

        hour = req_date[3].split(":")
        # converting date and hour from string to int
        date = list(map(int, date))
        hour = list(map(int, hour))

        # create a datetime object
        reqDate = datetime.datetime(date[0], date[1], date[2], hour[0], hour[1], hour[2], 0)

        return reqDate

    def parseIp(self, hostIp):
        """
        This method will get an Ip in the format ffff::0.0.0.0 and will return a normal ip (ex. 0.0.0.0)
        """
        hostIp = hostIp.split(":")
        return hostIp[3]

    # vsftpd log saves the month like string and not as number so we use a dictionary to change it
    def getMonth(self, i):
        """
        This method is just a switcher to convert months from string (ex: Jan, Feb, ...) to number (ex: 1, 2, ...)
        """
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
        """
        toString in JSON format
        """
        return json.dumps(self.req_json, indent=4, sort_keys=True, default=str)
