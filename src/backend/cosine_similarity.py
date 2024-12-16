# PROGRAM K01-GeprekMumbul-F07

# IDENTITAS
# Kelompok     : 01 - Geprek Mumbul
# NIM/Nama - 1 : 13523021 - Muhammad Raihan Nazhim Oktana
# NIM/Nama - 2 : 13523044 - Muhammad Luqman Hakim
# NIM/Nama - 3 : 13523092 - Muhammad Izzat Jundy
# Instansi     : Sekolah Teknik Elektro dan Informatika (STEI) Institut Teknologi Bandung (ITB)
# Jurusan      : Teknik Informatika (IF)
# Nama File    : cosine_similarity.py
# Topik        : Tugas Besar 2 Aljabar Linier dan Geometri 2024 (IF2123-24)
# Tanggal      : Kamis, 12 Desember 2024
# Deskripsi    : Subprogram F07 - Cosine Similarity
# PJ F07       : 13523021 - Muhammad Raihan Nazhim Oktana

# KAMUS
# cosine_function , merge , merge_sort : function
# similarity_cosine : procedure

# ALGORITMA
from math import sqrt

def cosine_function(vec1 : list[float] , vec2 : list[float]) -> float :
    # DESKRIPSI LOKAL
    # Membuat perhitungan fungsi cosinus seperti pada spesifikasi.

    # KAMUS LOKAL
    # vec1 , vec2 : list of float
    # size , size1 , size2 , sum_a2 , sum_b2 , sum_ab : integer
    # res : float
    # i : integer (index)

    # ALGORITMA LOKAL
    size1 = len(vec1)
    size2 = len(vec2)
    size = min(size1 , size2)
    sum_a2 = 0
    sum_b2 = 0
    sum_ab = 0
    for i in range (size) :
        sum_a2 = sum_a2 + (vec1[i] ** 2)
        sum_b2 = sum_b2 + (vec2[i] ** 2)
        sum_ab = sum_ab + (vec1[i] * vec2[i])
    if sum_a2 == 0 or sum_b2 == 0:
        return 0 
    res = sum_ab / (sqrt(sum_a2) * sqrt(sum_b2))
    return (res + 1) / 2

def merge(left : list[tuple[int , float]] , right : list[tuple[int , float]]) -> list[tuple[int , float]] :
    # DESKRIPSI LOKAL
    # Fungsi untuk menggabungkan 2 list, sebuah fungsi antara untuk merge sort.

    # KAMUS LOKAL
    # data , left , right , res : list of tuple of integer and float
    # i , j : integer (index)

    # ALGORITMA LOKAL
    res = []
    i = 0
    j = 0
    while ((i < len(left)) and (j < len(right))) :
        if (left[i][1] < right[j][1]) :
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

def merge_sort(data : list[tuple[int , float]]) -> list[tuple[int , float]] :
    # DESKRIPSI LOKAL
    # Fungsi untuk melakukan merge sort dengan time complexity O(n log(n)).

    # KAMUS LOKAL
    # data , left , right , res_left , res_right : list of tuple of integer and float
    # mid : integer

    # ALGORITMA LOKAL
    if (len(data) <= 1) :
        return data
    else :
        mid = len(data) // 2
        left = data[:mid]
        right = data[mid:]
        res_left = merge_sort(left)
        res_right = merge_sort(right)
        return merge(res_left , res_right)

def similarity_cosine(query : list[float] , matrix : list[list[float]]) -> list[tuple[int , float]] :
    # DESKRIPSI LOKAL
    # Mengurutkan kemiripan antara query dengan setiap data pada database.

    # KAMUS LOKAL
    # value , data : list of tuple of integer and float
    # query : list of float
    # matrix : matrix of float

    # ALGORITMA LOKAL
    size = len(matrix)
    value = [[0 , 0.0] for i in range (size)]
    for i in range (size) :
        value[i][0] = i + 1
        value[i][1] = cosine_function(query , matrix[i])
    data = merge_sort(value)
    return data
