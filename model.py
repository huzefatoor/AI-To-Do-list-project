# Project Overview: 
# We will first create an audio file. From there, it needs to be sent via the API, 
# which in a few calls we can have transcribed and pulled back to be read. 
# However, I did this in two separate files to try to have it somewhat dynamic. 
# To help with reusability, all of my API calls were captured into a class that’ll be the first file we’ll write. 
# The second file will be the more specific code that will create the audio file, 
# make the necessary calls to the API via the class, save it into the DB, and read the results as well.

import requests
import sys


class speech_to_text:
    """
    """

    def __init__(self, api_key):
        self.endpoint = "https://api.assemblyai.com/app"
        self.header = {
            "authorization": api_key
        }

    def upload_file(self, file):
        response = requests.post(f"{self.endpoint}upload", headers=self.header, data=self.__read_file(file))
        return response.json()
    
    def submit_audio(self, uploaded_file):
        self.header["content-type"] = "application/json"

        json = {
            "audio_url": uploaded_file,
            "punctuate": True,
            "format_text": True
        }

        url = f"{self.endpoint}transcript"

        response = requests.post(url, json=json, headers=self.header)

        return response.json()
    
    def get_text(self, transcript_id):
        url = f"{self.endpoint}transcript/{transcript_id}"

        response = requests.get(url, headers=self.header)

        return response.json()
    
    def __read_file(self, filename, chunk_size=5242880):
        print(filename)
        with open(filename, 'rb') as file:
            while True:
                data = file.read(chunk_size)
                if not data:
                    return
                yield data


    def list_transcripts(self, limit = 200, status = "completed"):
        self.header["content-type"] = "application/json"

        url = f"{self.endpoint}transcript?{limit}/{status}"

        response = requests.get(url, headers=self.header)

        return response.json()
    
    def remove_transcript(self, transcript_id):
     url = f"{self.endpoint}transcript/{transcript_id}"

     response = requests.delete(url, headers=self.header)

     return response.json()
    
    