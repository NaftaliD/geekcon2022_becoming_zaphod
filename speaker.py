"""Getting Started Example for Python 2.7+/3.3+"""
import os
import time
from contextlib import closing
from tempfile import gettempdir

import numpy as np
import vlc
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from gpiozero import Servo


def play_text(text: str):

    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    # session = Session(profile_name="adminuser")
    session = Session()
    polly = session.client("polly")

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                            VoiceId="Brian")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        raise

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
               output = os.path.join(gettempdir(), "speech.mp3")

               try:
                # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                       file.write(stream.read())
               except IOError as error:
                  # Could not write to file, exit gracefully
                  raise

    else:
        # The response didn't contain audio data, exit gracefully
        raise Exception("no audio data")

    mouth_servo = Servo('GPIO03', min_pulse_width=0.001, max_pulse_width=0.004, frame_width=0.02)

    print(output)
    p = vlc.MediaPlayer(output)
    p.play()
    start = time.time()
    time.sleep(0.1)
    duration = p.get_length()/1000
    while time.time() - start < duration:
        mouth_servo.value = -1
        time.sleep(0.2)
        mouth_servo.value = 0
        time.sleep(0.2)
    p.stop()
    p.release()


SENTANCES = [ "Please tell me more.",
        "Can you elaborate on that?, oh wait I dont care",
        "Why do you say that?",
        "I see you are ugly.",
        "Very interesting.",
        "I see.  And what does that tell you?",
        "How does that make you feel?",
        "How do you feel when you say that?",
        "Can please you go and search for me in the other room?",
        "Ow! My brains!",
        "If there's anything more important than my ego around, I want it caught and shot now.",
        "Don't try to understand me, just be grateful that you felt the warmth of Zaphod Beeblebrox's aura on your wonderstruck face.",
        "What is this? Some sort of galactic hyperhearse?",
        "If I ever meet myself,' said Zaphod, 'I'll hit myself so hard I won't know what's hit me.",
        "Thank you, for nothing",
        "Are you scared by computers? Oh what a wanker",
        "Go home, you are drunk",
        "because I am bloody awesome",
        "That's a great question, and I know exactly who can answer, the trash bin there in the corner",
        "Also, there are aliens, just in front of you",
        "Yes, you may kiss my boot",
        "The galaxy is a dump, and I am the president",
        "When you have a scalpel in hand, everything is a patient",
        "Thanks for the fishes",
        "Goodbye and fuck you very much",
        "I dont like you and it is personal",
        "I dont like to talk about myself. But I am the best",
        "Dont you, forget about me",
        "There's a starman waiting in the sky, he'd like to come and meet us but he thinks he'd blow our minds"
        "how... you doing?",
        "I could ask you for more, but I don't really care",
        "Every place is the center of the universe, scientifically proven",
        ]


if __name__ == '__main__':
    play_text("Hi, I'm Zaphod, and fuck you too")
    n_sentances = len(SENTANCES)
    while True:
        time.sleep(4)
        phrase = SENTANCES[int(np.random.random() * n_sentances)]
        print(phrase)
        play_text(phrase)
