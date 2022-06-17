from Actuators.Actuator import Actuator
from MQTT.vehicledetectionmessage_pb2 import Action
from pydub import AudioSegment
from pydub.playback import play
import multiprocessing


siren = AudioSegment.from_file("./Assets/siren.mp3", format="mp3")
playThread = None

def play_loop():
    while True:
        play(siren)

def on_message(action: Action):
    global playThread
    if action == Action.ON:
        if playThread is None:
            playThread = multiprocessing.Process(target=play_loop, args=())
            playThread.start()
    else:
        if playThread is not None:
            playThread.terminate()
        playThread = None


def main():
    actuator = Actuator(on_message)
    ready = AudioSegment.from_file("./Assets/ready.mp3", format="mp3")
    play(ready)
    actuator.on_run()

