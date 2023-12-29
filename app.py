from flask import Flask, render_template
import pygame
import os
import random
import threading
import time

app = Flask(__name__)

# Set the paths to the static music folders
music_folder1 = os.path.join("/Users/ezequielabregu/code/personal/disco_eterno/static/eze")
music_folder2 = os.path.join("/Users/ezequielabregu/code/personal/disco_eterno/static/gus")

tracks1 = [file for file in os.listdir(music_folder1) if file.endswith(".mp3")]
tracks2 = [file for file in os.listdir(music_folder2) if file.endswith(".mp3")]

random.shuffle(tracks1)
random.shuffle(tracks2)

current_track1 = None
current_track2 = None
channel1 = None
channel2 = None
playing1 = False
playing2 = False

pygame.init()

def play_music1():
    global current_track1, channel1, tracks1
    while playing1:
        if not channel1.get_busy():
            if not tracks1:
                random.shuffle(tracks1)
            current_track1 = os.path.join(music_folder1, tracks1.pop())
            channel1.queue(pygame.mixer.Sound(current_track1))
        pygame.time.wait(100)  # Adjust as needed for synchronization

def play_music2():
    global current_track2, channel2, tracks2
    while playing2:
        if not channel2.get_busy():
            if not tracks2:
                random.shuffle(tracks2)
            current_track2 = os.path.join(music_folder2, tracks2.pop())
            channel2.queue(pygame.mixer.Sound(current_track2))
        pygame.time.wait(100)  # Adjust as needed for synchronization

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    global playing1, playing2, channel1, channel2
    if not playing1 and not playing2:
        playing1 = True
        playing2 = True
        channel1 = pygame.mixer.Channel(1)
        channel2 = pygame.mixer.Channel(2)
        threading.Thread(target=play_music1).start()
        threading.Thread(target=play_music2).start()
    return "Started"

@app.route("/stop")
def stop():
    global playing1, playing2, tracks1, tracks2
    if playing1 or playing2:
        playing1 = False
        playing2 = False
        time.sleep(1)  # Give some time for the threads to gracefully stop
        pygame.mixer.stop()
        # Reset the shuffled tracks for the next playback
        tracks1 = [file for file in os.listdir(music_folder1) if file.endswith(".mp3")]
        tracks2 = [file for file in os.listdir(music_folder2) if file.endswith(".mp3")]
        random.shuffle(tracks1)
        random.shuffle(tracks2)
    return "Stopped"

if __name__ == "__main__":
    app.run(debug=True)
