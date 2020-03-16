import os
import os.path
from reader_thread import Reader


def main():
    print("Script running and waiting for new entry")

    DIR = '/home/lorenzo/Desktop/vsftpd/'
    files = ([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

    threads = []

    for fileName in files:
        file = (open((DIR + str(fileName)), "r"))
        threads.append(Reader(fileName, file))

    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()
