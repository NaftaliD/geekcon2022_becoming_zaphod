from datetime import datetime, timedelta

import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

from eyebrow_controller import EyebrowController


class HeadState:
    LISTENING = "listening"
    TALKING = "talking"
    WAITING = "waiting"


class ConversationController:
    def __init__(self):
        self.eb_controller = EyebrowController(is_random_mode=True)
        self.head_state = HeadState.WAITING
        self.reset()

    def run(self):
        while True:
            have_person_now = self.is_person_seen()

            if self.head_state == HeadState.WAITING and not have_person_now:
                pass
            elif self.head_state == HeadState.WAITING and have_person_now:
                self.start_new_conversation()
            elif self.head_state in [HeadState.TALKING, HeadState.LISTENING]:
                and have_person_now:
                continue_conversation()
            elif conversation_state and not have_person_now:
                end_conversation()
            else:
                reset()  # shouldn't have gt here
            frame_id += 1


if __name__ == '__main__':
    main()
