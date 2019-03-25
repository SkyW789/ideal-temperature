import requests
from datetime import datetime
import pytz
from abc import ABC, abstractmethod

class GenericDataPoint(ABC):
    
    @abstractmethod
    def verify_data(self):
        pass

    @abstractmethod
    def get_dict(self):
        pass

    def convert_datetime_to_string(self, time):
        # Round time to nearest second then convert to string
        time_rounded_sec = datetime(time.year, 
                             time.month, 
                             time.day, 
                             time.hour, 
                             time.minute, 
                             time.second, 
                             tzinfo=time.tzinfo)
        return time_rounded_sec.isoformat()

class TempDataPoint(GenericDataPoint):

    def __init__(self, temp, sensor, unit='F', time=None):
        self.temp = temp
        self.unit = unit
        self.sensor = sensor
        if time:
            self.time = time
        else:
            self.time = datetime.now(tz=pytz.utc)

    def verify_data(self):
        if not self.sensor:
            return False
        if not self.temp:
            return False
        if not self.time:
            return False
        return True

    def get_dict(self):
        return {"temperature": self.temp, 'timeRecorded': self.convert_datetime_to_string(self.time), 'sensorName': self.sensor}

    def convert_to_c(self):
        if self.unit =="F":
            self.temp = (self.temp - 32) * (5/9)
            self.unit = "C"

    def convert_to_f(self):
        if self.unit == "C":
            self.temp = self.temp * 9/5 + 32
            self.unit = "F"

class DoorDataPoint(GenericDataPoint):

    def __init__(self, state, time=None):
        self.state = state
        if time:
            self.time = time
        else:
            self.time = datetime.now(tz=pytz.utc)

    def verify_data(self):
        if not self.state:
            return False
        if not self.time:
            return False
        return True

    def get_dict(self):
        return {"state": self.state, "time": self.convert_datetime_to_string(self.time)}

class Comm():

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    def send(self, data):
        if not data.verify_data:
            return (False, "Unable to verify the data")
        
        try:
            response = requests.post(self.url, 
                                     data=data.get_dict(), 
                                     auth=requests.auth.HTTPBasicAuth(self.username, self.password), timeout=9.1)
        except requests.exceptions.RequestException as e:
            return (False, str(e))

        return (True, None)

