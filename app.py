from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER_IMAGE = 'uploads/image'
app.config['UPLOAD_FOLDER_IMAGE'] = UPLOAD_FOLDER_IMAGE
UPLOAD_FOLDER_AUDIO = 'uploads/audio'
app.config['UPLOAD_FOLDER_AUDIO'] = UPLOAD_FOLDER_AUDIO

ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_AUDIO = {'mid'}

def allowed_file_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE

def allowed_file_audio(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_AUDIO

# -----------------------------------------------------------------------------------------------
# JUMP PAGE
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/database')
def go_to_menu_database():
    return render_template('menudatabase.html')

@app.route('/database/image')
def go_to_database_image():
    return render_template('databaseimage.html')

@app.route('/database/audio')
def go_to_database_audio():
    return render_template('databaseaudio.html')

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

@app.route('/database/image/upload', methods=['POST'])
def upload_file_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    # Check if the file is valid
    if file and allowed_file_image(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER_IMAGE'], file.filename)
        file.save(filename)
        return render_template('berhasilmenambah.html')
    else:
        return render_template('databaseimage.html')
    
@app.route('/database/audio/upload', methods=['POST'])
def upload_file_audio():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    # Check if the file is valid
    if file and allowed_file_audio(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER_AUDIO'], file.filename)
        file.save(filename)
        return render_template('berhasilmenambah.html')
    else:
        return render_template('databaseaudio.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER_IMAGE):
        os.makedirs(UPLOAD_FOLDER_IMAGE)
    if not os.path.exists(UPLOAD_FOLDER_AUDIO):
        os.makedirs(UPLOAD_FOLDER_AUDIO)
    app.run(debug=True)
