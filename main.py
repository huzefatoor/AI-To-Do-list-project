import time
from tinydb import TinyDB, Query
import sounddevice as sd
from scipy.io.wavfile import write
from model import speech_to_text
import assemblyai as aai 

db = TinyDB('db.json')
FILE_LOCATION = YOUR_FILE_LOCATION

def main():
    #record audio file
    fs = 44100
    seconds = 5

    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(FILE_LOCATION, fs, recording)

    converter = speech_to_text(a906f30674f84cd4b2bf9b6b55c367db)

    upload = converter.upload_file(FILE_LOCATION)

    audio_file = converter.submit_audio(upload["upload_url"])

    time.sleep(10)

    text = converter.get_text(audio_file["id"])

    # insert into database
    db.insert({"todo": text["text"]})

    # print list of todosuc
    if text["status"] != "error":
        print("Todo List")
        for item in db:
            print(item["todo"])
        return
    else:
        print(f"Error getting list: {text['error']}")
        return
    
if __name__ == "__main__":
    main()



