import speech_recognition as s

#create an object of Recognizer
sr=s.Recognizer()


# Use microphone as the audio source
with s.Microphone()as m:
    print("I am listening to you...")
    # Record the audio
    audio= sr.listen(m)
    
try:
    # Recognize the speech using Google Speech Recognition Engine
    print("You said:", sr.recognize_google(audio))
except s.UnknownValueError:
    print("Sorry, could not understand the audio.")
except s.RequestError as e:
    print("Could not request results from Google Speech Recognition service; (0)",format(e))



