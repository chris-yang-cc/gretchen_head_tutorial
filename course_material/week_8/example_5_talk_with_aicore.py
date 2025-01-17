#!/usr/bin/env python
import sys
import speech_recognition as sr
import playsound
from gtts import gTTS
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.aicore_client import AICoRE

def main():
    #We need to initalize ROS environment for AICoRE to connect
    ROSEnvironment()
    #Initalize AICoRe client
    client = AICoRE()
    #Set up client name
    client.setUserName('Jacob')

    #Initalize speeech recogniton
    r = sr.Recognizer()
    #Initalize mic
    #TODO set the microphone index
    mic = sr.Microphone(device_index=11)
    print("start talking")
    with mic as source:
        #adjust for noise
        r.adjust_for_ambient_noise(source)
        #listen to source
        audio = r.listen(source)
    #convert audio to text
    text = r.recognize_google(audio)
    #send text to client
    client.send(text)
    #get answer from AICoRe
    answer = client.answer()

    #creates speech from text
    tts = gTTS(answer)
    #saves the answer to mp3 file
    tts.save('answer.mp3')
    #plays the mp3
    playsound.playsound('answer.mp3')

if __name__ == '__main__':
    main()
