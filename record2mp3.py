# import required libraries
import sounddevice as sd
import scipy.io.wavfile
from pydub import AudioSegment
import io
from threading import Thread
from queue import Queue

CHUNK_SIZE = 300  #seconds

total_cnt=0
# producer task
def producer(q, seconds, freq):
    print('Producer: Running')
    # generate items
    while seconds > 0:
        chunk=CHUNK_SIZE
        if seconds< CHUNK_SIZE:
            chunk=seconds
        seconds-=chunk
        recording = sd.rec(int(chunk * freq), samplerate=freq, channels=2)

        # Record audio for the given number of seconds
        sd.wait()
        wav_io = io.BytesIO()
        scipy.io.wavfile.write(wav_io, freq, recording)
        wav_io.seek(0)
        q.put(wav_io)

    q.put(None)
    print('Producer: Done')


# consumer task
def consumer(q, filename):
    print('Consumer: Running')
    # consume items
    global total_cnt
    while True:
        item = q.get()
        if item==None:
            break

        sound = AudioSegment.from_wav(item)
        with open(filename + f"_{total_cnt:03}"+".mp3", 'wb') as af:
            sound.export(
                af,
                format='mp3',
                codec='mp3',
                bitrate='160000',
            )
        total_cnt+=1
    # all done
    print('Consumer: Done')

if __name__ == '__main__':

    import sys

    if len(sys.argv) < 3:
        print("python record2mp3.py filename_prefix duration_in_secconds")
        exit(1)
    filename=sys.argv[1]
    seconds=int(sys.argv[2])
    freq=44100
    print(filename, seconds, freq)
    queue = Queue()

    # start the consumer
    consumer = Thread(target=consumer, args=(queue, filename,))
    consumer.start()
    # start the producer
    producer = Thread(target=producer, args=( queue, seconds, freq))
    producer.start()
    # wait for all threads to finish
    producer.join()
    consumer.join()
    print(f"recording done to {filename}_ddd.mp3, total {total_cnt} files.")
