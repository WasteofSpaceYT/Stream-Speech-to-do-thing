# Imports
import speech_recognition as sr
# Define your variable
r = sr.Recognizer()
# define the no function
def no():
    with sr.Microphone(int(micindex)) as source:
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            if(text != None):
                splittext = text.split(" ")
                print('\n'.join(map(str, splittext)))
                no()
            no()
        except sr.UnknownValueError:
            no()
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
        no()
    except ValueError:
        no()

