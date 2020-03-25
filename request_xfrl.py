import datetime
import json


def get_json(file_path, host_ip, date, username):
    """
    this method will create a JSON with this format
    {
        file_path: "/etc",
        host_ip: "0.0.0.0"
        date: "2020-03-16 14:07:13"
    }
    """
    return {"file_path": file_path, "host_ip": host_ip, "date": date, "username": username}


def get_host_ip(req):
    """
    This method will return the IP in string format (ex. "192.168.1.1")
    """
    if req[2] == "":
        return req[7]
    else:
        return req[6]


def get_file(req):
    """
    This method will return the requested file in string format (ex. "/music/file.mp3")
    """
    if req[2] == "":
        return req[9]
    else:
        return req[8]


def get_username(req):
    """
    his method will return the username of the client in string format (ex. "lorenzo")
    """
    if req[2] == "":
        return req[14]
    else:
        return req[13]


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


def parse_date(req_date):
    """
    This method will elaborate the req_date an will return a normal date format (datetime)
    """
    print(req_date)
    # here will be build a date in this format: year, month (in number), day (in number)
    if req_date[2] == "":
        date = [req_date[5], get_month(req_date[1]), req_date[3]]
    else:
        date = [req_date[4], get_month(req_date[1]), req_date[2]]

    # here will be build an hour in this format: hh, mm, ss
    if req_date[2] == "":
        hour = req_date[4].split(":")
    else:
        hour = req_date[3].split(":")
    # converting date and hour from string to int
    date = list(map(int, date))
    hour = list(map(int, hour))

    # create a datetime object
    req_date = datetime.datetime(date[0], date[1], date[2], hour[0], hour[1], hour[2], 0)

    return req_date


class Request_xfrl:
    def __init__(self, req=['Mon', 'Jan', '1', '00:00:00', '1970', '1', '0.0.0.0', '0', '/', 'b', '_', 'o', 'r', 'l', 'ftp', '0', '*', 'c']):
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
        print(req)
        self.file = get_file(req)  # file path requested from the client
        self.host = get_host_ip(req)  # ip of the client
        self.date = parse_date(req)  # date and hour when the request has been processed
        self.username = get_username(req)
        self.req_json = get_json(self.file, self.host, self.date, self.username)

    # ///the date needs an elaboration to get a normal format (datetime)

    # vsftpd log saves the month like string and not as number so we use a dictionary to change it

    def __str__(self):
        """
        toString in JSON format
        """
        return json.dumps(self.req_json, indent=4, sort_keys=True, default=str)
