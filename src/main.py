from soil_moisture import MultiplexorSensorsManager
from dht import DHT
from webserver import create_web_server



def main():
    sensor_manager = MultiplexorSensorsManager()
    dht = DHT()
    server = create_web_server()


if __name__ == '__main__':
    main()