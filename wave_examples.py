# Audio file formats
# .mp3 
# .flac 
# .wav

import wave

# Audio signal parameters 
# - number of channels 
# - sample width 
# - framerate/sample_rate 
# - number of frames 
# - values of frame

# loads audio file with wave.open()
obj = wave.open("output.mp3", "rb")

# print parameters
print(obj.getframerate())
print(obj.getnchannels())
print(obj.getnframes())

t_audio = obj.getnframes()/obj.getframerate()
