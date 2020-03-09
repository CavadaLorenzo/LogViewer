import Request
import time;
def main():
    print("Script running and waiting for new entry")
    file = open("/var/log/vsftpd.log", "r")

    f1 = file.readlines()

    while 1:
        where = file.tell()
        line = file.readline()
        if "OK DOWNLOAD" in line:
            request = Request.Request(line)
            print(request)
        if not line:
            time.sleep(1)
            file.seek(where)



if __name__ == "__main__":
    main()
