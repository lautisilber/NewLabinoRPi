from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import List, Generator
from gpio import ADS1015Manager, GPIOAddressManager


Callibration_T = Callable[[float], float]


class AbstractMultiplexedSensor:
    def __init__(self, callibration_func: Callibration_T, multiplexor_index: int) -> None:
        self.callibration_func = callibration_func
        self.multiplexor_index = multiplexor_index
    

def create_AbstractMultiplexedSensor_linear_callibration(multiplexor_index: int, m: float, b: float=0) -> AbstractMultiplexedSensor:
    callibration_func = lambda x: m * x + b
    return AbstractMultiplexedSensor(callibration_func, multiplexor_index)


class SensorGenYield:
    def __init__(self, index: int, value: float) -> None:
        self.index = index
        self.value = value


class AbstractMultiplexorSensorsManager(ABC):
    def __init__(self, sensor_list: List[AbstractMultiplexedSensor]=list()) -> None:
        if not all(isinstance(e, AbstractMultiplexedSensor) for e in sensor_list):
            raise TypeError("Tried to create MultiplexorSensorsManager object with a list that is not entirely comprised of MultiplexedAnalogSensor objects")
        self.sensors = { s.multiplexor_index:s for s in sensor_list }
    
    @abstractmethod
    def _adc_get_func(self) -> float:
        pass

    @abstractmethod
    def _multiplexor_index_change_func(self, index: int) -> None:
        pass

    def _check_index(self, index: int) -> bool:
        return index in self.sensors.keys()
    
    def get_value(self, index: int) -> float:
        if not self._check_index(index):
            raise IndexError(f"Multiplexor index is out of range. Sensor list has length of {len(self.sensor_list)} and the index provided was {index}")
        self.multiplexor_index_change_func(index)
        raw = self.adc_get_func()
        value = self.sensors[index].callibration_func(raw)
        return value
    
    def get_all_values(self) -> Generator[SensorGenYield, None, None]: # Generator[YieldType, SendType, ReturnType]
        for index in self.sensors:
            yield SensorGenYield(index, self.get_value(index))


class MultiplexorSensorsManager(AbstractMultiplexorSensorsManager):
    def __init__(self, sensor_list: List[AbstractMultiplexedSensor], addr_pins_list: List[int]) -> None:
        super().__init__(sensor_list)
        self.ads = ADS1015Manager()
        self.multiplexor = GPIOAddressManager(addr_pins_list)

        self.ads.add_single_channel_P0()

    @staticmethod
    def _adc_get_func(self) -> float:
        return self.ads.read_first_voltage()
    
    @staticmethod
    def _multiplexor_index_change_func(self, index: int) -> None:
        self.multiplexor.set_address(index)