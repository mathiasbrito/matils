"""An example of the Observer pattern with ZeroMQ."""

import zmq
import random
import asyncio
import zmq.asyncio

from typing import Any

from matils.patterns.zmq_observer import ZMQObserver
from matils.patterns.observer import Observable


class SensorsReader(Observable):
    """Simulate a sensor reader."""

    def __init__(self, zmq_ep, zmq_context=None):
        """Initialize the observer with ZMQ related variables."""
        super().__init__()

        if zmq_context is None:
            self.zmq_context = zmq.asyncio.Context()
        else:
            self.zmq_context = zmq_context

        self.socket = self.zmq_context.socket(zmq.PUB)
        self.socket.bind(zmq_ep)

    async def read_sensors_data_loop(self):
        """Generate random values for sensors and propagates the data."""
        while True:
            # reads new sensors data each 2 seconds.
            temperature_data = self.get_temperature()
            await self.notify(temperature_data, 'sensors.temperature')

            humidity_data = self.get_humidity()
            await self.notify(humidity_data, 'sensors.humidity')

            await asyncio.sleep(1)

    @staticmethod
    def get_temperature():
        """Generate a random value for temperature."""
        # return some Random Value between 0-40
        return {'value': random.uniform(0, 40)}

    @staticmethod
    def get_humidity():
        """Generate a random value for humidity."""
        # return a random value between 20-100
        return {'value': random.uniform(20, 100)}

    async def notify(self, data, event):
        """Overwrite notify to send data via ZMQ."""
        await self.socket.send_multipart([event.encode(), str(data).encode()])


class SensorDataAnalyzer(ZMQObserver):
    """A Dummy sensor analyzer."""

    def update(self, data: Any, event: str="all"):
        """Execute upon new data."""
        print('Sensor data observed, I will do some nice analysis from '
              'received data type: {}, data: {}'.format(event, data))


if __name__ == '__main__':
    endpoint = "tcp://127.0.0.1:5555"
    sensors_reader = SensorsReader(endpoint)
    sensors_analyzer = SensorDataAnalyzer(endpoint, ['sensors.temperature',
                                                     'sensors.humidity'],
                                          zmq_context=sensors_reader.
                                          zmq_context)

    event_loop = asyncio.get_event_loop()
    tasks = asyncio.gather(sensors_reader.read_sensors_data_loop(),
                           sensors_analyzer.listen())
    try:
        event_loop.run_until_complete(tasks)
    except KeyboardInterrupt:
        event_loop.close()
