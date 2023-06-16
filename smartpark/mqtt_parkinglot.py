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
                #self.current_cars = self.total_spaces
        else:
            self.current_cars=self.current_cars-1
            if (self.current_cars < 0):
                print("Invalid number")
                self.current_cars = 0
        self.count_available_cars()
    
    def get_time_and_temperature(self):
        return f'{random.randint(0, 45):02d}℃', time.strftime("%H:%M:%S")

    def count_available_cars(self):
        current_time, temperature=self.get_time_and_temperature()
        display_available_cars = min(self.total_spaces-self.current_cars,self.total_spaces) # =< self.total_spaces
        display_available_cars = max(display_available_cars,0) # => 0

        self.client.publish("lot/display",  str(display_available_cars)+"@"+current_time+"@"+temperature)



if __name__ == '__main__':
    # TODO: Run each of these classes in a separate terminal. You should see the CarParkDisplay update when you click the buttons in the CarDetector.
    # These classes are not designed to be used in the same module - they are both blocking. If you uncomment one, comment-out the other.
    config = config_parser.parse_config("config.toml") 
    ParkingLot(config)


