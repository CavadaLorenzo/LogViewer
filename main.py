##
# @file
# The main class. Here is where the script will start
# First of all the script will search in a specific directory all the
# log file. For each log file it will create a thread for the reading and parsing part.
#
# Constant:
# DIR: indicates the path where the log are stored
#

import os
import os.path

from reader_thread import Reader

DIR = '/home/lorenzo/Desktop/vsftpd/'


def create_thread():
    """
    This method will create and return an array of thread. Each thread regards a specific
    log file, the thread will read from the file in real time.
    Each file is identified by its name and the file itself.
    """
    threads = []

    control = True
    while control:
        files = ([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        for file_name in files:
            if file_name == "vsftpd.log":
                file = (open((DIR + str(file_name)), "r"))
                threads.append(Reader(file_name, file))
                control = False

    return threads

def main():
    """
    Main function of the script, here is where the thread will be launch.
    """
    print("Script running and waiting for new entry")

    threads = create_thread()

    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()
