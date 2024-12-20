# PROGRAM K01-GeprekMumbul-F00

# IDENTITAS
# Kelompok     : 01 - Geprek Mumbul
# NIM/Nama - 1 : 13523021 - Muhammad Raihan Nazhim Oktana
# NIM/Nama - 2 : 13523044 - Muhammad Luqman Hakim
# NIM/Nama - 3 : 13523092 - Muhammad Izzat Jundy
# Instansi     : Sekolah Teknik Elektro dan Informatika (STEI) Institut Teknologi Bandung (ITB)
# Jurusan      : Teknik Informatika (IF)
# Nama File    : app.py
# Topik        : Tugas Besar 2 Aljabar Linier dan Geometri 2024 (IF2123-24)
# Tanggal      : Kamis, 12 Desember 2024
# Deskripsi    : Subprogram F00 - Main Program App
# PJ F00       : 13523021 - Muhammad Izzat Jundy

# KAMUS
# ...

# ALGORITMA
from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
import math
import zipfile
from backend.main_picture import *
from backend.sound_conversion import *

app = Flask(__name__)

DATABASE_FOLDER_IMAGE = 'static/uploads/database/image'
app.config['DATABASE_FOLDER_IMAGE'] = DATABASE_FOLDER_IMAGE
DATABASE_FOLDER_AUDIO = 'static/uploads/database/audio'
app.config['DATABASE_FOLDER_AUDIO'] = DATABASE_FOLDER_AUDIO
QUERY_FOLDER_IMAGE = 'static/uploads/query/image'
app.config['QUERY_FOLDER_IMAGE'] = QUERY_FOLDER_IMAGE
QUERY_FOLDER_AUDIO = 'static/uploads/query/audio'
app.config['QUERY_FOLDER_AUDIO'] = QUERY_FOLDER_AUDIO
app.config['PAGE'] = 0

ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_AUDIO = {'midi', 'mid'}

def allowed_file_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE

