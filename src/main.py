from soil_moisture import create_MultiplexedSensor_linear_callibration, read_sensor, ADS, ADDR
from dht import DHT
#from webserver import create_web_server
from save import save
from time import sleep
from timer import RepeatedTimer


fname = 'save.txt'
ADDR.set_pins([27, 22, 23])
sensors = [create_MultiplexedSensor_linear_callibration(i, 1, 0) for i in range(8)]
dht = DHT(24)


def measure():
    print('tick')

    soil_hum_readings = []
    for sensor in sensors:
        reading = read_sensor(sensor, 2)
        soil_hum_readings.append(reading)
    
    dht.update_values()
    hum = dht.humidity
    temp = dht.temperature
    
    save(fname, soil_hum_readings, hum, temp)


def main():
    measure_timer = RepeatedTimer(5, measure)

    while True:
        sleep(1)
        



if __name__ == '__main__':
    main()