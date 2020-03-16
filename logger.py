
def update_log(text):
    """
    this method is just to keep update a log file where all the accepted requests are stored
    """
    file = open("./LogViewer.log", "a")
    file.write(text)
