import pyaudio
import threading 
import wave

status = False

def wire_audio():
    if (status == False):
        print ("status stopped")
        return
    CHUNK = 1024
    WIDTH = 2
    CHANNELS = 2
    FORMAT = pyaudio.paInt16
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)
    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * 5)):
        data = stream.read(CHUNK)
        frames.append(data)
        stream.write(data, CHUNK)

    print("* done")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return

while True:
    command = input('command? ').strip()
    if command == 'start':
        status = True
        threading.Thread(wire_audio()).start()
    elif command == 'stop':
        status = False
    elif command == 'quit':
        break
    else:
        print ('Invalid Command.')
  
