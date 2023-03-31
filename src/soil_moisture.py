from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import List, Generator
from gpio import ADS1015Manager, GPIOAddressManager
from time import sleep


Callibration_T = Callable[[float], float]


ADS = ADS1015Manager(True)
ADDR = GPIOAddressManager()


class MultiplexedSensor:
    def __init__(self, callibration_func: Callibration_T, multiplexor_index: int) -> None:
        self.callibration_func = callibration_func
        self.multiplexor_index = multiplexor_index
    

def create_MultiplexedSensor_linear_callibration(multiplexor_index: int, m: float, b: float=0) -> MultiplexedSensor:
    callibration_func = lambda x: m * x + b
    return MultiplexedSensor(callibration_func, multiplexor_index)


def read_sensor(sensor: MultiplexedSensor, delay: float=0, ads: ADS1015Manager=ADS, addr: GPIOAddressManager=ADDR) -> float:
    addr.set_address(sensor.multiplexor_index)
    if delay:
        sleep(delay)
    return ads.read_first_voltage()
