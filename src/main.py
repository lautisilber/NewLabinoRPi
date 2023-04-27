from soil_moisture import create_MultiplexedSensor_linear_callibration, read_all_sensors
#from dht import DHT
from webserver import create_web_server
from gpio import ADS1015Manager, GPIOAddressManager
from save import save
from time import sleep
from timer import RepeatedTimer
#from dropbox import dropbox_upload_file

import os

os.chdir('/home/labestomas/NewLabinoRPi')

fname = 'save.txt'
ADS = ADS1015Manager()
ADS.add_single_channel_P0()
ADS.add_single_channel_P1()
ADDR1 = GPIOAddressManager([17, 27, 22])
ADDR2 = GPIOAddressManager([18, 23, 24])
ADDRS = [ADDR1, ADDR2]
sensors = [create_MultiplexedSensor_linear_callibration(i, 0) for i in range(8)]
sensors.extend([create_MultiplexedSensor_linear_callibration(i, 1) for i in range(0, 8)])


def measure():
    print('tick')

    soil_hum_readings = list(read_all_sensors(sensors, ADS, ADDRS))
    
    #dht.update_values()
    hum = 0#dht.humidity
    temp = 0#dht.temperature
    
    save(fname, soil_hum_readings, hum, temp)

def backup_dropbox():
    pass#dropbox_upload_file(fname, '/save.txt')


def main():
    #measure_timer = RepeatedTimer(5, measure)
    #dropbox_timer = RepeatedTimer(15, backup_dropbox)

    httpd = create_web_server()
    httpd.run_thread()

    hs_in_s = 7200
    while True:
        measure()
        for _ in range(hs_in_s):
            sleep(1)




if __name__ == '__main__':
    main()