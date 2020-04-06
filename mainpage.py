##
# @mainpage
#
# LogViewer is a python script which is able to parse an ftp log extracting the useful information and uploading them to a common InfluxDB database.
#
# A vsftpd server will, by default, store its log in /var/log/vsftpd.log. This path can be edit in the vsftpd.conf file, in the same file can also be decided the log form.
# A log in FTP can be saved in a standard form or in xferlog standard form, there is not much difference in the reported data, the real difference is in the form in which they are shown.
#
# To explain how the script works is better to analyze it throw a few steps.
#
# **STEP ONE:**
#
# First thing the script does is search inside a specific directory all the log file that are stored. 
# This is done because may be more than one server running at the same time on the same hardware so having a shared directory for the log can help reduce waste. 
# Each file is then opened, and a dedicated thread object is created and started.
#
# **STEP TWO:**
#
# First thing the script does is search inside a specific directory all the log file that are stored. 
# This is done because may be more than one server running at the same time on the same hardware so having a shared directory for the log can help reduce waste. 
# Each file is then opened, and a dedicated thread object is created and started.
#
# **STEP THREE:**
#
# The pointer to the file is now moved at the end of the file and the thread enter in a while True loop where constantly check if new line have been added to the file. 
# If there isn’t any new entry the thread suspend itself for a couple of seconds.
#
# **STEP FOUR:**
#
# When a new line is found inside the log there is a first check to ensure it is a confirmed download operation and not an upload or login operation. 
# If the line respects this property, the script proceeds to parse the request with the purpose to isolate some crucial information. 
# To do that an object Request is created. This process will end with the creation of a JSON object.
#
# **STEP FIVE:**
#
# Now that the request has been parsed the new entry is entered in the influxDB database throw a simple INSERT query. The connection and writing method are managed by an opposite class.
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

