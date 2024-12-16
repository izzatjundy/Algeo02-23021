# PROGRAM K01-GeprekMumbul-F08

# IDENTITAS
# Kelompok     : 01 - Geprek Mumbul
# NIM/Nama - 1 : 13523021 - Muhammad Raihan Nazhim Oktana
# NIM/Nama - 2 : 13523044 - Muhammad Luqman Hakim
# NIM/Nama - 3 : 13523092 - Muhammad Izzat Jundy
# Instansi     : Sekolah Teknik Elektro dan Informatika (STEI) Institut Teknologi Bandung (ITB)
# Jurusan      : Teknik Informatika (IF)
# Nama File    : retrieval_output.py
# Topik        : Tugas Besar 2 Aljabar Linier dan Geometri 2024 (IF2123-24)
# Tanggal      : Kamis, 12 Desember 2024
# Deskripsi    : Subprogram F08 - retrieval & Output
# PJ F08       : 13523021 - Muhammad Raihan Nazhim Oktana

# KAMUS
# picture_index , sound_index : function
# information_retrieval , display_output , display_sound , array_names : procedure

# ALGORITMA
import os
import mido
import librosa
import librosa.display
import matplotlib.pyplot as plt
from PIL import Image
from similarity_computation import *
from cosine_similarity import *

def picture_index(folder_path : str , index : int) -> tuple[str , str] :
    # DESKRIPSI LOKAL
    # Fungsi untuk mengambil path dan name dari file picture pada indeks yang diinginkan.

    # KAMUS LOKAL
    # folder , images : list of string
    # file , name , path , folder_path : string
    # index : integer

    # ALGORITMA LOKAL
    folder = os.listdir(folder_path)
    images = []
    for file in folder :
        if (file.lower().endswith(('.jpg' , '.png' , '.jpeg'))) :
            images.append(file)
    name = images[index]
    path = os.path.join(folder_path , name)
    return (path , name)

def sound_index(folder_path : str , index : int) -> tuple[str , str] :
    # DESKRIPSI LOKAL
    # Fungsi untuk mengambil path dan name dari file sound pada indeks yang diinginkan.

    # KAMUS LOKAL
    # folder , sounds : list of string
    # file , name , path , folder_path : string
    # index : integer

    # ALGORITMA LOKAL
    folder = os.listdir(folder_path)
    sounds = []
    for file in folder :
        if (file.lower().endswith(('.mid'))) :
            sounds.append(file)
    name = sounds[index]
    path = os.path.join(folder_path , name)
    return (path , name)

def display_audio(path_file : str , audio_type : str) -> None :
    # DESKRIPSI LOKAL
    # Fungsi untuk melakukan display audio yang dimasukkan.

    # KAMUS LOKAL
    # path_file , audio_type : string

    # ALGORITMA LOKAL
    if (audio_type == "Waveform") :
        (y , sr) = librosa.load(path_file)
        plt.figure(figsize = (12 , 4))
        librosa.display.waveshow(y , sr = sr)
        plt.title("Waveform")
        plt.xlabel("Time (second)")
        plt.ylabel("Amplitudo")
        plt.show()
    elif (audio_type == "Spectrogram") :
        (y , sr) = librosa.load(path_file)
        s = librosa.stft(y)
        s_db = librosa.amplitude_to_db(abs(s))
        plt.figure(figsize=(12 , 4))
        librosa.display.specshow(s_db , sr = sr , x_axis = 'time' , y_axis = 'log' , cmap = 'viridis')
        plt.title("Spectrogram")
        plt.colorbar(format = "%+2.0f dB")
        plt.xlabel("Time (second)")
        plt.ylabel("Frequency (Hz)")
        plt.show()
    else :
        print("Tipe Audio Tidak Valid.")

def information_retrieval(query : list[float] , matrix : list[list[float]] , type : str , database : str , audio_type : str) -> None :
    # DESKRIPSI LOKAL
    # Fungsi untuk melakukan proses pencarian informasi dan melempar ke tipe fungsi output yang bersesuaian.

    # KAMUS LOKAL
    # query : list of float
    # matrix : matrix of float
    # data : list of tuple of integer and float
    # type , database , audio_type : string

    # ALGORITMA LOKAL
    if (type == "picture") :
        data = jarak_euclidean(query , matrix)
    else :
        data = cosine_function(query , matrix)
    audio_type = "Waveform"
    return display_output(data , type , database , audio_type)

def array_names(data : list[tuple[int , float]] , type : str , database : str) -> list[str] :
    # DESKRIPSI LOKAL
    # Fungsi untuk mengembalikan kumpulan nama file hasil pencarian yang telah terurut.

    # KAMUS LOKAL
    # data : list of tuple of integer and float
    # type , database , name : string
    # res : list of string
    # size : integer
    # i : integer (index)

    # ALGORITMA LOKAL
    size = len(data)
    res = ["" for i in range (size)]
    if (type == "picture") :
        for i in range (len(data)) :
            (_ , name) = picture_index(database , data[i][0] - 1)
            res[i] = name
    else :
        for i in range (len(data)) :
            (_ , name) = sound_index(database , data[i][0] - 1)
            res[i] = name
    return res

def display_output(data : list[tuple[int , float]] , type : str , database : str , audio_type : str) -> None :
    # DESKRIPSI LOKAL
    # Fungsi untuk menampilkan output berupa urutan hasil query yang tepat ke layar.

    # KAMUS LOKAL
    # data : list of tuple of integer and float
    # type , database , path , name , audio_type : string

    # ALGORITMA LOKAL
    if (type == "picture") :
        print("Berikut adalah daftar informasi gambar yang serupa :")
        for i in range (len(data)) :
            (path , name) = picture_index(database , data[i][0] - 1)
            print(f"{i + 1}. {name}")
            Image.open(path)
    else :
        print("Berikut adalah daftar informasi suara yang serupa :")
        for i in range (len(data)) :
            (path , name) = sound_index(database , data[i][0] - 1)
            print(f"{i + 1}. {name}")
            display_audio(path , audio_type)