from os import path as osp
import json

import numpy as np
from gpiozero import Servo, BadPinFactory


CONFIG_PATH = osp.join(osp.dirname(__file__), "eye_controller_config.json")


class EyeController:
    def __init__(self):
        with open(CONFIG_PATH, 'r') as fid_:
            config = json.load(fid_)

        self.angles_range = config["angles_range"]
        self.movement_range = config["movement_range"]
        # self.black_pupil_loc = self.angles_range / 2  # angular in -90..90
        # self.red_pupil_loc = movement_range
        self.black_pupil_loc = -1 + self.angles_range / self.movement_range / 2  # linear in -1..0
        self.red_pupil_loc = 0
        self.servo_every_n_frames = config["servo_every_n_frames"]
        self.black_to_red_prob = config["black_to_red_prob"]
        self.red_to_black_prob = config["red_to_black_prob"]
        self.mark_pupil_mode = config["mark_pupil_mode"]

        # self.servo = AngularServo(SERVO_PIN, min_angle=-90, max_angle=90)

        self.is_eye_black = (self.mark_pupil_mode is None) or (self.mark_pupil_mode.lower() == "black")
        np.random.seed(42)
        self.frame_id = 0

        try:
            self.servo = Servo(config["servo_pin"], max_pulse_width=0.004)
            if self.is_eye_black:
                # self.servo.angle = self.black_pupil_loc
                self.servo.value = self.black_pupil_loc
            else:
                # self.servo.angle = self.red_pupil_loc
                self.servo.value = self.red_pupil_loc
        except BadPinFactory:
            self.servo = None

    def update_location(self, relative_x_center):
        if self.servo is None:
            return

        # servo_angle = self.black_pupil_loc + relative_x_center * self.angles_range
        servo_value = self.black_pupil_loc + relative_x_center * self.angles_range / self.movement_range
        self.frame_id += 1
        if self.frame_id % self.servo_every_n_frames == 0:
            if self.mark_pupil_mode:
                pass
            elif self.is_eye_black:
                if np.random.random() <= self.black_to_red_prob:
                    self.is_eye_black = False
                    self.servo.value = self.red_pupil_loc
                    print("moving to red eye")
                else:
                    self.servo.value = servo_value
            else:
                # red pupil
                if np.random.random() <= self.red_to_black_prob:
                    self.is_eye_black = True
                    self.servo.value = servo_value
                    print("moving to black eye")
                else:
                    pass  # red pupil is static


if __name__ == '__main__':
    config_ = {
        "angles_range": 100,
        "movement_range": 135,
        "servo_every_n_frames": 5,
        "black_to_red_prob": 0.2,
        "red_to_black_prob": 0.8,
        "mark_pupil_mode": None,
        "servo_pin": "GPIO04",
    }
    with open(CONFIG_PATH, 'w') as fid:
        json.dump(config_, fid, indent=4)