def allowed_file_audio(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_AUDIO

def allowed_file_zip(filename):
    return filename.split('.')[-1] == "zip"

def allowed_file_mapper(filename):
    return filename.split('.')[-1] == "txt"

# -----------------------------------------------------------------------------------------------
# JUMP PAGE
@app.route('/')
def home():
    app.config['PAGE'] = 0
    return render_template('index.html')

@app.route('/database')
def go_to_menu_database():
    app.config['PAGE'] = 0
    return render_template('menudatabase.html')

@app.route('/database/menambah')
def go_to_database_menambah():
    return render_template('databasemenambah.html')

@app.route('/query')
def go_to_menu_query():
    return render_template('menuquery.html')

@app.route('/query/image')
def go_to_query_image():
    return render_template('queryimage.html')

@app.route('/query/audio')
def go_to_query_audio():
    return render_template('queryaudio.html')

# -----------------------------------------------------------------------------------------------
# DATABASE

@app.route('/database/menambah/upload', methods=['POST'])
def upload_file():
    if 'zip_image' not in request.files or 'zip_audio' not in request.files or 'newmapper' not in request.files:
        return redirect(request.url)
    zip_image = request.files['zip_image']
    zip_audio = request.files['zip_audio']
    newmapper = request.files['newmapper']
    
    # Check if the file is valid
    if zip_image and allowed_file_zip(zip_image.filename) and zip_audio and allowed_file_zip(zip_audio.filename) and newmapper and allowed_file_mapper(newmapper.filename):
        filenameImage = os.path.join(app.config['DATABASE_FOLDER_IMAGE'], zip_image.filename)
        filenameAudio = os.path.join(app.config['DATABASE_FOLDER_AUDIO'], zip_audio.filename)
        filenameMapper = os.path.join("static/uploads/database", newmapper.filename)
        zip_image.save(filenameImage)
        zip_audio.save(filenameAudio)
        newmapper.save(filenameMapper)

        with open('./static/uploads/database/mapper.txt', 'a') as lama:
            with open(filenameMapper, 'r') as baru:
                isi = baru.read()
                lama.write(isi)

        with zipfile.ZipFile(zip_image, 'r') as zip_ref:
            for zip_info in zip_ref.infolist():
                zip_ref.extract(zip_info, app.config['DATABASE_FOLDER_IMAGE'])

        with zipfile.ZipFile(zip_audio, 'r') as zip_ref:
            for zip_info in zip_ref.infolist():
                zip_ref.extract(zip_info, app.config['DATABASE_FOLDER_AUDIO'])

        os.remove(filenameImage)
        os.remove(filenameAudio)
        os.remove(filenameMapper)

        return render_template('berhasilmenambah.html')
    else:
        return render_template('gagalmenambah.html')

@app.route('/database/view/next')
def next_page():
    with open('./static/uploads/database/mapper.txt', 'r') as file:
        singles = [line.strip() for line in file]
    if app.config['PAGE'] < math.ceil(len(singles)/10) - 1: app.config['PAGE']+=1
    return melihat_database()

@app.route('/database/view/prev')
def prev_page():
    if app.config['PAGE'] > 0: app.config['PAGE']-=1
    return melihat_database()

@app.route('/database/view/' + str(app.config['PAGE']))
def melihat_database():
    with open('./static/uploads/database/mapper.txt', 'r') as file:
        singles = [line.strip() for line in file]
    singles = [single.split(';') for single in singles]
    singlesInPage = []
    i = 0
    while app.config['PAGE'] * 10 + i < len(singles) and i < 10:
        singlesInPage.append(singles[app.config['PAGE'] * 10 + i])
        i+=1

    print(singles)
    return render_template('databasemelihat.html', singles=singlesInPage)

# SEARCHING
@app.route('/database/view/search', methods=['POST'])
def pencarian_database():
    keyword = request.form['keyword']

    with open('./static/uploads/database/mapper.txt', 'r') as file:
        singles = [line.strip() for line in file]

    singles = [single for single in singles if keyword.lower() in single.lower()]
    singles = [single.split(';') for single in singles]

    print(singles)

    return render_template('databasemelihatsearch.html', singles=singles)


# -----------------------------------------------------------------------------------------------
# QUERY

@app.route('/query/image/upload', methods=['POST'])
def query_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    # Check if the file is valid
    if file and allowed_file_image(file.filename):
        waktuAwal = datetime.datetime.now()
        filename = str(app.config['QUERY_FOLDER_IMAGE'] + "\\" + 'query' + '.' + file.filename.split('.')[-1])
        file.save(filename)

        images = os.listdir(app.config['DATABASE_FOLDER_IMAGE'])
        images = [image for image in images if image.endswith(('jpg', 'jpeg', 'png'))]
        filename = str(app.config['QUERY_FOLDER_IMAGE'] + "/" + 'query' + '.' + file.filename.split('.')[-1])
        print(filename)
        urutan_kemiripan = website_information(filename, "picture", app.config['DATABASE_FOLDER_IMAGE'])

        print(urutan_kemiripan)

        with open('./static/uploads/database/mapper.txt', 'r') as file:
            singles = [line.strip() for line in file]
        singles = [single.split(';') for single in singles]

        singles_sorted_with_percentage = []
        i = 0
        while i < len(urutan_kemiripan):
            j = 0
            while j < len(singles):
                if urutan_kemiripan[i][0] != singles[j][0]:
                    j+=1
                else:
                    break
            if j!=len(singles):singles_sorted_with_percentage.append((singles[j][0], singles[j][1], singles[j][2], round(urutan_kemiripan[i][1] * 100, 1)))
            else: print("ga ada di folder cuks " + filename + ";" + urutan_kemiripan[i][0])
            i+=1

        waktuAkhir = datetime.datetime.now()

        durasi = waktuAkhir - waktuAwal
        durasiDalamMS = durasi.total_seconds() * 1000

        return render_template('hasilqueryimage.html', singles=singles_sorted_with_percentage, durasi=round(durasiDalamMS, 2))
    else:
        return render_template('gagalmenambah.html')
    
@app.route('/query/audio/upload', methods=['POST'])
def query_audio():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    # Check if the file is valid
    if file and allowed_file_audio(file.filename):
        waktuAwal = datetime.datetime.now()
        filename = str(app.config['QUERY_FOLDER_AUDIO'] + "\\" + 'query' + '.' + file.filename.split('.')[-1])
        file.save(filename)

        audios = os.listdir(app.config['DATABASE_FOLDER_AUDIO'])
        audios = [audio for audio in audios if audio.endswith(('mid', 'midi'))]
        filename = str(app.config['QUERY_FOLDER_AUDIO'] + "/" + 'query' + '.' + file.filename.split('.')[-1])
        print(filename)
        urutan_kemiripan = retrieval(app.config['DATABASE_FOLDER_AUDIO'], filename)

        for i in range(len(urutan_kemiripan)):
            urutan_kemiripan[i] = (urutan_kemiripan[i][0].split('\\')[-1], urutan_kemiripan[i][1])

        print(urutan_kemiripan)

        with open('./static/uploads/database/mapper.txt', 'r') as file:
            singles = [line.strip() for line in file]
        singles = [single.split(';') for single in singles]

        singles_sorted_with_percentage = []
        i = 0
        while i < len(urutan_kemiripan):
            j = 0
            while j < len(singles):
                if urutan_kemiripan[i][0] != singles[j][1]:
                    j+=1
                else:
                    break
            if j!=len(singles):singles_sorted_with_percentage.append((singles[j][0], singles[j][1], singles[j][2], round(urutan_kemiripan[i][1] * 100, 1)))
            else: print("ga ada di folder cuks " + filename + ";" + urutan_kemiripan[i][0])
            i+=1

        waktuAkhir = datetime.datetime.now()

        durasi = waktuAkhir - waktuAwal
        durasiDalamMS = durasi.total_seconds() * 1000
        return render_template('hasilqueryaudio.html', singles=singles_sorted_with_percentage, durasi=round(durasiDalamMS, 2))
    else:
        return render_template('gagalmenambah.html')
    


if __name__ == '__main__':
    if not os.path.exists(DATABASE_FOLDER_IMAGE):
        os.makedirs(DATABASE_FOLDER_IMAGE)
    if not os.path.exists(DATABASE_FOLDER_AUDIO):
        os.makedirs(DATABASE_FOLDER_AUDIO)
    if not os.path.exists(QUERY_FOLDER_IMAGE):
        os.makedirs(QUERY_FOLDER_IMAGE)
    if not os.path.exists(QUERY_FOLDER_AUDIO):
        os.makedirs(QUERY_FOLDER_AUDIO)
    app.run(debug=True)
