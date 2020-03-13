import os, os.path
import myThread


def main():
    print("Script running and waiting for new entry")

    DIR = '/home/lorenzo/Desktop/vsftpd/'
    files = ([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

    threads = []

    for fileName in files:
        file = (open((DIR + str(fileName)), "r"))
        threads.append(myThread.myThread(fileName, file))

    for thread in threads:
        thread.start()






if __name__ == "__main__":
    main()

    """
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
                if request.reqJson["filePath"] != oldRequest.reqJson["filePath"] or request.reqJson["date"] > (
                        oldRequest.reqJson["date"] + timedelta(seconds=10)):
                    fileLog.write(str(datetime.datetime.now()) + " PARSED REQUEST: -" + str(request) + "\n")
                    print("PARSED REQUEST: " + str(request))
                    updateDatabase(request)
                    oldRequest = request

    """
