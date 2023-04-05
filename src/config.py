from dataclasses import dataclass, asdict
from typing import List, Tuple
import pickle

@dataclass
class Config:
    soil_moisture_sensors: List[Tuple[int, int, int]] # [*[multiplexer_index, calibration_incline (m), calibration_offset (b)]]
    dht_pin: int

    dict = asdict


CONFIG_FILE = 'config.yaml'

def save_config(config: Config, config_file: str=CONFIG_FILE) -> bool:
    pass

def load_config(config_file: str=CONFIG_FILE) -> Config:
    pass

