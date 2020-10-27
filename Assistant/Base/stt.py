import speech_recognition as sr
from time import sleep

from Assistant.Config.env_vars import voice_recognition_energy_threshhold, voice_recognition_dynamic_energy_threshhold

sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer()

# prints all available microphones
def printMicrophones():
	print("------Microphones Found------")

	for index, name in enumerate(sr.Microphone.list_microphone_names()):
		    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

	print("----------------------------------")

# selects the default system microphone
mic = sr.Microphone(device_index=0, sample_rate = sample_rate, chunk_size = chunk_size)

def convertSpeech(limit=None):
    with mic as source:
    	# adjusts for ambient noise
        # r.adjust_for_ambient_noise(source)
        r.energy_threshold = voice_recognition_energy_threshhold
        r.dynamic_energy_threshold = voice_recognition_dynamic_energy_threshhold

        # message displayed when speech recognition is ready
        print("STARTED SPEECH RECOGNITION")

        if limit:
            # listen for audio for a specified amount seconds
            audio = r.listen(source, phrase_time_limit=limit)
        else:
            audio = r.listen(source)

    # recognize speech with the google speech recognition engine
    result = r.recognize_google(audio)

    # returns the resulting recognized speech
    return result

# function to detect if the user said the wakeword and record the command that followed
def voiceCommandActivation():
    command = convertSpeech()
    return command
