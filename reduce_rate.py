import os
from pydub import AudioSegment as AS
from pydub.playback import play
import sys
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('--source', required=True,
                help='source directory where all the song files are')
ap.add_argument('--dest', required=True,
                help='destination directory where the reduced rate songs should go')
ap.add_argument('--frame_rate', type=int, required=True,
                help='new frame rate of songs')
args = ap.parse_args()

src = args.source
dest = args.dest
frame_rate = args.frame_rate

if not dest.endswith("/"):
    dest += "/"
if not src.endswith("/"):
    src += "/"

if not os.path.isdir(dest):
    os.system("mkdir " + dest)

count = 0
for root, dirs, files in os.walk(src):
    f = [root+'/'+i for i in files if i.endswith(".mp3")]
    for song in f:
        if os.path.isfile(song.replace(src, dest)):
            continue
        if not os.path.isdir(root.replace(src, dest)):
            os.system("mkdir " + root.replace(src, dest))
        try:
            music = AS.from_mp3(song).set_frame_rate(frame_rate)
            music.export(song.replace(src, dest), format='mp3')
        except:
            continue
    print(root)
