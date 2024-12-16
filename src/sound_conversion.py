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
from src.audio import *
from src.pca_computation import *
import os
from src.cosine_similarity import *

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
    for name in os.listdir(path_folder) :
        path_file = os.path.join(path_folder, name)
        if name.lower().endswith(('.mid', '.midi')) :
            res.append(convert_sound(path_file))
    return res

def retrieval(folder: str, query: str) -> list[tuple[str, float]]:
    songs_data = data_sound(folder)
    query_data = convert_sound(query)
    names = []
    for name in os.listdir(folder) :
        path_file = os.path.join(folder, name)
        if name.lower().endswith(('.mid', '.midi')) :
            names.append(path_file)
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
        e = e + label[i-1]
    atb_basis = get_keigen(matrix_atb)
    rtb_basis = get_keigen(matrix_rtb)
    ftb_basis = get_keigen(matrix_ftb)
    matrix_atb = multiply(matrix_atb, atb_basis)
    matrix_rtb = multiply(matrix_rtb, rtb_basis)
    matrix_ftb = multiply(matrix_ftb, ftb_basis)
    query_atb = multiply(query_data.ATB, atb_basis)
    query_rtb = multiply(query_data.RTB, rtb_basis)
    query_ftb = multiply(query_data.FTB, ftb_basis)
    similarity = [(i, 0) for i in range(len(matrix_atb))]
    for i, t in enumerate(similarity):
        idx, sim = t
        named = False
        for j, n in enumerate(label):
            if t[0] >= n:
                similarity[i] = (names[j-1], sim)
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
    r = retrieval(".", "./EspanjaPrelude.mid")
    for e in r:
        print(e)
