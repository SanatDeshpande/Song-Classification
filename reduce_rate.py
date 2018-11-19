import os
from pydub import AudioSegment as AS
from pydub.playback import play




for root, dirs, files in os.walk("./data"):
    f = [root+'/'+i for i in files if i.endswith(".mp3")]

    for song in f:
        if os.path.isfile(song.replace("data", "low_data")):
            continue
        if not os.path.isdir(root.replace("./data", "./low_data")):
            os.system("mkdir " + root.replace("./data", "./low_data"))
        try:
            music = AS.from_mp3(song)
            music.export(song.replace("./data", "./low_data"), format='mp3', bitrate='1k')
        except:
            continue
    print(root)
