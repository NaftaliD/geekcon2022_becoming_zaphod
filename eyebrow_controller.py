import time
from datetime import datetime
from os import path as osp
import json

import numpy as np
from gpiozero import Servo, BadPinFactory

CONFIG_PATH = osp.join(osp.dirname(__file__), "eyebrow_controller_config.json")


class EyebrowController:
    def __init__(self, is_random_mode = None):
        with open(CONFIG_PATH, 'r') as fid_:
            config = json.load(fid_)

        if is_random_mode is None:
            self.is_random_mode =  config["is_random_mode"]
        else:
            self.is_random_mode = is_random_mode
        self.is_up = False
        self.up_to_down_prob = config["up_to_down_prob"]
        self.down_to_up_prob = config["down_to_up_prob"]
        self.update_interval_sec = config["update_interval_sec"]

        np.random.seed(42)

        self.last_update_time = datetime.now()
        try:
            self.servo = Servo(config["servo_pin"], min_pulse_width=0.001, max_pulse_width=0.004, frame_width=0.02)
            if self.is_up:
                self.set_eyebrow_up()
            else:
                self.set_eyebrow_down()
        except BadPinFactory:
            self.servo = None

    def update_location(self, should_be_up):
        if self.servo is None:
            return
        
        if self.is_random_mode:
            if self.is_up and np.random.random() <= self.up_to_down_prob:
                self.is_up = False
                print("moving to down eye")
        else:
            if np.random.random() <= self.down_to_up_prob:
                self.is_up = True
                print("moving to up eye")

        self.is_up = should_be_up

        if (datetime.now() - self.last_update_time).microseconds * 1e6 < self.update_interval_sec:
            return

        if self.is_up:
            self.set_eyebrow_up()
        else:
            self.set_eyebrow_down()

    def set_eyebrow_up(self):
        if self.servo.value != -0.5:
            self.servo.value = -0.5

    def set_eyebrow_down(self):
        if self.servo.value != -1:
            self.servo.value = -1


if __name__ == '__main__':
    # config_ = {
    #     "is_random_mode": True,
    #     "up_to_down_prob": 0.2,
    #     "down_to_up_prob": 0.05,
    #     "servo_pin": "GPIO02",
    #     "update_interval_sec": 1
    # }
    # with open(CONFIG_PATH, 'w') as fid:
    #     json.dump(config_, fid, indent=4)

    controller = EyebrowController(is_random_mode=True)
    while True:
        controller.update_location(None)
        time.sleep(0.5)