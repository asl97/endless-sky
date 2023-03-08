import PIL.Image
#import ffmpeg
import threading
#import typing
import queue
import os

q = queue.Queue()


def worker():
    while (work := q.get()) is not None:
        func, args = work
        func(*args)

def image(directory, f):
    # print(os.path.join(directory, f))
    try:
        with PIL.Image.open(os.path.join(directory, f), 'r') as im:
            #im2 = PIL.Image.new("1", im.size, color=0)
            #new_size = (int(im.size[0]/2+.5), int(im.size[1]/2+.5))
            im2 = im.convert('P')
            #fs = f.rsplit('.', 1)
            #im.save(os.path.join(directory, f"{fs[0]}@2x.{fs[1]}"))
            im2.save(os.path.join(directory, f))
    except Exception as E:
        print('error: ', f, E)

def wav(directory, f):
    path = os.path.join(directory, f)
    ffmpeg.input(path).output(path.replace('.wav', '.ogg')).run()
    os.remove(path)
    os.rename(path.replace('.wav', '.ogg'), path)

for directory, folders, files in os.walk('images'):
    for f in files:
        if f.endswith('.png'):# or f.endswith('.jpg'):
            q.put((image, (directory, f)))
        #if f.endswith('.wav'):
        #    q.put((wav, (directory, f)))

threads: list[threading.Thread] = []
for _ in range(8):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
    q.put(None)

for t in threads:
    t.join()
