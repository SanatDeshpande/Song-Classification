import numpy as np
from pydub import AudioSegment as AS
from pydub.playback import play
import os
import json
import csv
import pickle
import argparse
from collections import defaultdict

ap = argparse.ArgumentParser()
ap.add_argument('--song_dir', required=True,
                help='source directory where all the song files are')
ap.add_argument('--metadata_file', required=True,
                help='location of raw_tracks.csv')
args = ap.parse_args()


#chops up songs into fixed length segments returns accompanying label array (one_hot encoded)
def chop_and_label(songfile, labels_to_one_hot, songs_to_label, chop):
    track_id = int(songfile.split("/")[-1].split(".")[0])
    song = AS.from_mp3(songfile)
    song_array = []
    label_array = []
    for i in range(0, int(len(song)/(chop * 1000))):
        raw = song[i*1000*chop:(i+1)*1000*chop].raw_data
        if len(raw) != 96000:
            continue
        song_array.append(list(raw))
        genre_label = songs_to_label[track_id]
        label_array.append(labels_to_one_hot[genre_label])
    return song_array, label_array

songs_to_label = {}
label_to_name = {} #human readability
label_to_frequency = defaultdict(int)
labels = set([])
with open(args.metadata_file) as f:
    data = csv.DictReader(f)
    for d in data:
        try:
            genre = json.loads(d["track_genres"].replace("\'", "\""))[0]
        except:
            continue
        songs_to_label[int(d['track_id'])] = int(genre['genre_id'])
        label_to_name[int(genre['genre_id'])] = genre['genre_title']
        labels.add(int(genre['genre_id']))



#songs to one_hot labels
labels_to_one_hot = {}
for count, i in enumerate(labels):
    #one_hot = np.zeros(len(labels))
    #one_hot[count] = 1
    labels_to_one_hot[i] = count


path = args.song_dir
files = []
for r, d, f in os.walk(path):
    paths = [r + "/" + i for i in f if i.endswith(".mp3")]
    files += paths

# songs = []
# targets = []
#test = set([])

#get top n most frequent labels
for count, f in enumerate(files):
    track_id = int(f.split("/")[-1].split(".")[0])
    genre_label = songs_to_label[track_id]
    final_label = labels_to_one_hot[genre_label]
    label_to_frequency[final_label] += 1
label_to_frequency = [(key, value) for key, value in label_to_frequency.items()]
label_to_frequency.sort(key=lambda k: k[1])
acceptable_labels = [i[0] for i in label_to_frequency[-5:]]

for count, f in enumerate(files):
    #reduce categorization problem
    track_id = int(f.split("/")[-1].split(".")[0])
    genre_label = songs_to_label[track_id]
    final_label = labels_to_one_hot[genre_label]
    if final_label not in acceptable_labels:
        continue
    #end reduce categorization

    songs, targets = chop_and_label(f, labels_to_one_hot, songs_to_label, 3)

    # songs += s
    # targets += t

    songs = np.asarray(songs, dtype=np.float)
    targets = np.asarray(targets, dtype=np.float)
    with open("songs.data", "ab") as f:
        songs.tofile(f)
    with open("labels.data", "ab") as f:
        targets.tofile(f)
    print(count, label_to_name[final_label], final_label)
