import vlc
import threading
import requests
import pafy
from time import sleep
import sys

from Assistant.Config.env_vars import wakeword, api_key, vlc_path
from Assistant.Base.stt import convertSpeech, voiceCommandActivation

# sets up the path for VLC player
import os
os.add_dll_directory(vlc_path)

# creates a VLC instance and a player object
Instance = vlc.Instance()
player = Instance.media_player_new()
player.isPaused = False

# this function plays the song, it is called on a separate thread so it doesn't block code execution
def playSong(playurl):
	# setting up and playing the audio
	Media = Instance.media_new(playurl)
	Media.get_mrl()
	player.set_media(Media)
	player.play()

	sleep(2)
	while player.is_playing() or player.isPaused:
		# print(player.can_pause())
		# print(player.is_playing())
		sleep(0.2)
	player.stop()
	player.isPaused = False

# controls the song player
def playerController(song):
	# (important later)
	songId = ""

	# creates the save file if it does not exist
	if not os.path.exists("../saved_song_data.txt"):
		with open("../saved_song_data.txt", "w"): pass

	# checks if the song that the user wants to play exists in the save file
	saved_songs_txt = open("../saved_song_data.txt", "r")
	saved_songs = saved_songs_txt.read().split("\n\n")
	for i in range(len(saved_songs)):
		saved_songs[i] = saved_songs[i].split("\n")

	for saved_song in saved_songs:
		if saved_song[0] == song:
			print("Song data found in saved songs...")
			songId = saved_song[1]
			break

	# if the song does not exist, the songId variable stays empty
	# this code will now make 2 calls to the YouTube data API to get song data, it will also save that data in the save file
	if songId == "":
		print("Saving song data...")
		rawResponse = requests.get("https://www.googleapis.com/youtube/v3/search?type=video&videoCategoryId=10&q=" + song + "&key=" + api_key) # make a file called api_key.py and in there set an api_key variable to be your YouTube Data API key
		print(rawResponse.json())
		songId = rawResponse.json()["items"][0]["id"]["videoId"]

		with open("../saved_song_data.txt", "a") as save_file:
			save_file.write("\n\n" + song + "\n" + songId)

    # this creates the YouTube url for the song
	songUrl = "https://www.youtube.com/watch?v=" + songId

	# sets up the url for playing with VLC
	video = pafy.new(songUrl)
	best = video.getbest()
	playurl = best.url

	# creates the thread for the media player and starts it
	playerThread = threading.Thread(target=playSong, args=(playurl,))
	playerThread.start()

	# while the thread is alive, the user has the ability to stop it
	while playerThread.is_alive():
			try:
				command = voiceCommandActivation()
				if(wakeword in command):
					command = " ".join(command.split(" ")[(command.split(" ").index(wakeword) + 1):])
					print("DETECTED: " + command)
					if "stop" in command:
						player.stop()
						print("joining player thread")
						playerThread.join()
					if "pause" in command or "play" in command:
						player.pause()
						if player.isPaused:
							player.isPaused = False
						else:
							player.isPaused = True
						sleep(0.1)
						
				if not player.isPaused and not player.is_playing():
					print("joining player thread")
					playerThread.join()
			except:
				if sys.exc_info()[0] == SystemExit:
					sys.exit()
				else:
					pass

"""
while True:
	command = input("> ")
	if command.split(" ")[0] == "play":
		print("now playing " + command.split(" ", 1)[1] + "...")
		playerController(command.split(" ", 1)[1])
"""
