from http.server import BaseHTTPRequestHandler, HTTPServer
import ntplib
import time
import threading
import pyaudio
import wave


def play_sound(play_time):
    dt = play_time - (time.time() + time_offset)
    time.sleep(dt)
    print(time.time() + time_offset)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    f.rewind()
    print(time.time() + time_offset)
    mutex.release()
    return


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        result = mutex.acquire(False)
        if result:
            time_now = time.time() + time_offset + 0.2
            tt = '%d' % (time_now * 1000)
            t = threading.Thread(target=play_sound, args=[time_now])
            # t.setDaemon(True)
            t.start()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(tt.encode(encoding="ascii"))
        else:
            self.send_response(200)
            self.end_headers()
            tt = "-1"
            self.wfile.write(tt.encode(encoding="ascii"))
        return


def run():
    port = 8000
    print('starting server, port', port)

    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('running server...')
    httpd.serve_forever()

chunk = 1024

# open a wav format music
f = wave.open("PNformal.wav", "rb")
# instantiate PyAudio
p = pyaudio.PyAudio()
# open stream
stream = p.open(
    format=p.get_format_from_width(f.getsampwidth()),
    channels=f.getnchannels(),
    rate=f.getframerate(),
    output=True)
c = ntplib.NTPClient()
response = c.request('202.120.2.101')
time_offset = response.offset
mutex = threading.Lock()
run()

stream.stop_stream()
stream.close()
print('stopping server...')
# close PyAudio
p.terminate()