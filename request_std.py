import datetime
import json


def get_json(filePath, hostIp, date, username):
    """
       this method will create a JSON with this format
       {
           file_path: "/etc",
           host_ip: "0.0.0.0"
           date: "2020-03-16 14:07:13"
           username: "Bob"
       }
    """
    return {"file_path": filePath, "host_ip": hostIp, "username": username, "date": date}


def parse_username(req):
    """
    This method will extract the username of the client from the request
    """
    req = req.split(" ")
    if req[2] == "":
        req = req[8]
        return req[slice(1, len(req) - 1)]
    else:
        req = req[7]
        return req[slice(1, len(req) - 1)]


def get_month(i):
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


def parse_date(req):
    """
    This method will elaborate the req_date an will return a normal date format (datetime)
    """
    req = req.split(" ")
    if req[2] == "":
        date = [req[5], get_month(req[1]), req[3]]
    else:
        date = [req[4], get_month(req[1]), req[2]]
    if req[2] == "":
        hour = req[4].split(":")
    else:
        hour = req[3].split(":")
    date = list(map(int, date))
    hour = list(map(int, hour))
    req_date = datetime.datetime(date[0], date[1], date[2], hour[0], hour[1], hour[2], 0)

    return req_date


class Request_std:
    def __init__(self, req=['Mon Jan  2 01:01:01 1970 [pid 22171] [lorenzo] OK DOWNLOAD: Client ', '0.0.0.0', ', ', '/', ', 0 bytes, 0.0Kbyte/sec']):
        """
        Expected a req like the default one
        From that some data will be extract. At the end there will be a Json with:
        data of the request, ip of the client, requested file, username of the client

        There are 5 attributes:
        - file: which represents the requested file
        - host: which represents the IP of the client
        - date: which represents the date when the request was made
        - username: which represents the username of the client
        - reqJson: which is a JSON with all this three information stored
        """
        # First splitting of the log string. OUTPUT => ["date + pid, user, ...", "client's ip", "empty", "empty", "requested file path", "bytes", "transfer speed"]
        self.file = req[3]  # file path requested from the client
        self.host = req[1]  # ip of the client
        self.username = parse_username(req[0])
        self.date = parse_date(req[0])  # date and hour when the request has been processed
        self.req_json = get_json(self.file, self.host, self.date, self.username)

    def __str__(self):
        """
            toString in JSON format
        """
        return json.dumps(self.req_json, indent=4, sort_keys=True, default=str)
