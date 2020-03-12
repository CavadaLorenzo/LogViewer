# LogViewer

###V1.0
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
