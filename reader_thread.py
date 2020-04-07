import threading
import time
from request_xfrl import Request_xfrl
from request_std import Request_std
from datetime import timedelta
from logger import update_log
from database import Database

r"""Thread which actually read and parse the line of the log file

This class handle the thread which will read the line of the log file,
it will parse each line getting only the useful information and will upload
them to a common InfluxDB database.


"""


class Reader(threading.Thread):
    """
    Represent the file-reader of the system
    Attributes:
        -name: name of the file, useful to identify to which server has been done a request
        -file: represent the actual log file to read
    """

    def __init__(self, name, file):
        """
        This class will run the reading process from the log file.
        There are 2 attributes needed:
        -name: unique identify of the logviewer instance
        -file: file object where the log are stored
        """
        self.db = Database()
        threading.Thread.__init__(self)
        self.name = name
        self.file = file

    def run(self):
        """
        Main method of the class, first of all it will run the check of the type of the log file
        and then it will run the right request parser.
        """
        print("Reading from: " + self.name)
        update_log(text="READING FROM FILE " + self.name + "\n")
        log_type = self.check_log_type()

        if log_type:
            self.read_file_in_xfrl_mode()
        else:
            self.read_file_in_std_mode()

    def read_file_in_xfrl_mode(self):
        """
        This method consist in a while True which will constantly check the log file (in xfrelog standard mode to see if
        there is new entry. If not the thread will sleep for 3 seconds, although it will parse the request.
        Is possible that Kodi will do more than 1 request for the same file. To prevent that the script will save the
        same request more than once, the last request is saved and is compered with the new one. A request is new
        if is different from the previous one or if is pass at least 10 seconds from the previous one.
        """

        self.file.seek(0, 2)
        old_request = Request_xfrl()
        while True:
            where = self.file.tell()
            line = self.file.readline()
            if not line:
                time.sleep(3)
                self.file.seek(where)
            else:
                old_request = self.parse_new_line_xfrl(line, old_request)

    def read_file_in_std_mode(self):
        """
        This method consist in a while True which will constantly check the log file (in standard mode to see if
        there is new entry. If not the thread will sleep for 3 seconds, although it will parse the request.
        Is possible that Kodi will do more than 1 request for the same file. To prevent that the script will save the
        same request more than once, the last request is saved and is compered with the new one. A request is new
        if is different from the previous one or if is pass at least 10 seconds from the previous one.
        """

        self.file.seek(0, 2)
        old_request = Request_std()
        while True:
            where = self.file.tell()
            line = self.file.readline()
            if not line:
                time.sleep(3)
                self.file.seek(where)
            else:
                old_request = self.parse_new_line_std(line, old_request)

    def parse_new_line_xfrl(self, line, old_request):
        """
        This method will analise the new line of the log file (which is in xferlog standard mode), if a download
        is found it will, create an object Request_xfrl and add the new request to the database if is a new one.
        """
        line = line.split(" ")
        if line[len(line) - 1] == "c\n" or line[len(line) - 1] == "c":
            request = Request_xfrl(line)
            if request.req_json["file_path"] != old_request.req_json["file_path"] or request.req_json["date"] > (
                    old_request.req_json["date"] + timedelta(seconds=10)):
                print("PARSED REQUEST RECEIVED AT: " + self.name + "\n" + str(request))
                update_log(text="PARSED REQUEST RECEIVED AT: " + self.name + "\n" + str(request))
                self.db.update_database(self.name, request)
                old_request = request
        return old_request

    def parse_new_line_std(self, line, old_request):
        """
        This method will analise the new line of the log file (which is in standard mode), if a download is found it
        will, create an object Request_std and add the new request to the database if is a new one.
        """
        if "OK DOWNLOAD" in line:
            line = line.split("\"")
            request = Request_std(line)
            if request.req_json["file_path"] != old_request.req_json["file_path"] or request.req_json["date"] > (
                    old_request.req_json["date"] + timedelta(seconds=10)):
                print("PARSED REQUEST RECEIVED AT: " + self.name + "\n" + str(request))
                update_log(text="PARSED REQUEST RECEIVED AT: " + self.name + "\n" + str(request))
                self.db.update_database(self.name, request)
                old_request = request
        return old_request

    def check_log_type(self):
        """
        This method will check in the first line of the log if it contains any of this specific words: CONNECT,
        OK LOGIN, OK UPLOAD, FAIL DOWNLOAD, OK DOWNLOAD. If any of this words is inside the log line so the log is NOT
        in xferlog standard mode. This method will return true if the log is in xferlog standard mode, false in any
        other case
        """
        line = self.file.readline()
        while line == "":
            time.sleep(3)
            line = self.file.readline()

        log_type = True
        if "CONNECT" in line or "OK LOGIN" in line or "OK UPLOAD" in line or "FAIL DOWNLOAD" in line or "OK DOWNLOAD" in line:
            log_type = False

        return log_type
