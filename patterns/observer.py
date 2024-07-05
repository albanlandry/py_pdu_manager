from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List

class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        raise NotImplementedError("Subclass must implement this method")

class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass

class DefaultSubject(Subject):
    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer) 

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

class PDUSubject(DefaultSubject):
    def __init__(self):
        pass

    def notify(self):
        pass

class PDUListener(Observer):
    """
    The Subject interface declares a set of methods for managing PDU subscribers.
    """
    @abstractmethod
    def onPduFound(self, sbj):
        raise NotImplementedError("Subclass must implement this method")
    

