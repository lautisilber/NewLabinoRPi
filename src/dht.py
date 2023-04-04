import Adafruit_DHT as dht
from time import time


class DHT:
    ACQUISITION_FERQUENCY = 2 # in seconds

    def __init__(self, pin: int) -> None:
        self.pin = pin
        self._last_time = 0
        self._humidity = 0
        self._temperature = 0
    
    def update_values(self) -> None:
        if abs(time() - self._last_time) > DHT.ACQUISITION_FERQUENCY:
            h, t = dht.read_retry(dht.DHT11, self.pin)
            self._last_time = time()
            if h: self._humidity = h
            if t: self._temperature = t
    
    @property
    def humidity(self) -> float:
        return self._humidity
    
    @property
    def temperature(self) -> float:
        return self._temperature