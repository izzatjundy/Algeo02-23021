# PROGRAM K01-GeprekMumbul-F01

# IDENTITAS
# Kelompok     : 01 - Geprek Mumbul
# NIM/Nama - 1 : 13523021 - Muhammad Raihan Nazhim Oktana
# NIM/Nama - 2 : 13523044 - Muhammad Luqman Hakim
# NIM/Nama - 3 : 13523092 - Muhammad Izzat Jundy
# Instansi     : Sekolah Teknik Elektro dan Informatika (STEI) Institut Teknologi Bandung (ITB)
# Jurusan      : Teknik Informatika (IF)
# Nama File    : picture_conversion.py
# Topik        : Tugas Besar 2 Aljabar Linier dan Geometri 2024 (IF2123-24)
# Tanggal      : Kamis, 12 Desember 2024
# Deskripsi    : Subprogram F01 - Picture Conversion
# PJ F01       : 13523021 - Muhammad Raihan Nazhim Oktana

# KAMUS
# convert_picture , data_picture : procedure

# ALGORITMA
import os
from PIL import Image

def convert_picture(path : str) -> list[float] :
    # SPESIFIKASI LOKAL
    # Melakukan konversi gambar menjadi pixel RGB dengan bantuan PIL, lalu menyimpan hasil intensitasnya pada list of float.

    # KAMUS LOKAL
    # img : ImageFile
    # pixels : list of tuple of integer
    # res : list of float
    # path : string
    # size : integer
    # i : integer (index)

    # ALGORITMA LOKAL
    img = Image.open(path)
    img = img.resize((512 , 512) , Image.ANTIALIAS)
    img = img.convert('RGB')
    pixels = list(img.getdata())
    size = 512 * 512
    res = [0.0 for i in range (size)]
    for i in range (size) :
        res[i] = 0.2989 * pixels[i][0] + 0.5870 * pixels[i][1] + 0.1140 * pixels[i][2]
    return res

def data_picture(path_folder : str) -> list[list[float]] :
    # SPESIFIKASI LOKAL
    # Melakukan konversi semua file dalam suatu folder database menjadi list of vektor (list of float) / matrix of float.

    # KAMUS LOKAL
    # res : matrix of float
    # temp : list of float
    # path_folder , path_file , name : string

    # ALGORITMA LOKAL
    res = []
    for name in os.listdir(path_folder) :
        path_file = os.path.join(path_folder, name)
        if name.lower().endswith(('.png' , '.jpg' , '.jpeg')) :
            temp = convert_picture(path_file)
            res.append(temp)
    return res