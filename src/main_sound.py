# PROGRAM K01-GeprekMumbul-F10

# IDENTITAS
# Kelompok     : 01 - Geprek Mumbul
# NIM/Nama - 1 : 13523021 - Muhammad Raihan Nazhim Oktana
# NIM/Nama - 2 : 13523044 - Muhammad Luqman Hakim
# NIM/Nama - 3 : 13523092 - Muhammad Izzat Jundy
# Instansi     : Sekolah Teknik Elektro dan Informatika (STEI) Institut Teknologi Bandung (ITB)
# Jurusan      : Teknik Informatika (IF)
# Nama File    : main_sound.py
# Topik        : Tugas Besar 2 Aljabar Linier dan Geometri 2024 (IF2123-24)
# Tanggal      : Kamis, 12 Desember 2024
# Deskripsi    : Subprogram F10 - Main Sound
# PJ F10       : 13523021 - Muhammad Raihan Nazhim Oktana

# KAMUS
# website_information , terminal_information : procedure

# ALGORITMA
from src.picture_conversion import *
from src.sound_conversion import *
from src.data_centering import *
from src.pca_computation import *
from src.normalisasi_histogram import *
from src.similarity_computation import *
from src.cosine_similarity import *
from src.retrival_output import *

def website_information(query : str , type : str , database : str) -> list[str] :
    # DESKRIPSI LOKAL
    # Mengembalikan array of string (file name) ke website.

    # KAMUS LOKAL
    # list_query , avg : list of float
    # matrix : matrix of float
    # names : list of string
    # data : list of tuple of integer and float
    # type , database , query : string
    # size : integer
    # i : integer (index)

    # ALGORITMA LOKAL
    data = []
    if (type == "picture") :
        matrix = data_picture(database)
        avg = find_average(matrix)
        matrix = data_centering(matrix)
        list_query = convert_picture(query)
        size = len(list_query)
        for i in range (size) :
            list_query[i] = list_query[i] - avg[i]
        data = jarak_euclidean(list_query , matrix)
    else :
        matrix = data_sound(database)
        matrix = normalize_histogram(matrix)
        list_query = convert_picture(query)
        matrix_query = normalize_histogram(list_query)
        data = cosine_function(matrix_query[0] , matrix)
    names = array_names(data , type , database)
    return names

def terminal_information(query : str , type : str , database : str) -> None :
    # DESKRIPSI LOKAL
    # Fungsi untuk melakukan proses pencarian informasi dan melempar ke tipe fungsi output yang bersesuaian.

    # KAMUS LOKAL
    # list_query , avg : list of float
    # matrix , matrix_query : matrix of float
    # type , database , audio_type , query : string
    # size : integer
    # i : integer (index)

    # ALGORITMA LOKAL
    audio_type = "Waveform"
    if (type == "picture") :
        matrix = data_picture(database)
        avg = find_average(matrix)
        matrix = data_centering(matrix)
        list_query = convert_picture(query)
        size = len(list_query)
        for i in range (size) :
            list_query[i] = list_query[i] - avg[i]
        information_retrival(list_query , matrix , type , database , audio_type)
    else :
        matrix = data_sound(database)
        matrix = normalize_histogram(matrix)
        list_query = convert_picture(query)
        matrix_query = normalize_histogram(list_query)
        information_retrival(matrix_query[0] , matrix , type , database , audio_type)