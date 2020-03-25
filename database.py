from influxdb import InfluxDBClient


class Database:

    def __init__(self):
        """
        Create an object Database which connect to the default database: firstDB
        """
        self.db = InfluxDBClient(host='localhost', port='8086')
        self.db.switch_database('firstDB')

    def update_database(self, name, req):
        """
        This method will store the request into a InfluxDB database.
        The entry will have this format:
        time   hostIp   filePath   logName
        """
        query = "request host_ip=\"" + req.req_json["host_ip"] + "\",file_path=\"" + req.req_json[
            "file_path"] + "\",log_name=\"" + name + "\"" + ",username=\"" + req.req_json["username"] + "\""

        self.db.write([query], {'db': "firstDB"}, 204, 'line')
