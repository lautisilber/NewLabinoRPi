from datetime import datetime
from typing import List, Union
import os


def save(fname: str, soil_hums: List[float], hum: float, temp: float, temps: Union(List[float], None)=None) -> bool:
    entry_elems = [datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), *soil_hums, hum, temp]
    if temps:
        entry_elems.extend(temps)
    write_mode = 'a' if os.path.isfile(fname) else 'w'
    if write_mode == 'w':
        header_elems = ['timestamp', *[f'soil_hum_{i}' for i in range(len(soil_hums))], 'dht_hum', 'dht_temp']
        if temps:
            header_elems.extend([f'ds18b20_temp_{i}' for i in range(len(temps))])
    
    with open(fname, write_mode) as f:
        if write_mode == 'w':
            f.write(','.join(header_elems) + '\n')
        f.write(','.join(entry_elems) + '\n')
            

