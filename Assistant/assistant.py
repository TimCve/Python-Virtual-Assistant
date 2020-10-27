import sys

from Assistant.Config.env_vars import wakeword
from Assistant.Base import tts, stt
from Assistant.Skills import wiki, musicplayer

musicplayer.playerController("Thunder")

def powerOff():
	tts.saySync("powering off")
	sys.exit()

"""
command: {what the user has to say to trigger the command}
hasArgs: {if there is a variable argument after the initial command (e.g. Wikipedia [argument])}
function: {the function that the command executes}
"""
commandsList = [
	{
		"command": "power",
		"hasArgs": False,
		"function": powerOff
	},
	{
		"command": "Wikipedia",
		"hasArgs": True,
		"function": wiki.makeQuery
	},
	{
		"command": "play",
		"hasArgs": True,
		"function": musicplayer.playerController
	}
]

# parses command and executes the command function appropriately
def executeCommand(command):
  for cmd in commandsList:
    if cmd["command"] in command:
      if cmd["hasArgs"]:
        args = command.split(" ", len(cmd["command"].split(" ")))[len(cmd["command"].split(" "))]
        cmd["function"](args)
      else:
        cmd["function"]()

# main function, runs the voiceCommandActivation function until it picks up a command, the command is then executed
while __name__ == "__main__":
	try:
		command = stt.voiceCommandActivation()
		if(wakeword in command):
			# command.split(" ").index(wakeword)
			command = " ".join(command.split(" ")[(command.split(" ").index(wakeword) + 1):])
			print("DETECTED: " + command)
			executeCommand(command)
	except:
		if sys.exc_info()[0] == SystemExit:
			sys.exit()
		else:
			pass