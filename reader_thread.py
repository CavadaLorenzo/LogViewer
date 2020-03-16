import threading
import time
from request import Request
from datetime import timedelta
from logger import update_log
from database import Database


class Reader(threading.Thread):

    def __init__(self, name, file):
        """
        This class will run the reading process from the log file.
        There are 3 attributes needed:
        -name: name of the vsftpd file log
        -file: file where the log are stored
        """
        threading.Thread.__init__(self)
        self.name = name
        self.file = file

    def run(self):
        """
        This method consist in a while True which will constantly check the log file to see if there is new entry.
        If not the thread will sleep for 3 seconds, although it will parse the request.
        Is possible that Kodi will do more than 1 request for the same file. To prevent that the script will save the
        same request more than once, the last request is saved and is compered with the new onw
        """
        print("Reading from: " + self.name)
        update_log(text="READING FROM FILE " + self.name + "\n")
        self.file.seek(0, 2)
        old_request = Request()
        while True:
            where = self.file.tell()
            line = self.file.readline()
            if not line:
                time.sleep(3)
                self.file.seek(where)
            else:
                old_request = self.parseNewLine(line, old_request)

    def parseNewLine(self, line, old_request):
        """
        This method will parse the request, create an object Request and add the new request to the database if is a new
        one.
        """
        line = line.split(" ")
        if line[len(line) - 1] == "c\n":
            request = Request(line)
            if request.req_json["filePath"] != old_request.reqJson["filePath"] or request.req_json["date"] > (
                    old_request.reqJson["date"] + timedelta(seconds=10)):
                print("PARSED REQUEST RECEIVED AT: " + self.name + "\n" + str(request))
                update_log(text="PARSED REQUEST RECEIVED AT: " + self.name + "\n" + str(request))
                Database.update_database(request)
                old_request = request
        return old_request
