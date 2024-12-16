# PROGRAM K01-GeprekMumbul-F02

# IDENTITAS
# Kelompok     : 01 - Geprek Mumbul
# NIM/Nama - 1 : 13523021 - Muhammad Raihan Nazhim Oktana
# NIM/Nama - 2 : 13523044 - Muhammad Luqman Hakim
# NIM/Nama - 3 : 13523092 - Muhammad Izzat Jundy
# Instansi     : Sekolah Teknik Elektro dan Informatika (STEI) Institut Teknologi Bandung (ITB)
# Jurusan      : Teknik Informatika (IF)
# Nama File    : sound_conversion.py
# Topik        : Tugas Besar 2 Aljabar Linier dan Geometri 2024 (IF2123-24)
# Tanggal      : Kamis, 12 Desember 2024
# Deskripsi    : Subprogram F02 - Sound Conversion
# PJ F02       : 13523044 - Muhammad Luqman Hakim

# KAMUS
# convert_sound , data_sound : procedure

# ALGORITMA
import mido
from audio import *
from pca_computation import *
import os
from cosine_similarity import *
import numpy as np

def convert_sound(path : str) -> AudioResult :
    # DESKRIPSI LOKAL
    # Mengubah audio menjadi objek AudioResult
    # input:
    # path : path ke berkas audio
    # output:
    # objek hasil konversi

    # KAMUS LOKAL
    # -

    # ALGORITMA LOKAL
    return AudioResult(mido.MidiFile(path))

def data_sound(path_folder : str) -> list[AudioResult] :
    # DESKRIPSI LOKAL
    # Mengubah semua audio pada suatu folder menjadi list of AudioResult
    # input:
    # path : path ke folder audio
    # output:
    # list objek hasil konversi

    # KAMUS LOKAL
    # res : list[AudioResult]

    # ALGORITMA LOKAL
    res = []
    names = []
    for name in os.listdir(path_folder) :
        path_file = os.path.join(path_folder, name)
        if name.lower().endswith(('.mid', '.midi')) :
            res.append(convert_sound(path_file))
            names.append(name)
    return (res, names)

# def copy_matrix(mtx : list[list[float]])

def retrieval(folder: str, query: str) -> list[tuple[str, float]]:
    songs_data, names = data_sound(folder)
    query_data = convert_sound(query)
    matrix_atb = []
    matrix_rtb = []
    matrix_ftb = []
    label = []
    for e in songs_data:
        matrix_atb.extend(e.ATB)
        matrix_rtb.extend(e.RTB)
        matrix_ftb.extend(e.FTB)
        label.append(len(e.ATB))
    for i, e in enumerate(label[1:]):
        label[i+1] = e + label[i]
    print
    atb_basis = get_keigen(np.array(matrix_atb))
    rtb_basis = get_keigen(np.array(matrix_rtb))
    ftb_basis = get_keigen(np.array(matrix_ftb))
    matrix_atb = multiply(matrix_atb, atb_basis)
    matrix_rtb = multiply(matrix_rtb, rtb_basis)
    matrix_ftb = multiply(matrix_ftb, ftb_basis)
    query_atb = multiply(query_data.ATB, atb_basis)
    query_rtb = multiply(query_data.RTB, rtb_basis)
    query_ftb = multiply(query_data.FTB, ftb_basis)
    # for e in matrix_atb:
    #     print(e)
    # for e in query_atb:
    #     print(e)
    similarity = [(i, 0) for i in range(len(matrix_atb))]
    for i, t in enumerate(similarity):
        idx, sim = t
        for j, n in enumerate(label):
            if idx < n:
                similarity[i] = (names[j], sim)
                named = True
                break
        if not named:
           similarity[i] = (names[-1], sim)
    q = min(len(query_atb), len(query_ftb), len(query_rtb))
    m = min(len(matrix_atb), len(matrix_ftb), len(matrix_rtb))
    for i in range(q):
        for j in range(m):
            s = cosine_function(query_atb[i], matrix_atb[j])
            s += cosine_function(query_rtb[i], matrix_rtb[j])
            s += cosine_function(query_ftb[i], matrix_ftb[j])
            s = float(s) / 3
            idx, sim = similarity[j]
            if s > sim:
                similarity[j] = (idx, s)
    similarity = merge_sort(similarity)
    similarity.reverse()
    result = {}
    res_list = []
    for t in similarity:
        name, sim = t
        if not name in result:
            result[name] = sim
        else:
            result[name] = max(result[name], sim)
    for name in result:
        res_list.append((name, result[name]))
    return res_list

if __name__ == "__main__":
    r = retrieval(".", "AnyConv.com__spotifydown.com - Bunga Abadi.midi")
    for e in r:
        print(e)
