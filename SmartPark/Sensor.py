"""The following code is used to provide an alternative to students who do not have a Raspberry Pi.
If you have a Raspberry Pi, or a SenseHAT emulator under Debian, you do not need to use this code.

You need to split the classes here into two files, one for the CarParkDisplay and one for the CarDetector.
Attend to the TODOs in each class to complete the implementation."""
import tkinter as tk
import paho.mqtt.client as paho
import config_parser



class CarDetector:
    """Provides a couple of simple buttons that can be used to represent a sensor detecting a car. This is a skeleton only."""

    def __init__(self, config):
        self.root = tk.Tk()
        self.root.title("Car Detector ULTRA")

        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Incoming Car', font=('Arial', 50), cursor='right_side', command=self.incoming_car)
        self.btn_incoming_car.pack(padx=10, pady=5)
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car 🚘',  font=('Arial', 50), cursor='bottom_left_corner', command=self.outgoing_car)
        self.btn_outgoing_car.pack(padx=10, pady=5)

        self.client = paho.Client()
        self.client.connect(config["broker_host"], config["broker_port"])



        self.root.mainloop()

    def incoming_car(self):
        # TODO: implement this method to publish the detection via MQTT
        self.client.publish("lot/sensor", "in")
        print("Car goes in")

    def outgoing_car(self):
        # TODO: implement this method to publish the detection via MQTT
        self.client.publish("lot/sensor", "out")
        print("Car goes out")


if __name__ == '__main__':
    # TODO: Run each of these classes in a separate terminal. You should see the CarParkDisplay update when you click the buttons in the CarDetector.
    # These classes are not designed to be used in the same module - they are both blocking. If you uncomment one, comment-out the other.

    config = config_parser.parse_config("config.toml") 
    CarDetector(config)
