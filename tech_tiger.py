from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from gtts import gTTS
import pygame
import os
import threading
import speech_recognition as sr

class TechTigerApp(App):
    def build(self):
        Window.size = (400, 600)
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.logo = Image(source='Logo.jpg', size_hint=(None, None), size=(200, 200))
        layout.add_widget(self.logo)
        
        self.start_button = Button(text='START', font_size=24, size_hint=(None, None), size=(200, 60),
                                   on_press=self.start_listening, background_color=(0, 1, 0, 1))
        layout.add_widget(self.start_button)

        self.stop_button = Button(text='STOP', font_size=24, size_hint=(None, None), size=(200, 60),
                                  on_press=self.stop_listening, background_color=(1, 0, 0, 1))
        layout.add_widget(self.stop_button)

        self.minimize_button = Button(text='MINIMIZE', font_size=20, size_hint=(None, None), size=(200, 50),
                                      on_press=self.minimize_app, background_color=(0.5, 0.5, 0.5, 1))
        layout.add_widget(self.minimize_button)
        
        return layout
    
    def speak(self, text):
        tts = gTTS(text=text, lang="bn")
        tts.save("response.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        os.remove("response.mp3")

    def listen_and_respond(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("MeriJin activated")
            recognizer.adjust_for_ambient_noise(source)
            self.speak("আপনি কি জানতে চান?")
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language="bn-BD")
            print("আপনি বললেন:", command)
            response = self.get_response(command)
            self.speak(response)
        except sr.UnknownValueError:
            self.speak("দুঃখিত, আমি বুঝতে পারিনি")
        except sr.RequestError:
            self.speak("সার্ভারের সাথে সংযোগ করা যাচ্ছে না")
    
    def get_response(self, command):
        try:
            with open("data.txt", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if command.lower() in line.lower():
                        return line.strip()
        except FileNotFoundError:
            return "আমি তথ্য খুঁজে পাচ্ছি না।"
        return "আমি বুঝতে পারিনি, দয়া করে আবার বলুন।"
    
    def start_listening(self, instance):
        threading.Thread(target=self.listen_and_respond).start()
    
    def stop_listening(self, instance):
        self.speak("Tech Tiger বন্ধ হচ্ছে")
        App.get_running_app().stop()
    
    def minimize_app(self, instance):
        Window.hide()  # শুধু UI ছোট হবে, কিন্তু AI চলবে

if __name__ == "__main__":
    TechTigerApp().run()
