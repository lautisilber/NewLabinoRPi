from typing import Optional, List, Tuple
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import DigitalOutputDevice as OutPin
from math import log2, ceil


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

ads.gain = 2 / 3 # 1 2 4 8 16

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)


class ADS1015Manager(ADS.ADS1015):
    def __init__(self) -> None:
        i2c = busio.I2C(board.SCL, board.SDA)
        super().__init__(i2c)
        self.channels: List[AnalogIn] = []
    
    def gain_info(self) -> None:
        print(f'Possible gains: {self.gains}')

    def add_channel(self, positive_pin: int, negative_pin: Optional[int]=None) -> int:
        self.channels.append(AnalogIn(self, positive_pin, negative_pin))
        return len(self.channels) - 1
    
    def add_single_channel_P0(self) -> int:
        return self.add_channel(ADS.P0)
    
    def add_single_channel_P1(self) -> int:
        return self.add_channel(ADS.P1)
    
    def add_single_channel_P2(self) -> int:
        return self.add_channel(ADS.P2)

    def add_single_channel_P3(self) -> int:
        return self.add_channel(ADS.P3)
    
    def add_differential_channel_P0_P1(self) -> int:
        return self.add_channel(ADS.P0, ADS.P1)
    
    def read_first_voltage(self) -> float:
        if not self.channels:
            raise Exception('No channels were set up')
        if len(self.channels) > 1:
            print('Warning. Many channels were set up. reading from the first one...')
        return self.channels[0].voltage
    
    def read_channel(self, index: int) -> float:
        if not self.channels:
            raise Exception('No channels were set up')
        if index < 0 or index >= len(self.channels):
            raise Exception(f'Tried to read channel {index} when only {len(self.channels)} exist')
        return self.channels[index].voltage
    
    def add_first_single(self) -> None:
        self.add_single_channel_P0()
    
    def add_all_single(self) -> None:
        self.add_single_channel_P0()
        self.add_single_channel_P1()
        self.add_single_channel_P2()
        self.add_single_channel_P3()



def _get_binary_size(nr: int) -> int:
    # get max number of binary digits
    return ceil(log2(nr+1))


class GPIOAddressManager:
    def __init__(self, pins: Optional[List[int]]=None) -> None:
        self.pins = []
        self.max_addr = 0

        if pins:
            self.set_pins(pins)

    def set_pins(self, pins: List[int]) -> None:
        self.pins = tuple(OutPin(pin) for pin in pins)
        self.max_addr = 2**len(self.pins) - 1
    
    def set_address(self, addr: int) -> None:
        if 0 > addr or addr > self.max_addr:
            raise Exception(f'Out of bounds address. Max addr = {self.max_addr}. Provided addr = {addr}')
        
        states = [state == '1' for state in format(addr, f'{len(self.pins)}b')]
        for i, state in enumerate(states):
            self.pins[i].value = state
