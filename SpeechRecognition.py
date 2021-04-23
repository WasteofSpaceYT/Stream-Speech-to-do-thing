# Imports
from pynput.keyboard import Key, Controller
import speech_recognition as sr
import time

# Clear the files on startup
with open('fullscript.txt', 'w') as script:
    script.truncate()
with open('speech.txt', 'w') as speech:
    speech.truncate()

# Create a keyboard controller
keyboard = Controller()

# variables for loops
x = 0
y = 0

# Define the recognizer
r = sr.Recognizer()

# list only the microphones
while y == 0:
    mics = sr.Microphone.list_microphone_names()
    num = mics.index("Microsoft Sound Mapper - Output")
    numindexed = num + 1
    length = int(len(mics))
    lengthminus = length - 1
    while length > numindexed:
        del mics[lengthminus]
        num = mics.index("Microsoft Sound Mapper - Output")
        numindexed = num + 1
        length = int(len(mics))
        lengthminus = length - 1

    # list mics and select
    if(length == numindexed):
        del mics[0]
        newmiclength = len(mics) - 1
        del mics[newmiclength]
    print('\n'.join(map(str, mics)))
    print(" ")
    print("Which microphone do you want to use?")
    micdevice = input("Mic: ")
    try:
        if(micdevice.isdigit() == True):
            micindexed = int(micdevice) - 1
            micindexname = mics[micindexed]
            micindex = mics.index(micindexname)
        if(micdevice.isdigit() != True):
            micindex = mics.index(micdevice)
    except ValueError:
        y = 0

    mic = mics[int(micindex)]
    print("Are you sure you want " + mic + "?")
    ans = input()
    # user dosen't want that input
    if(ans == "no"):
        y = 0
    # User wants the input
    if(ans == 'yes'):
        try:
            y = 1
            x = 1
        except ValueError:
            y = 1
            x = 1

# The speech recognition itself
while x == 1:
    # Make the mic object with the pre decided device as input
    with sr.Microphone(int(micindex)) as source:
        
        while True:
            # listen and save that as audio data
            audio = r.listen(source)

            try:
                #take the audio data and run it through the recognition
                text = r.recognize_google(audio)
                
                # makes sure the text has a value
                if(text != None):

                    # print to console
                    print(text)

                    # print to file
                    with open('speech.txt', 'w') as speech:
                        speech.write(text)
                    
                    # check script for word
                    with open('speech.txt', 'r') as speech:
                        word = speech.readline()

                        # check if word is on blacklist
                        with open('blacklist.txt', 'r') as blacklist:
                            blklst = blacklist.readlines()
                            listsep = blklst[0].split(" ")
                            print(listsep)
                            if(listsep.__contains__(word)):
                                print('Your mom dosent love you')      
                    
                    # print to file
                    with open("fullscript.txt", 'a') as script:
                        script.write(text + '\n')
                    x = 1
                x = 1
                
                # Checks for a value error
            except sr.UnknownValueError:
                x = 1