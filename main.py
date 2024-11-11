import random
import datetime
import webbrowser
import json
from typing import Dict, List
import re
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
import speech_recognition as sr
import pyttsx3
import os
import subprocess
import platform

class AdvancedEmotionalChatbot:
    def __init__(self):
        # Set both possible names
        self.names = ["Emoti", "Iris"]
        self.current_name = random.choice(self.names)  # Choose one at random initially
        self.emotion = "neutral"
        self.emotion_levels = {
            "happiness": 50,
            "energy": 50,
            "friendliness": 50
        }
        
        # Initialize speech recognition and text-to-speech
        self.initialize_speech_systems()
        
        # Initialize DialoGPT model
        print("Initializing DialoGPT model... This might take a moment.")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
            self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
            self.chat_history_ids = None
            self.max_history = 5
            print("DialoGPT model initialized successfully!")
        except Exception as e:
            logging.error(f"Error loading DialoGPT model: {str(e)}")
            print("Failed to load DialoGPT model. Falling back to basic responses.")
            self.model = None
            self.tokenizer = None
        
        # System information
        self.system = platform.system().lower()
        
        # Common application paths
        self.common_apps = {
            'windows': {
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'paint': 'mspaint.exe',
                'explorer': 'explorer.exe',
                'word': 'WINWORD.EXE',
                'excel': 'EXCEL.EXE',
                'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe'
            },
            'darwin': {  # macOS
                'notepad': 'TextEdit.app',
                'calculator': 'Calculator.app',
                'safari': 'Safari.app',
                'finder': 'Finder.app',
                'terminal': 'Terminal.app'
            },
            'linux': {
                'notepad': 'gedit',
                'calculator': 'gnome-calculator',
                'terminal': 'gnome-terminal',
                'files': 'nautilus'
            }
        }
        
        # Extended commands dictionary
        self.commands = {
            "time": "Get current time",
            "date": "Get current date",
            "weather": "Check weather (simulated)",
            "search": "Search the web",
            "joke": "Tell a joke",
            "help": "Show available commands",
            "reset": "Reset conversation history",
            "emotion": "Show current emotional state",
            "open": "Open a file or application",
            "list apps": "List available applications",
            "voice": "Toggle voice mode",
            "speak": "Toggle text-to-speech",
            "listen": "Toggle speech recognition"
        }

    def initialize_speech_systems(self):
        """Initialize speech recognition and text-to-speech engines"""
        # Initialize text-to-speech
        try:
            self.tts_engine = pyttsx3.init()
            # Configure text-to-speech properties
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.9)
            voices = self.tts_engine.getProperty('voices')
            # Set a female voice if available
            for voice in voices:
                if "female" in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            self.voice_enabled = True
        except Exception as e:
            logging.error(f"Error initializing text-to-speech: {str(e)}")
            self.tts_engine = None
            self.voice_enabled = False

        # Initialize speech recognition
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.speech_recognition_enabled = True
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            logging.error(f"Error initializing speech recognition: {str(e)}")
            self.speech_recognition_enabled = False

    def listen(self) -> str:
        """Listen for voice input and convert to text"""
        if not self.speech_recognition_enabled:
            return "Speech recognition is not available."
        
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5)
                print("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.WaitTimeoutError:
            return "No speech detected"
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not request results"
        except Exception as e:
            logging.error(f"Error in speech recognition: {str(e)}")
            return "Error processing speech"

    def speak(self, text: str):
        """Convert text to speech"""
        if self.voice_enabled and self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                logging.error(f"Error in text-to-speech: {str(e)}")
                print(text)  # Fallback to printing
        else:
            print(text)

    def respond(self, input_text: str) -> str:
        """Generate a response using the model"""
        # Example processing for commands, logic, etc.
        return f"{self.current_name}: {input_text}"  # Example of appending current assistant name

    def main():
        chatbot = AdvancedEmotionalChatbot()
        greeting = f"Hello! I'm {chatbot.current_name}. How can I help you today?"
        print(greeting)
        chatbot.speak(greeting)
        
        while True:
            if chatbot.speech_recognition_enabled:
                user_input = chatbot.listen()
                print(f"\nYou said: {user_input}")
            else:
                user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                response = f"{chatbot.current_name}: Goodbye! Take care! 👋"
                print(response)
                chatbot.speak("Goodbye! Take care!")
                break
            
            response = chatbot.respond(user_input)
            print(response)
            
            if chatbot.voice_enabled:
                clean_response = re.sub(r'[^\w\s.,?!]', '', response)
                chatbot.speak(clean_response)

if __name__ == "__main__":
    AdvancedEmotionalChatbot.main()
