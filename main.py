import os
import os.path
from reader_thread import Reader

DIR = '/home/lorenzo/Desktop/vsftpd/'


def create_thread(files):
    """
    Here the script will search and open all the files in the selected directory. Each file will be assigned to an array
    of thread ready to be executed.
    """
    threads = []
    for file_name in files:
        file = (open((DIR + str(file_name)), "r"))
        threads.append(Reader(file_name, file))
    return threads


def main():
    """
    Main function of the script, here is where the thread will be launch
    """
    print("Script running and waiting for new entry")

    files = ([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

    threads = create_thread(files)

    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()
