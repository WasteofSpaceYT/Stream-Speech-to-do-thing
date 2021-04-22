# Imports
import speech_recognition as sr
# make a no function
with open('fullscript.txt', 'w') as script:
    script.truncate()
with open('speech.txt', 'w') as speech:
    speech.truncate()
x = 0
# Define your variable
r = sr.Recognizer()
# list the microphones
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
micindex = mics.index(micdevice)
mic = mics[int(micindex)]
print("Are you sure you want " + mic + "?")
ans = input()
# user dosen't want that input
if(ans == "no"):
    print("Which microphone do you want to use?")
    micindex = input("Mic Index: ")
    mic = mics[int(micindex)]
    print("Are you sure you want " + mic + "?")
    ans = input()
if(ans == 'yes'):
    try:
        x = 1
    except ValueError:
        x = 1

while x == 1:
    with sr.Microphone(int(micindex)) as source:
        r.adjust_for_ambient_noise(source, duration=1)
        while True:
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                if(text != None):
                    print(text)
                    with open('speech.txt', 'w') as speech:
                        speech.write(text)
                    with open("fullscript.txt", 'a') as script:
                        script.write(text + '\n')
                    x = 1
                x = 1
            except sr.UnknownValueError:
                x = 1
            
                
