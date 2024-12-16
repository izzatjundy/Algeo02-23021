# PROGRAM K01-GeprekMumbul-F03

# IDENTITAS
# Kelompok     : 01 - Geprek Mumbul
# NIM/Nama - 1 : 13523021 - Muhammad Raihan Nazhim Oktana
# NIM/Nama - 2 : 13523044 - Muhammad Luqman Hakim
# NIM/Nama - 3 : 13523092 - Muhammad Izzat Jundy
# Instansi     : Sekolah Teknik Elektro dan Informatika (STEI) Institut Teknologi Bandung (ITB)
# Jurusan      : Teknik Informatika (IF)
# Nama File    : data_centering.py
# Topik        : Tugas Besar 2 Aljabar Linier dan Geometri 2024 (IF2123-24)
# Tanggal      : Kamis, 12 Desember 2024
# Deskripsi    : Subprogram F03 - Data Centering
# PJ F03       : 13523021 - Muhammad Raihan Nazhim Oktana

# KAMUS
# find_average : function
# data_centering : procedure

# ALGORITMA
def find_average(matrix : list[list[float]]) -> list[float] :
    # DESKRIPSI LOKAL
    # Sebuah fungsi untuk menghitung rata-rata intensitas di posisi yang bersesuaian.

    # KAMUS LOKAL
    # matrix : matrix of float
    # avg : list of float
    # row , col : integer
    # i , j : integer (index)

    # ALGORITMA LOKAL
    row = len(matrix)
    col = len(matrix[0])
    avg = [0.0 for i in range (col)]
    for i in range (row) :
        for j in range (col) :
            avg[j] = avg[j] + matrix[i][j]
    for i in range (len(avg)) :
        avg[i] = avg[i] / row
    return avg

def data_centering(matrix : list[list[float]]) -> list[list[float]] :
    # DESKRIPSI LOKAL
    # Sebuah prosedur untuk mengurangi nilai setiap elemen intensitas dengan rata-rata yang bersesuaian.

    # KAMUS LOKAL
    # matrix : matrix of float
    # avg : list of float
    # row , col : integer
    # i , j : integer (index)

    # ALGORITMA LOKAL
    avg = find_average(matrix)
    row = len(matrix)
    col = len(matrix[0])
    for i in range (row) :
        for j in range (col) :
            matrix[i][j] = matrix[i][j] - avg[j]
    return matrix