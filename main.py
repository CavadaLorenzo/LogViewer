import Request
import time
import datetime
from datetime import timedelta
from influxdb import InfluxDBClient

def updateDatabase(req):
    client = InfluxDBClient(host='localhost', port='8086')
    client.switch_database('firstDB')
    query = "request hostIp=\"" + req.reqJson["hostIp"] + "\",filePath=\"" + req.reqJson["filePath"] + "\""
    client.write([query], {'db': "firstDB"}, 204, 'line')


def main():
    print("Script running and waiting for new entry")
    file = open("/home/lorenzo/Desktop/vsftpd/vsftpd.log", "r")
    fileLog = open("/home/lorenzo/PycharmProjects/LogViewer/LogViewer.log", "a")
    fileLog.write("\n" + str(datetime.date.today()) + " - Starting the script\n")

    oldRequest = Request.Request()
    file.seek(0,2)
    while 1:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            fileLog.write(str(datetime.datetime.now()) + " RECEIVED REQUEST: -" + line + "\n")
            line = line.split(" ")
            if "c" == str(line[len(line) - 1]) or line[len(line) - 1] == "c\n":
                request = Request.Request(line)
                if request.reqJson["filePath"] != oldRequest.reqJson["filePath"] or request.reqJson["date"] > (oldRequest.reqJson["date"] + timedelta(seconds=10)):
                    fileLog.write(str(datetime.datetime.now()) + " PARSED REQUEST: -" + str(request) + "\n")
                    print("PARSED REQUEST: " + str(request))
                    updateDatabase(request)
                    oldRequest = request


if __name__ == "__main__":
    main()