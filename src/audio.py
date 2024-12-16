import mido as md
import numpy as np
import typing

WINDOW_SIZE = 20

def weighted_average(l):
    n = 0
    s = 0
    for i, e in enumerate(l):
        n += e
        s += e * i
    if s == 0:
        return 0
    return s / n

def normalize(l):
    n = sum(l)
    if n == 0:
        return
    for i, e in enumerate(l):
        l[i] = e / n

def absolute_tone_histogram(midi_file):
    histogram = []
    beat_len = midi_file.ticks_per_beat
    for track in midi_file.tracks[0:2]:
        next_msg_idx = 0
        while (next_msg_idx < len(track)):
            notes = [0.0 for i in range(128)]
            beat_count = 0
            if track[next_msg_idx].type != 'note_on' and track[next_msg_idx].type != 'note_off':
                next_msg_idx += 1
                continue
            next = False
            for i, msg in enumerate(track[next_msg_idx:]):
                if msg.type == 'end_of_track':
                    next_msg_idx = len(track)
                    break
                if msg.type == 'note_on' and msg.velocity >= 0:
                    notes[msg.note] += msg.time / beat_len
                    notes[msg.note+1] += 0.25 * msg.time / beat_len
                    notes[msg.note+2] += 0.0625 * msg.time / beat_len
                    notes[msg.note-1] += 0.25 * msg.time / beat_len
                    notes[msg.note-2] += 0.0625 * msg.time / beat_len
                beat_count += msg.time / beat_len
                if beat_count >= 4 and not next and i == 0:
                    next_msg_idx += 1
                    next = True
                elif beat_count >= 4 and not next:
                    next_msg_idx += i
                    next = True
                if beat_count >= WINDOW_SIZE:
                    next = False
                    avg_note = int(weighted_average(notes))
                    result = [notes[avg_note + i - 6] for i in range(13)]
                    if avg_note > 6:
                        result[0] += sum(notes[:avg_note - 7])
                    if avg_note < 115:
                        result[12] += sum(notes[avg_note + 7:])
                    normalize(result)
                    histogram.append(result)
                    break
    return histogram

def relative_tone_histogram(midi_file):
    histogram = []
    beat_len = midi_file.ticks_per_beat
    for track in midi_file.tracks[0:2]:
        next = False
        next_msg_idx = 0
        while (next_msg_idx < len(track)):
            if track[next_msg_idx].type != 'note_on' and track[next_msg_idx].type != 'note_off':
                next_msg_idx += 1
                continue
            prev_note = track[next_msg_idx].note
            notes = [0.0 for i in range(256)]
            beat_count = 0
            for i, msg in enumerate(track[next_msg_idx:]):
                if msg.type == 'end_of_track':
                    next_msg_idx = len(track)
                    break
                if msg.type == 'note_on' and msg.velocity >= 0 and i > 0:
                    idx = msg.note - prev_note + 128
                    notes[idx] += 1
                    notes[idx+2] += 0.125
                    notes[idx-1] += 0.125
                    prev_note = msg.note
                beat_count += msg.time / beat_len
                if beat_count >= 4 and not next and i == 0:
                    next_msg_idx += 1
                    next = True
                elif beat_count >= 4 and not next:
                    next_msg_idx += i
                    next = True
                if beat_count >= WINDOW_SIZE:
                    next = False
                    avg_note = int(weighted_average(notes))
                    result = [notes[avg_note + i - 6] for i in range(13)]
                    normalize(result)
                    histogram.append(result)
                    break
    return histogram

def first_tone_histogram(midi_file):
    histogram = []
    beat_len = midi_file.ticks_per_beat
    for track in midi_file.tracks[0:2]:
        next = False
        next_msg_idx = 0
        while (next_msg_idx < len(track)):
            if track[next_msg_idx].type != 'note_on' and track[next_msg_idx].type != 'note_off':
                next_msg_idx += 1
                continue
            prev_note = track[next_msg_idx].note
            notes = [0.0 for i in range(256)]
            beat_count = 0
            for i, msg in enumerate(track[next_msg_idx:]):
                if msg.type == 'end_of_track':
                    next_msg_idx = len(track)
                    break
                if msg.type == 'note_on' and msg.velocity > 0:
                    idx = msg.note - prev_note + 128
                    notes[idx] += 1
                    # notes[idx+2] += 0.125
                    # notes[idx-1] += 0.125
                beat_count += msg.time / beat_len
                if beat_count >= 4 and not next and i == 0:
                    next_msg_idx += 1
                    next = True
                elif beat_count >= 4 and not next:
                    next_msg_idx += i
                    next = True
                if beat_count >= WINDOW_SIZE:
                    next = False
                    avg_note = int(weighted_average(notes))
                    result = [notes[avg_note + i - 6] for i in range(13)]
                    normalize(result)
                    histogram.append(result)
                    break
    return histogram

class AudioResult:
    def __init__(self, midi_file):
        self.ATB = absolute_tone_histogram(midi_file)
        self.RTB = relative_tone_histogram(midi_file)
        self.FTB = first_tone_histogram(midi_file)

if __name__ == "__main__":
    m = md.MidiFile("EspanjaPrelude.mid")
    histogram = np.array(absolute_tone_histogram(m))
    print(len(histogram))
    for e in histogram:
        print(e)
    histogram2 = np.array(relative_tone_histogram(m))
    print(histogram2[0])
    print(type(histogram2))
    histogram3 = np.array(first_tone_histogram(m))
    print(histogram3[0])
    for i in range (100):
        notes, arr, n = absolute_tone_histogram(m, start_beat=i * 4)
        if np.isnan(n):
            print(notes)
            print(arr)
            print(i)
        print(n)
