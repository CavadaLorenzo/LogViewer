# LogViewer

### v1.0
Simply python script which read in real time a vsftpd log (default position */var/log/vsftpd.log*).

A vsftpd log line has this format

Tue Mar 10 15:25:21 2020 [pid 3595] [lorenzo] OK DOWNLOAD: Client "::ffff:10.3.10.155", "/media/Zombieland Doppio colpo 2019 BluRay 1080xH264 Ita Eng Ac3 5.1 Sub Ita Eng/Zombieland Doppio colpo 2019 BluRay 1080xH264 Ita Eng Ac3 5.1 Sub Ita Eng.mkv", 131072 bytes, 74159.91Kbyte/sec

This script will create from a log line like that a json like this:
{
    "date": "2020-03-11 15:27:02",
    "filePath": "/music/Download/Marshmello  Anne-Marie - FRIENDS (Lyric Video).mp3",
    "hostIp": "::ffff:10.3.10.155"
}

This json will be uploaded in an influxDB measurement called request.


### v1.1
Now the script is able to parse vsftpd log written in standard ftpd xferlog format. The default location is also changed. Now is in /home/USER/Desktop/vsftpd/vsftpd.log


### v2.0
Now the script can read form N files stored in the same directory. It will create a thread for each file for real-time reading


### v3.0
Now the script can read from N file, for each file it will detect if it is written in default mode or in xferlog standard mode. Now the script will also keep track of the username of the client who has done the request.

### ATTENTION:
This is an old version of Logviewer, a more update veersion can be found here: https://github.com/CavadaLorenzo/FTP-Server_docker


