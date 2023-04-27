from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import List, Generator, Optional
from gpio import ADS1015Manager, GPIOAddressManager
from time import sleep
from statistics import mean


Callibration_T = Callable[[float], float]



class MultiplexedSensor:
    def __init__(self, callibration_func: Callibration_T, multiplexor_index: int, multiplexor_number: int, ads_channel: Optional[int]=None) -> None:
        self.callibration_func = callibration_func
        self.multiplexor_index = multiplexor_index
        self.multiplexor_number = multiplexor_number
        self.ads_channel = self.multiplexor_number if ads_channel is None else multiplexor_number
    

def create_MultiplexedSensor_linear_callibration(multiplexor_index: int, multiplexor_number: int, ads_channel: Optional[int]=None, m: float=1, b: float=0) -> MultiplexedSensor:
    callibration_func = lambda x: m * x + b
    return MultiplexedSensor(callibration_func, multiplexor_index, multiplexor_number, ads_channel)


def read_sensor(sensor: MultiplexedSensor, ads: ADS1015Manager, ads_channel: int, addr: GPIOAddressManager, delay: float=0.1) -> float:
    addr.set_address(sensor.multiplexor_index)
    if delay:
        sleep(delay)
    vals = []
    for i in range(50):
        sleep(1)
        vals.append(ads.read_channel(ads_channel))
    return mean(vals)

def read_all_sensors(sensors: List[MultiplexedSensor], ads: ADS1015Manager, addrs: List[GPIOAddressManager], delay: float=0.1) -> Generator[float, None, None]:
    for sensor in sensors:
        mult = sensor.multiplexor_number
        channel = sensor.ads_channel
        yield read_sensor(sensor, ads, channel, addrs[mult], delay)

if __name__ == '__main__':
    ADS = ADS1015Manager()
    ADS.add_single_channel_P0()
    ADS.add_single_channel_P1()
    ADDR1 = GPIOAddressManager([17, 27, 22])
    ADDR2 = GPIOAddressManager([18, 23, 24])
    #sensors = [create_MultiplexedSensor_linear_callibration(i, 0) for i in range(8)]
    #sensors.extend([create_MultiplexedSensor_linear_callibration(i, 1) for i in range(0, 8)])
    sensors = [create_MultiplexedSensor_linear_callibration(i, 0) for i in [0, 4, 5, 6]]
    for i in read_all_sensors(sensors, ADS, [ADDR1, ADDR2]):
        print(i)