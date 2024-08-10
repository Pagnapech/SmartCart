# https://docs.sunfounder.com/projects/raphael-kit/en/latest/python/3.1.3_audio_module_python.html#py
# https://docs.sunfounder.com/projects/raphael-kit/en/latest/components/component_audio_speaker.html

from pygame import mixer
from time import sleep 


def itemInCart():
    mixer.init()
    mixer.music.load(f'/home/pi/Desktop/AutoCart/audioModule/button-pressed-38129.mp3')
    mixer.music.set_volume(0.7)
    mixer.music.play()

def itemOutCart():
    mixer.init()
    mixer.music.load(f'/home/pi/Desktop/AutoCart/audioModule/beep-6-96243.mp3')
    mixer.music.set_volume(0.7)
    mixer.music.play()

# itemInAudio()
# sleep(2)
# itemOutAudio()