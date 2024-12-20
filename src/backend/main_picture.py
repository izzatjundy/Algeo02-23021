# PROGRAM K01-GeprekMumbul-F09

# IDENTITAS
# Kelompok     : 01 - Geprek Mumbul
# NIM/Nama - 1 : 13523021 - Muhammad Raihan Nazhim Oktana
# NIM/Nama - 2 : 13523044 - Muhammad Luqman Hakim
# NIM/Nama - 3 : 13523092 - Muhammad Izzat Jundy
# Instansi     : Sekolah Teknik Elektro dan Informatika (STEI) Institut Teknologi Bandung (ITB)
# Jurusan      : Teknik Informatika (IF)
# Nama File    : main_picture.py
# Topik        : Tugas Besar 2 Aljabar Linier dan Geometri 2024 (IF2123-24)
# Tanggal      : Senin, 16 Desember 2024
# Deskripsi    : Subprogram F09 - Main Picture
# PJ F09       : 13523021 - Muhammad Raihan Nazhim Oktana

# KAMUS
# website_information , terminal_information : procedure

# ALGORITMA
from backend.picture_conversion import *
from backend.sound_conversion import *
from backend.data_centering import *
from backend.pca_computation import *
from backend.similarity_computation import *
from backend.retrieval_output import *

def website_information(query : str , type : str , database : str) -> list[tuple[str , float]] :
    # DESKRIPSI LOKAL
    # Mengembalikan array of string (file name) ke website.

    # KAMUS LOKAL
    # res : list of tuple of string and float
    # list_query , avg , percent : list of float
    # matrix : matrix of float
    # data : list of tuple of integer and float
    # type , database , query : string
    # size : integer
    # i : integer (index)

    # ALGORITMA LOKAL
    data = []
    if (type == "picture") :
        matrix = data_picture(database)
        if (len(matrix) > 1) :
            avg = find_average(matrix)
            matrix = data_centering(matrix)
            list_query = convert_picture(query)
            size = len(list_query)
            for i in range (size) :
                list_query[i] = list_query[i] - avg[i]
            (data , percent) = jarak_euclidean(list_query , matrix)
            res = array_names_percents(data , percent , type , database)
            return res
        else :
            return data

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
        if (len(matrix) > 1) :
            avg = find_average(matrix)
            matrix = data_centering(matrix)
            list_query = convert_picture(query)
            size = len(list_query)
            for i in range (size) :
                list_query[i] = list_query[i] - avg[i]
            information_retrival(list_query , matrix , type , database , audio_type)
        else :
            print("Error : Database terlalu sedikit, minimal ada 2 buah data.")