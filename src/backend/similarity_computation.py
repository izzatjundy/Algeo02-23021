# PROGRAM K01-GeprekMumbul-F05

# IDENTITAS
# Kelompok     : 01 - Geprek Mumbul
# NIM/Nama - 1 : 13523021 - Muhammad Raihan Nazhim Oktana
# NIM/Nama - 2 : 13523044 - Muhammad Luqman Hakim
# NIM/Nama - 3 : 13523092 - Muhammad Izzat Jundy
# Instansi     : Sekolah Teknik Elektro dan Informatika (STEI) Institut Teknologi Bandung (ITB)
# Jurusan      : Teknik Informatika (IF)
# Nama File    : similarity_computation.py
# Topik        : Tugas Besar 2 Aljabar Linier dan Geometri 2024 (IF2123-24)
# Tanggal      : Senin, 16 Desember 2024
# Deskripsi    : Subprogram F05 - Similarity Computation
# PJ F05       : 13523021 - Muhammad Raihan Nazhim Oktana

# KAMUS
# proyeksi_query , count_function , jarak_euclidean : function
# merge , merge_sort : procedure

# ALGORITMA
from math import sqrt , exp
from backend.data_centering import *
from backend.pca_computation import *

def proyeksi_query(query : list[float] , k_eigen_vector : list[list[float]] , matrix : list[list[float]]) -> list[list[float]] :
    # DESKRIPSI LOKAL
    # Membuat fungsi untuk memproyeksikan query ke ruang komponen utama (PCA).

    # KAMUS LOKAL
    # query , avg : list of float
    # matrix , matrix_query , k_eigen_vector : matrix of float
    # size : integer
    # i , j : integer (index)

    # ALGORITMA LOKAL
    avg = find_average(matrix)
    size = len(query)
    matrix_query = [[0.0 for j in range (size)] for i in range (1)]
    for i in range (size) :
        matrix_query[0][i] = query[i] - avg[i]
    res = multiply(matrix_query , k_eigen_vector)
    return res

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
    
def count_function(query : list[float] , data : list[float]) -> float :
    # DESKRIPSI LOKAL
    # Fungsi untuk menghitung proyeksi jarak euclidian.

    # KAMUS LOKAL
    # query , data : list of float
    # sumq , res : float
    # i : integer (index)

    # ALGORITMA LOKAL
    sumq = 0.0
    size = len(query)
    for i in range (size) :
        sumq = sumq + (query[i] - data[i]) * (query[i] - data[i])
    res = sqrt(sumq)
    return res

def minimum_similarity(data : list[list[float]] , target : float) -> tuple[list[list[float]] , list[float]] :
    # DESKRIPSI LOKAL
    # Membatasi similaritas diatas target yang ditentukan untuk 

    # KAMUS LOKAL
    # data , res : matrix of float
    # target , bar , count : float
    # size : integer
    # i : integer (index)

    # ALGORITMA LOKAL
    res = []
    size = len(data)
    bar = data[size - 1][1]
    percent = []
    for i in range (size) :
        count = 1 - data[i][1] / bar
        if (count >= target) :
            res.append(data[i])
            percent.append(count)
    return (res , percent)

def jarak_euclidean(query : list[float] , matrix : list[list[float]]) -> tuple[list[tuple[int , float]] , list[float]] :
    # DESKRIPSI LOKAL
    # Menghitung jarak euclidean antara query dengan setiap data di database dan mengurutkannya.

    # KAMUS LOKAL
    # matrix , matrix_z , k_eigen_vector , matrix_query : matrix of float
    # data , distance : list of tuple of integer and float
    # query : list of float
    # size : integer
    # i : integer (index)

    # ALGORITMA LOKAL
    k_eigen_vector = get_keigen(matrix)
    matrix_z = get_z(matrix , k_eigen_vector)
    matrix_query = proyeksi_query(query , k_eigen_vector , matrix)
    size = len(matrix_z)
    distance = [[0 , 0.0] for i in range (size)]
    for i in range (size) :
        distance[i][0] = i + 1
        distance[i][1] = count_function(matrix_query[0] , matrix_z[i])
    target = 0.55
    data = merge_sort(distance)
    res , percent = minimum_similarity(data , target)
    return (res , percent)