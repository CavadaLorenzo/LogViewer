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
