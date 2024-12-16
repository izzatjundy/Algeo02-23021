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
    return s / n

def normalize(l):
    n = sum(l)
    for i, e in enumerate(l):
        l[i] = e / n

def absolute_tone_histogram(midi_file):
    notes = [0.0 for i in range(128)]
    histogram = []
    beat_len = midi_file.ticks_per_beat
    beat_count = 0
    next_msg_idx = 0
    next = False
    temp = 0
    while (next_msg_idx < len(midi_file.tracks[1])):
        for i, msg in enumerate(midi_file.tracks[1][next_msg_idx:]):
            if msg.type == 'end_of_track':
                next_msg_idx = len(midi_file.tracks[1])
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
                result = [notes[avg_note + i - 12] for i in range(25)]
                if avg_note > 12:
                    result[0] += sum(notes[:avg_note - 13])
                if avg_note < 115:
                    result[24] += sum(notes[avg_note + 13:])
                normalize(result)
                histogram.append(result)
                notes = [0.0 for i in range(256)]
                beat_count = 0
                break
    return histogram

def relative_tone_histogram(midi_file):
    notes = [0.0 for i in range(256)]
    histogram = []
    beat_len = midi_file.ticks_per_beat
    beat_count = 0
    next_msg_idx = 0
    for msg in midi_file.tracks[1]:
        if msg.type != 'note_on' and msg.type != 'note_off':
            next_msg_idx += 1
        else:
            break
    next = False
    temp = 0
    while (next_msg_idx < len(midi_file.tracks[1])):
        prev_note = midi_file.tracks[1][next_msg_idx].note
        for i, msg in enumerate(midi_file.tracks[1][next_msg_idx+1:]):
            if msg.type == 'end_of_track':
                next_msg_idx = len(midi_file.tracks[1])
                break
            if msg.type == 'note_on' and msg.velocity > 0:
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
                result = [notes[avg_note + i - 12] for i in range(25)]
                normalize(result)
                histogram.append(result)
                notes = [0.0 for i in range(256)]
                beat_count = 0
                break
    return histogram

def first_tone_histogram(midi_file):
    notes = [0.0 for i in range(256)]
    histogram = []
    beat_len = midi_file.ticks_per_beat
    beat_count = 0
    next_msg_idx = 0
    for msg in midi_file.tracks[1]:
        if msg.type != 'note_on' and msg.type != 'note_off':
            next_msg_idx += 1
        else:
            break
    next = False
    temp = 0
    while (next_msg_idx < len(midi_file.tracks[1])):
        prev_note = midi_file.tracks[1][next_msg_idx].note
        for i, msg in enumerate(midi_file.tracks[1][next_msg_idx+1:]):
            if msg.type == 'end_of_track':
                next_msg_idx = len(midi_file.tracks[1])
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
                result = [notes[avg_note + i - 12] for i in range(25)]
                normalize(result)
                histogram.append(result)
                notes = [0.0 for i in range(256)]
                beat_count = 0
                break
    return histogram
if __name__ == "__main__":
    m = md.MidiFile("EspanjaPrelude.mid")
    histogram = np.array(absolute_tone_histogram(m))
    # print(len(histogram))
    # for e in histogram:
    #     print(e)
    histogram2 = np.array(relative_tone_histogram(m))
    print(histogram2[0])
    print(type(histogram2))
    histogram3 = np.array(first_tone_histogram(m))
    print(histogram3[0])
    # for i in range (100):
    #     notes, arr, n = absolute_tone_histogram(m, start_beat=i * 4)
    #     if np.isnan(n):
    #         print(notes)
    #         print(arr)
    #         print(i)
        # print(n)
