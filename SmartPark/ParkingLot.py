import paho.mqtt.client as paho
import time
import random
import config_parser

class ParkingLot():

    def __init__(self, config):
        self.total_spaces = config['total_spaces']  
        self.current_cars=0
        self.client = paho.Client()
        self.client.connect(config["broker_host"], config["broker_port"])
        self.client.on_message = self.on_message_from_sensor 

        self.client.subscribe("lot/sensor")
        self.client.loop_forever()

    def on_message_from_sensor(self,client, userdata, msg):
        print(f'Received {msg.payload.decode()}')
        incoming=msg.payload.decode()
        if(incoming=="in"):
            self.current_cars=self.current_cars+1 
            if (self.current_cars > self.total_spaces):
                print("Fully occupied")
                self.current_cars = self.total_spaces
        else:
            self.current_cars=self.current_cars-1
            if (self.current_cars < 0):
                print("Invalid number")
                self.current_cars = 0
        self.Count_available_cars()
    
    def getTimeAndTemperature(self):
        return f'{random.randint(0, 45):02d}℃', time.strftime("%H:%M:%S")

    def Count_available_cars(self):
        currentTime, temperature=self.getTimeAndTemperature()
        self.client.publish("lot/display",  str(192-self.current_cars)+"@"+currentTime+"@"+temperature)



if __name__ == '__main__':
    # TODO: Run each of these classes in a separate terminal. You should see the CarParkDisplay update when you click the buttons in the CarDetector.
    # These classes are not designed to be used in the same module - they are both blocking. If you uncomment one, comment-out the other.
    config = config_parser.parse_config("config.toml") 
    ParkingLot(config)
