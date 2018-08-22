
import time

import speech_recognition as sr
import sounddevice as sd
from googletrans import Translator
from gtts import gTTS
import pygame



# this is called from the background thread
def callback(recognizer, audio):
	global CON_INPUT
	# received audio data, now we'll recognize it using Google Speech Recognition
	try:
		CON_INPUT = recognizer.recognize_sphinx(audio) + ' '
	except sr.UnknownValueError:
	    print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
	    print("Could not request results from Google Speech Recognition service; {0}".format(e))

def strsum(str_list):
	"""Returns the concatination of a list of strings."""
	r = ''
	for el in str_list:
		r += el + ' '
	return r[:-1]

def text_to_speech(text, target_lang):
	"""Converts text to a mp3 file and plays it."""
	tss = gTTS(text = text, lang = target_lang)
	tss.save("text2speech.mp3") 				# Save to a file
	pygame.mixer.music.load("text2speech.mp3")	# Load the file to pygame module
	pygame.mixer.music.play()					# Play the sound
	return True

CON_INPUT = ''

def main():
	pygame.mixer.init() 					# Initialize sound mixer to play text to speech
	global CON_INPUT 						# Declare the continuous input as a global variable
	r = sr.Recognizer() 					# Initalize a recognizer
	m = sr.Microphone()						# Initialize a microphone
	with m as source: 						# Use the microphone as a source
	    r.adjust_for_ambient_noise(source)  # We only need to calibrate once, before we start listening

	# start listening in the background (note that we don't have to do this inside a `with` statement)
	stop_listening = r.listen_in_background(m, callback)
	# `stop_listening` is now a function that, when called, stops background listening

	translator = Translator() 				# Initlizlie a translator
	while True: 							# For ever and ever
		if 'how do you say' in CON_INPUT: 	# Listen for "how do you say" as the trigger
			print("Heard: " + CON_INPUT) 	# Print what the microphone heard
			important_text = strsum(CON_INPUT.split()[4:]) # Cut out "how do you say"
			translated = translator.translate(important_text, dest = 'ru').text # Translate the input to russian
			print('вы говорите: ' + translated) # PRint some info
			text_to_speech(translated, 'ru')
			if pygame.mixer.music.get_busy():
				print("BUSY")
			else:
				pygame.mixer.music.stop()

			CON_INPUT = ''
		time.sleep(0.1)


if __name__ == '__main__':
	main()