import pygame
from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '200')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
import pyttsx3
import speech_recognition as sr
import random
import os
import sys
import time
import datetime
import logging
import webbrowser
import subprocess

r = sr.Recognizer()
m = sr.Microphone()

greeting = ("привет","здоров","хай","хей","здравствуй","здравствуйте","добрый день","хаюшки","приветики")
greeting_answer=("Приветствую","Доброго времени суток","Добропожаловать"," Моё почтение","разрешите вас приветствовать!","Привет, Машенька!","Сколько лет, сколько зим","Рад тебя видеть!")

how_are=("как твои дела","как ты","как поживаешь","шо ты")
how_are_ans=("Спасибо, в порядке, а у тебя","Не жалуюсь,а твои как","Всё отлично,ты шо?","Мне важнее знать как твои дела","Хорошо , а ты как")

how_are_ans_for_ans=("лучше всех","всё ок","всё пучком","хорошо","всё хорошо","отлично","как в сказке")


all_question=("привет","здоров","хай","хей","здравствуй","здравствуйте","добрый день","хаюшки","приветики","как твои дела","как ты","как поживаешь","шо ты",
              "открой браузер","калькулятор","браузер","открой калькулятор","блокнот")


# Root Widget
class Root(BoxLayout):
    pass


class RecordButton(Button):
    # String Property to Hold output for publishing by Textinput
    output = StringProperty('')

    def record(self):
        # GUI Blocking Audio Capture
        with m as source:
            audio = r.listen(source)
            engine = pyttsx3.init()

        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio,language="ru_RU")
            #Простое общение с собеседником
            if ((value.lower() in greeting) ):
                ans=greeting_answer[random.randint(0,len(greeting_answer)-1)]
                engine.say(ans)
                engine.runAndWait()

            if ((value.lower() in how_are) ):
                ans=how_are_ans[random.randint(0,len(how_are_ans)-1)]
                engine.say(ans)
                engine.runAndWait()

            if ((value.lower() in all_question) ==False ):
                ans = "Меня не научили на это отвечать"
                engine.say(ans)
                engine.runAndWait()
            #Выполнение различных команд
                # Команды для открытия различных внешних приложений
                if ((value.lower() =="калькулятор") or (value.lower() =="открой калькулятор")):
                    self.osrun('calc')

                if ((value.lower() =="блокнот") or (value.lower() =="открой блокнот")):
                    self.osrun('notepad')
                if ((value.lower() == "браузер") or (value.lower() == "открой браузер")):
                    self.openurl('http://google.com')

                # Команды для открытия URL в браузере

                if ((value.lower() =="ютуб") or (value.lower() =="открой ютуб")):
                    self.openurl('http://youtube.com')
                if ((value.lower() == "почта") or (value.lower() == "открой почту")):
                    self.openurl('https://mail.google.com/mail/u/0/#inbox')

                if ((value.lower() == "телеграм") or (value.lower() == "открой телеграм")):
                    self.openurl('https://web.telegram.org/')
                # Команды для поиска в сети интернет

                if ((value.lower() == "найди") or (value.lower() == "поиск")):
                    self.openurl('https://www.google.com/search?q=' + value)

                if ((value.lower() == "фильм") or (value.lower() == "смотреть фильм")):
                    self.openurl('https://www.google.com/search?q=Смотреть+онлайн+фильм+' + value)
                if ((value.lower() == "ютуб") or (value.lower() == "смотреть на ютуб")):
                    self.openurl('http://www.youtube.com/results?search_query=' + value)
            self.output = " You said \"{}\"".format(value)
        except sr.UnknownValueError:
            self.output = ("Повторите пожалуйста")

        except sr.RequestError as e:
            self.output = ("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

    def openurl(self, url):
        webbrowser.open(url)


    def osrun(self, cmd):
        PIPE = subprocess.PIPE
        p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)

class SpeechApp(App):
    def build(self):
        # Calibrate the Microphone to Silent Levels
        print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
        # Create a root widget object and return as root
        return Root()


# When Executed from the command line (not imported as module), create a new SpeechApp
if __name__ == '__main__':
    SpeechApp().run()