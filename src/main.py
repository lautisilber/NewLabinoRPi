from soil_moisture import create_MultiplexedSensor_linear_callibration, read_sensor, ADS, ADDR
from dht import DHT
#from webserver import create_web_server
from save import save
from time import sleep


fname = 'save.txt'

def main():
    ADDR.set_pins([27, 22, 23])

    sensors = [create_MultiplexedSensor_linear_callibration(i, 1, 0) for i in range(8)]

    while True:
        print('tick')

        soil_hum_readings = []
        for sensor in sensors:
            reading = read_sensor(sensor, 2)
            soil_hum_readings.append(reading)
        hum = 0
        temp = 0
        
        save(fname, soil_hum_readings, hum, temp)
        
        sleep(5)



if __name__ == '__main__':
    main()