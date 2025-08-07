from sense_hat import SenseHat
import datetime


class SensorReader:
    def __init__(self):
        self.sense = SenseHat()

    def get_temperature(self):
        return (self.sense.get_temperature() * 9.0 / 5.0) + 32  # Convert to Fahrenheit

    def get_humidity(self):
        return self.sense.get_humidity()

    def get_pressure(self):
        return self.sense.get_pressure()
    
    def get_all_data(self):
        return {
            'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'temperature': self.get_temperature(),
            'humidity': self.get_humidity(),
            'pressure': self.get_pressure()
        }