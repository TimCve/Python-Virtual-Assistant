import pyttsx3
import multiprocessing
import sys

from Assistant.Config.env_vars import wakeword
from Assistant.Base.stt import voiceCommandActivation

# say a phrase synchronously, halting code execution until finished speaking
def saySync(phrase):
	engine = pyttsx3.init()
	engine.setProperty('rate', 180)
	engine.say(phrase)
	engine.runAndWait()

# say a phrase asynchronously, can be stopped with the "stop" command, the assistant can also be powered off
def sayAsync(phrase):
  __name__ = "__main__"
  if __name__ == "__main__":
    tts = multiprocessing.Process(target=saySync, args=(phrase,))
    tts.start()
    while tts.is_alive():
      try:
        command = voiceCommandActivation()
        if(wakeword in command):
          command = " ".join(command.split(" ")[(command.split(" ").index(wakeword) + 1):])
          print("DETECTED: " + command)
          if "stop" in command:
            print("terminating tts thread")
            tts.terminate()
            tts.join()
          if "power" in command:
            tts.terminate()
            print("terminating tts thread")
            tts.join()
            saySync("powering off")
            sys.exit()
      except:
        if sys.exc_info()[0] == SystemExit:
          sys.exit()
        else:
          pass
    print("joining tts thread")
    tts.join()