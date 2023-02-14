from abc import ABC, abstractmethod
from time import time


class DHTValues:
    def __init__(self, humidity: float, temperature: float) -> None:
        self.humidity = humidity
        self.temperature = temperature


class AbstractDHT(ABC):
    ACQUISITION_FERQUENCY = 2 # in seconds

    def __init__(self) -> None:
        self.last_time = 0
        self.humidity = 0
        self.temperature = 0

    @abstractmethod
    def _update_values(self) -> None:
        pass

    def get_values(self) -> DHTValues:
        if abs(time() - self.last_time) > AbstractDHT.ACQUISITION_FERQUENCY:
            self._update_values()
        return DHTValues(self.humidity, self.temperature)


class DHT(AbstractDHT):
    def _update_values(self) -> None:
        self.humidity = 11.1
        self.temperature = 22.2