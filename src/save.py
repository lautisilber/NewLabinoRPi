from datetime import datetime
from typing import List, Optional
import os


def list_to_str(l: List) -> List:
    return [str(e) for e in l]


def save(fname: str, soil_hums: List[float], hum: float, temp: float, temps: Optional[List[float]]=None) -> bool:
    entry_elems = [datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), *soil_hums, hum, temp]
    if temps:
        entry_elems.extend(temps)
    entry_elems = list_to_str(entry_elems)
    write_mode = 'a' if os.path.isfile(fname) else 'w'
    if write_mode == 'w':
        header_elems = ['timestamp', *[f'soil_hum_{i}' for i in range(len(soil_hums))], 'dht_hum', 'dht_temp']
        if temps:
            header_elems.extend([f'ds18b20_temp_{i}' for i in range(len(temps))])
        header_elems = list_to_str(header_elems)
    
    try:
        with open(fname, write_mode) as f:
            if write_mode == 'w':
                f.write(','.join(header_elems) + '\n')
            f.write(','.join(entry_elems) + '\n')
        return True
    except Exception as err:
        print('Coudln\'t save readings')
        print(err)
        return False
            

