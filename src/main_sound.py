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
from src.normalisasi_histogram import *
from src.cosine_similarity import *
from src.retrival_output import *

def website_information(query : list[float] , type : str , database : str) -> list[str] :
    # DESKRIPSI LOKAL
    # Mengembalikan array of string (file name) ke website.

    # KAMUS LOKAL
    # query : list of float
    # matrix : matrix of float
    # names : list of string
    # data : list of tuple of integer and float
    # type , database : string

    # ALGORITMA LOKAL
    data = []
    if (type == "picture") :
        matrix = data_picture(database)
        data = jarak_euclidean(query , matrix)
    else :
        matrix = data_sound(database)
        data = cosine_function(query , matrix)
    names = array_names(data , type , database)
    return names

def terminal_information(query : list[float] , type : str , database : str) -> None :
    # DESKRIPSI LOKAL
    # Fungsi untuk melakukan proses pencarian informasi dan melempar ke tipe fungsi output yang bersesuaian.

    # KAMUS LOKAL
    # query : list of float
    # matrix : matrix of float
    # type , database , audio_type : string

    # ALGORITMA LOKAL
    if (type == "picture") :
        matrix = data_picture(database)
    else :
        matrix = data_sound(database)
    audio_type = "Waveform"
    information_retrival(query , matrix , type , database , audio_type)