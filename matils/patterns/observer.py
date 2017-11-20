"""
Implementation of the Observer Pattern.

In this module you will find the necessary classes to use the Observer Pattern.
It provides both the Observer and Observable classes that you must use to
derive your classes.

This Implementation allows you to observe general events occurred in a object
that extends the :class:`Observable` class. To do that you need to implement
the interface :class:`Observer` in your class and register it against the
Observable that you want to track. Below an usage example, let's say that we
have an Observable reading values from sensors, and notify observers for new
values, the Observable code is shown below:

.. code-block:: python

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

We want them to have an observer that will take action everytime a new reading
is done in the sensors. For that we implement the following observer:

.. code-block:: python

    class SensorDataAnalyzer(Observer):
        def update(self, sensor_data, event_name):
            print('Sensor data observed, I will do some nice analysis from '
                  'received data type: {}, data: {}'.format(event_name,
                                                            str(sensor_data)))

In our main code we have:

.. code-block:: python

    if __name__ == '__main__':
        sensors_reader = SensorsReader()
        sensors_analyzer = SensorDataAnalyzer()

        sensors_reader.register(sensors_analyzer, 'temperature')
        sensors_reader.register(sensors_analyzer, 'humidity')

        sensors_reader.read_sensors_data_loop()


After you implement your observer you can register it in Observables, let's
take the following :class:`Observable`
"""

from typing import Union, Dict, List, Any
from abc import ABC, abstractmethod


class Observer(ABC):
    """
    Intended to be implemented if the objects are wiling to observe.

    If your class wants to observe an :class:`Observable`, needs to implement
    this abstract class.

    Observers can register multiple times, in different Observables if they
    want to do so. However, only the method update will be called, the logic
    to be executed based on the event needs to be handled inside the update
    method.

    .. IMPORTANT::
        Check the implementation of your Observable to understand what kind of
        data it is send on each notification. An notification can send any type
        of data.
    """

    @abstractmethod
    def update(self, data: Any, event: str):
        """To be called by an :class:`Observable` to notified the Observer."""
        pass


class Observable:
    """
    The changes in a Observable object can be observed by Observer classes.

    The Observable manages a list of observers and have to make sure that all
    registered observers will be notified when the status of one of the
    observed attributes change.

    One characteristic of this implementation is that Observers need to inform
    what they want to observe. The Observers optionally can inform the type of
    messages as a list of string so that its callback will be called only when
    the specific event occurs.

    If an observer registers to observer a message unknown by the Observable no
    error will be generated, the observer will simply not receive
    notifications.
    """

    def __init__(self):
        """Initialize the Observers list."""
        self._observers: Dict[str, List[Observer]] = dict()
        """
        This attributes keeps a dictionary containing Observable events and the
        associated callbacks. Observers registered without specifying a
        event name are associated to the key "all" in the dictionary.

        As an example, in a given point in time the self.observers property
        can be like the following:

        .. code-block:: python
            self.observers = {
                "all": [observer1, observer2],
                "state": [observer3]
            }
        """

        self._observers['all'] = list()  # initializes the global event list

    @property
    def observers(self) -> Dict[str, List[Observer]]:
        """:attr:Observable._observers getter."""
        return self._observers

    def register(self, observer: Observer, to: Union[str, List[str]]="all"):
        """
        Register an observer to listen to events from this Observable.

        This function manipulates the attribute :attr:`Observer._observers by
        adding the 'observer' to the list in the right entry taking into
        consideration the events of interest. If 'all' is given to the
        parameter 'event', than the observer MUST be inserted in the 'all'
        entry of :attr:`Observer._observers`.

        The method can receive the events of interest as s string,
        for a single event or a list of strings for register multiple events
        in the same call.

        If an observer is already registered to observe to all events, if a
        request to observe an specific event arrive, the request will be
        ignored and the request will be considered successful.
        """
        if type(to) == str:
            events = [to]
        else:
            events = to

        for event in events:
            try:
                if observer not in self._observers[event] or \
                   observer not in self._observers['all']:
                    self._observers[event].append(observer)
            except KeyError:
                observers = [observer]
                self._observers[event] = observers

    def unregister(self,
                   observer: Observer,
                   from_events: Union[str, List[str]]="all"):
        """
        Unregister an observer, to all or specific events.

        This method will unregister an observer, the default behavior is to
        unregister from all events. If an event name or a list of events is
        given it will be unregistered only from the/those specified event(s).

        The unregistered process is done by manipulating the
        :attr:`Onservable.observers` removing the entries to the given
        observer from the different events lists.
        """
        if type(from_events) == str:
            events = [from_events]
        else:
            events = from_events

        for event in events:
            if event == 'all':
                # Now we need to find every reference to the observer
                for registered_event, observers in self._observers.items():
                    if observer in observers:
                        observers.remove(observer)
            else:
                try:
                    if observer in self._observers[event]:
                        self._observers[event].remove(observer)
                    else:
                        continue  # Element Not Found...
                except KeyError:
                    continue  # Event not found...

    def reset(self):
        """
        Remove all registered observers.

        Clean :attr:`Observable.observers`. This means that the attribute
        after a reset, must be exactly as it was when the obect was created.

        The reference to the original dictionary object is kept and the 'all'
        entry are kept...
        """
        self._observers.clear()
        self._observers['all'] = list()

    def notify(self, data: Any, event: str):
        """
        Notify observers registered to be update about the event.

        All the observers registered to get all events must be notified.

        .. IMPORTANT::
            Be sure to document the types returned by each event, so that the
            Observers can implement correctly their update functions. To
            maintain the flexibility we decided to allow the Observable to send
            any kind of object.

        .. CAUTION::
            This method do not check if an observer is registered at all and
            other event in the same :class:=`Observable`, if you do so in your
            code you will get notified more than once!
        """
        for observer in self._observers['all']:
            observer.update(data, event)

        if event in self._observers.keys():
            for observer in self._observers[event]:
                observer.update(data, event)
        else:
            pass  # nobody registered...
