import requests
from datetime import datetime

class TempDataPoint():

    def __init__(self, temp, sensor, unit='F', time=datetime.utcnow()):
        self.temp = temp
        self.unit = unit
        self.time = time
        self.sensor = sensor

    def verify_data(self):
        if not self.sensor:
            return False
        if not self.temp:
            return False
        if not self.time:
            return False
        return True

    def convert_datetime_to_string(self):
        # Round time to nearest second then convert to string
        self.time = datetime(self.time.year, 
                             self.time.month, 
                             self.time.day, 
                             self.time.hour, 
                             self.time.minute, 
                             self.time.second, 
                             tzinfo=self.time.tzinfo)
        return self.time.isoformat()

    def get_dict(self):
        return {"temperature": self.temp, 'timeRecorded': self.convert_datetime_to_string(), 'sensorName': self.sensor}

    def convert_to_c(self):
        if self.unit =="F":
            self.temp = (self.temp - 32) * (5/9)
            self.unit = "C"

    def convert_to_f(self):
        if self.unit == "C":
            self.temp = self.temp * 9/5 + 32
            self.unit = "F"

class TempComm():

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    def sendTemp(self, tempData):
        if not tempData.verify_data:
            return (False, "Unable to verify the data")
        
        try:
            response = requests.post(self.url, 
                                     data=tempData.get_dict(), 
                                     auth=requests.auth.HTTPBasicAuth(self.username, self.password), timeout=9.1)
        except requests.exceptions.RequestException as e:
            return (False, str(e))

        return (True, None)
