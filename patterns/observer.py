"""
Implementation of the Observer Pattern.

In this module you will find the necessary classes to use the Observer Pattern.
It provides both the Observer and Observable classes that you must use to
derive your classes.
"""

from typing import Dict, List, Callable, Any
from abc import ABC, abstractmethod


class Observer(ABC):
    """
    Intended to be implemented if the objects are whiling to observe.

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
    def update(data: Any, event: str="all"):
        """To be called by an Observable if object is registered."""
        pass


class Observable:
    """
    The changes in a Observable object can be observed by Observer classes.

    The Observable manages a list of observers and have to make sure that all
    registered observers will be notifyed when the status of one of the
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
        self.observers: Dict[str, List[Callable[[str, Dict], None]]] = dict()
        """
        This attributes keeps a dictionary containing Observable events and the
        assciated callbacks. Observers registered without specifying a
        event name are associated to the key "all" in the dictionary.

        As an example, in a given point in time the self.observers property
        can be like the following:

        .. code:: python
            self.observers = {
                "all": [observer1, observer2],
                "state": [observer3]
            }
        """

        self.observers['all'] = list()  # initializes the global event list

    def register(self, observer: Observer, event: str="all"):
        """
        Register an observer to listen to events from this Observable.

        This function manipulates the attribute self.obseervers by addying the
        'observer' to the list in the right entry taking into consideration
        the event of interest. If 'all' is given to the parameter 'event', than
        the observer MUST be inserted in the 'all' entry of self.observers.

        If an observer is already registered to observe to all events, if a
        request to observe an specific event arrive, the request will be
        ignored and the request will be considered successful.
        """
        try:
            if observer not in self.observers[event] or \
               observer not in self.observers['all']:
                self.observers[event].append(observer)
        except KeyError:
            observers = [observer]
            self.observers[event] = observers

    def unregister(self, observer: Observer, event: str="all"):
        """
        Unregister an observer, to all or specifc events.

        This method will unregister an observer, the default behavior is to
        unregister from all events. If a event name is given it will be
        unregistered only from the specified event.

        The unregistering process is done by manipulting the 'self.observers'
        removing the entries to the given observer from the different events
        lists.

        :return: True if the unregistration was successful, and False if the
                 unregistration failed, or no action was taken (maybe observer
                 not registered).
        """
        if event == 'all':
            # Now we need to find every reference to the observer
            found = False
            for event, observers in self.observers.items():
                if observer in observers:
                    observers.remove(observer)
                    found = True
            if found:
                return True
            else:
                return False
        else:
            try:
                if observer in self.observers[event]:
                    self.observers[event].remove(observer)
                    return True
                else:
                    return False  # Element Not Found...
            except KeyError:
                return False  # Event not found...

    def reset(self):
        """
        Remove all registered observers.

        Clean :attr:`Observable.observers`. This means that the attribute
        after a reset, must be exactly as it was when the obect was created.

        The reference to the original dictionary object is kept and the 'all'
        entry are kept...
        """
        self.observers.clear()
        self.observers['all'] = list()

    def notify(self, data: Any, event: str):
        """
        Notify observers registered to be update about the event.

        All the observers registered to get all events must be notified.

        .. IMPORTANT::
        Be sure to document the types returned by each event, so that the
        Observers can implement correctly their update functions. To maintain
        the flexibility we decided to allow the Observable to send any kind
        of object.

        .. CAUTION::
        This method do not check if an observer is registered at all and other
        event in the same :class:=`Observable`, if you do so in your code you
        will get notified more than once!
        """
        for observer in self.observers['all']:
            observer.update(data, event)

        if event in self.observers.keys():
            for observer in self.observers[event]:
                observer.update(data, event)
        else:
            pass  # nobody registered...
