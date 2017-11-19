"""A ZeroMQ Observer."""
import zmq
import asyncio

from abc import abstractmethod
from matils.patterns.observer import Observer


class ZMQObserver(Observer):
    """A Observer that listen to events in a 0MQ socket."""

    def __init__(self, zmq_ep: str, event: str='all', zmq_context=None):
        """Initialize the 0MQ Observer."""
        self.zmq_ep = zmq_ep
        self.event = '' if event == 'all' else event

        if zmq_context is None:
            self.zmq_context = zmq.Context()
        else:
            self.zmq_context = zmq_context

        self.zmq_socket = self.zmq_context.socket(zmq.SUB)
        self.zmq_socket.connect(self.zmq_ep)
        self.zmq_socket.subscribe(self.event.encode())

    async def listen(self):
        """Return messages arriving for the given envent name."""
        while True:
            try:
                msg = self.zmq_socket.recv_multipart(flags=zmq.NOBLOCK)
                print("Incomming Message...")
                self.update(msg, '')
            except zmq.Again:
                pass  # No messages ready
            await asyncio.sleep(0.01)
        self.zmq_socket.close()

    @abstractmethod
    def update(message):
        """Act on arrival of a message."""
        print(message)
