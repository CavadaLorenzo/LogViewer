from influxdb import InfluxDBClient


class Database:

    def update_database(self, req):
        """
        This method will store the request into a InfluxDB database.
        The entry will have this format:
        time   hostIp   filePath   logName
        """
        client = InfluxDBClient(host='localhost', port='8086')
        client.switch_database('firstDB')
        query = "request hostIp=\"" + req.req_json["hostIp"] + "\",filePath=\"" + req.req_json[
            "filePath"] + "\",logName=\"" + self.name + "\""
        client.write([query], {'db': "firstDB"}, 204, 'line')
