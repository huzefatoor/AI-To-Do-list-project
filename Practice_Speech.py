import assemblyai
import speech_recognition as sr
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
from gtts import gTTS
import playsound
import os

# Set up AssemblyAI
assemblyai.api_key = 'a906f30674f84cd4b2bf9b6b55c367db'

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Load Hugging Face GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

def transcribe_audio(audio_file):
    # Upload audio file to AssemblyAI
    headers = {'authorization': assemblyai.api_key}
    response = assemblyai.transcribe(audio_file, headers=headers)
    return response['text']

def generate_response(prompt):
    responses = generator(prompt, max_length=150, num_return_sequences=1)
    return responses[0]['generated_text']

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    playsound.playsound("response.mp3")
    os.remove("response.mp3")

def main():
    while True:
        # Capture audio from microphone
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        # Save audio to a file
        with open("audio.wav", "wb") as f:
            f.write(audio.get_wav_data())

        # Transcribe audio
        print("Transcribing audio...")
        transcribed_text = transcribe_audio("audio.wav")
        print(f"User: {transcribed_text}")

        # Generate response using GPT-2
        response_text = generate_response(transcribed_text)
        print(f"AI: {response_text}")

        # Speak the response
        speak_text(response_text)

if __name__ == "__main__":
    main()
