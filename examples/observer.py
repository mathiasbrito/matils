import time
import random

from matils.patterns.observer import Observable, Observer


class SensorsReader(Observable):
    def read_sensors_data_loop(self):
        while True:
            # reads new sensors data each 2 seconds.
            temperature_data = self.get_temperature()
            self.notify(temperature_data, 'temperature')

            humidity_data = self.get_humidity()
            self.notify(humidity_data, 'humidity')
            time.sleep(2)

    def get_temperature(self):
        # return some Random Value between 0-40
        return {'value': random.uniform(0,40)}

    def get_humidity(self):
        # return a random value between 20-100
        return {'value': random.uniform(20,100)}


class SensorDataAnalizer(Observer):
    def update(self, sensor_data, event_name):
        print('Sensor data observerd, I will do some nice analysis from '
              'received data type: {}, data: {}'.format(event_name,
                                                        str(sensor_data)))


if __name__ == '__main__':
    sensors_reader = SensorsReader()
    sensors_analyzer = SensorDataAnalizer()

    sensors_reader.register(sensors_analyzer, 'temperature')
    sensors_reader.register(sensors_analyzer, 'humidity')

    sensors_reader.read_sensors_data_loop()
