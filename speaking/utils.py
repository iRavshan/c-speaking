import os
import pyttsx3

def generate_audio_file(title, filename):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  
    engine.save_to_file(title, filename)
    engine.runAndWait()