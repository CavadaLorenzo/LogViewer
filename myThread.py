import threading
import time
from influxdb import InfluxDBClient
import Request
from datetime import timedelta


class myThread(threading.Thread):

    def __init__(self, name, file):
        threading.Thread.__init__(self)
        self.name = name
        self.file = file

    def run(self):
        fileLog = open("./LogViewer.log", "a")
        print("Reading from: " + self.name)
        fileLog.write("READING FROM FILE " + self.name + "\n")
        self.file.seek(0, 2)
        oldRequest = Request.Request()
        while True:
            where = self.file.tell()
            line = self.file.readline()
            if not line:
                time.sleep(2)
                self.file.seek(where)
            else:
                line = line.split(" ")
                if line[len(line) - 1] == "c\n":
                    request = Request.Request(line)
                    if request.reqJson["filePath"] != oldRequest.reqJson["filePath"] or request.reqJson["date"] > (
                            oldRequest.reqJson["date"] + timedelta(seconds=10)):
                        print("PARSED REQUEST RECEIVED AT: " + self.name + "\n" + str(request))
                        fileLog.write("PARSED REQUEST RECEIVED AT: " + self.name + "\n" + str(request))
                        updateDatabase(request, self.name)
                        oldRequest = request


def updateDatabase(req, name):
    client = InfluxDBClient(host='localhost', port='8086')
    client.switch_database('firstDB')
    query = "request hostIp=\"" + req.reqJson["hostIp"] + "\",filePath=\"" + req.reqJson[
        "filePath"] + "\",logName=\"" + name + "\""
    client.write([query], {'db': "firstDB"}, 204, 'line')
