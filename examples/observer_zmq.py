"""An example of the Observer pattern with ZeroMQ."""

import zmq
import random
import asyncio

from matils.patterns.zmq_observer import ZMQObserver
from matils.patterns.observer import Observable


class SensorsReader(Observable):
    """Simulate a sensor reader."""

    def __init__(self, zmq_ep, zmq_context=None):
        """Initilize the observer with ZMQ related variables."""
        if zmq_context is None:
            self.zmq_context = zmq.Context()
        else:
            self.zmq_context = zmq_context

        self.socket = self.zmq_context.socket(zmq.PUB)
        self.socket.bind(zmq_ep)

    async def read_sensors_data_loop(self):
        """Generate random values for sensors and propagates the data."""
        while True:
            # reads new sensors data each 2 seconds.
            temperature_data = self.get_temperature()
            self.socket.send_multipart([b'temperature', str(temperature_data)
                                        .encode()])

            humidity_data = self.get_humidity()
            self.socket.send_multipart([b'humidity', str(humidity_data)
                                        .encode()])
            print("Sent")
            await asyncio.sleep(1)

    def get_temperature(self):
        """Generate a radom value for temperature."""
        # return some Random Value between 0-40
        return {'value': random.uniform(0, 40)}

    def get_humidity(self):
        """Generate a random value for humidity."""
        # return a random value between 20-100
        return {'value': random.uniform(20, 100)}

    def notify():
        """Overwrite notify to send data via ZMQ."""
        pass


class SensorDataAnalizer(ZMQObserver):
    """A Dummy sensor analyzer."""

    def update(self, sensor_data, event_name):
        """Execute upon new data."""
        print('Sensor data observerd, I will do some nice analysis from '
              'received data type: {}, data: {}'.format(event_name,
                                                        str(sensor_data)))


if __name__ == '__main__':
    endpoint = "inproc://test"
    sensors_reader = SensorsReader(endpoint)
    sensors_analyzer = SensorDataAnalizer(endpoint, 'temperature',
                                          zmq_context=sensors_reader.
                                          zmq_context)

    try:
        event_loop = asyncio.get_event_loop()
        tasks = asyncio.gather(sensors_reader.read_sensors_data_loop(),
                               sensors_analyzer.listen())
        event_loop.run_until_complete(tasks)
    except KeyboardInterrupt:
        event_loop.close()
