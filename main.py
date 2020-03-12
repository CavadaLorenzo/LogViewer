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
    file = open("/var/log/vsftpd.log", "r")
    fileLog = open("/home/lorenzo/PycharmProjects/LogViewer/LogViewer.log", "a")
    fileLog.write("\n" + str(datetime.date.today()) + " - Starting the script\n")
    f1 = file.readlines()
    oldRequest = Request.Request()
    while 1:
        where = file.tell()
        line = file.readline()
        if "OK DOWNLOAD" in line:
            fileLog.write(str(datetime.datetime.now()) + " RECEIVED REQUEST: -" + line + "\n")
            request = Request.Request(line)
            if request.reqJson["filePath"] != oldRequest.reqJson["filePath"] or request.reqJson["date"] > (oldRequest.reqJson["date"] + timedelta(seconds=10)):
                fileLog.write(str(datetime.datetime.now()) + " PARSED REQUEST: -" + str(request) + "\n")
                print("PARSED REQUEST: " + str(request))
                updateDatabase(request)
                oldRequest = request
        if not line:
            time.sleep(5)
            file.seek(where)



if __name__ == "__main__":
    main()