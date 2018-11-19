import os
from pydub import AudioSegment as AS
from pydub.playback import play
import sys

src = sys.argv[1]
dest = sys.argv[2]
frame_rate = int(sys.argv[3])
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
    if count > 1:
        break
    count += 1
