"""A ZeroMQ Observer.

We understanding that this is basically a ZMQ Pub/Sub over the naming of an
Observer pattern. Despite we could call this as Publisher and Subscriber we
decided to keep Observer and Observable to shows the relation in functionality
to the Observer Pattern implemented in this library, an to highlight the
comparison between direct object communication and remote communication,
specially because ZMQ offers the 'inproc' and 'ipc' sockets, the first
to communication inside a process, and the second inter-process, allowing us
to fully rely on this implementation for in-process and inter-process
communication.
"""
import zmq
import zmq.asyncio

from typing import Any, List, Union
from abc import abstractmethod


class ZMQObserver:
    """
    A Observer that listen to events in a 0MQ socket.

    Since the registration to events (topic in Pub/Sub, filters in ZMQ) is 
    done to the ZMQ Socket, you need to inform the events to listen to at 
    creation time, or later by calling observe method.
    """

    def __init__(self, zmq_ep: str, events: Union[str, List[str]]='all',
                 zmq_context=None):
        """
        Initialize the 0MQ Observer and subscribe to desired events. 
        """
        self.zmq_ep = zmq_ep
        self.events = [''] if len(events) == 0 else events

        if zmq_context is None:
            self.zmq_context = zmq.asyncio.Context()
        else:
            self.zmq_context = zmq_context

        self.zmq_socket = self.zmq_context.socket(zmq.SUB)
        self.zmq_socket.connect(self.zmq_ep)

        self.observe(events)

    def observe(self, events: Union[str, List[str]]):
        if type(events) == str:
            events = [events]

        for event in events:
            if event != 'all':
                self.zmq_socket.subscribe(event.encode())
            else:
                self.zmq_socket.subscribe(b'')

    def stop_observing(self, events: Union[str, List[str]]):
        if type(events) == str:
            events = [events]

        for event in events:
            if event != 'all':
                self.zmq_socket.unsubscribe(event.encode())
            else:
                self.zmq_socket.unsubscribe(b'')

    async def listen(self):
        """Return messages arriving for the given event name."""
        while True:
            msg = await self.zmq_socket.recv_multipart()
            self.update(msg[1], msg[0])

    @abstractmethod
    def update(self, data: Any, event: str='all'):
        """Act on arrival of a message."""
        pass


class SensorsReader:
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

    async def notify(self, data, event):
        """Notify an observer by sending data via ZMQ."""
        await self.socket.send_multipart([event.encode(), str(data).encode()])
