
"""record to buffer and send when needed"""

import pyaudio
import wave
import time
import vlc
import buffer
import transcribe
import threading
import subprocess
import pygame
import speaker
from zaphod import Zaphod

from pygame.locals import(
    KEYDOWN,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP
)

class AudioRecorder():
# Audio class based on pyAudio and Wave
    def __init__(self, filename):

        self.open = True
        self.rate = 48000
        self.frames_per_buffer = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        self.audio_filename = filename
        self.audio = pyaudio.PyAudio()
        print("Channels = "+str(self.audio.get_device_info_by_index(0).get('channels')))
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      input_device_index=0,
                                      frames_per_buffer = self.frames_per_buffer)
        self.buffer_secs = 4
        self.audio_frames = buffer.RingBuffer(int((self.rate/ \
                                                   self.frames_per_buffer)* \
                                                   self.buffer_secs))

    def record(self):
        pygame.init()
        self.stream.start_stream()
        while self.open:
            data = self.stream.read(self.frames_per_buffer, exception_on_overflow = False) 
            self.audio_frames.append(data)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN): 
                    #send data to cloud
                    self.stream.stop_stream()
                    print("sending recording to cloud")
                    self.send_to_cloud()
                    #send text to speech
                    text = transcribe.sound_to_text_assemblyai(self.audio_filename)
                    #comment = (' '.join(text_dict.get("comment", ''))).strip()
                    print(text)
                    if text:
                        z = Zaphod()
                        response = z.respond(text)
                        print(response)
                        speaker.play_text(response)
                    print("back to record")
                    self.stream.start_stream()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop()


    def send_to_cloud(self):
        #write to te temp file
        waveFile = wave.open(self.audio_filename, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.audio.get_sample_size(self.format))
        waveFile.setframerate(self.rate)
        print(len(self.audio_frames.get()))
        waveFile.writeframes(b''.join(self.audio_frames.get()))
        waveFile.close()
        #do send to cloud

    # Finishes the audio recording therefore the thread to
    def stop(self):

        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
        pass



if __name__ == '__main__':
    print("start recording")
    filename = "temp_audio.wav"
    audio = AudioRecorder(filename)
    audio.record()
    print("done recording")
