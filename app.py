import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory

OBS_DIR = '/home/dominouzu/sairo/tmp'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

app = Flask(__name__)
app.config['OBS_DIR'] = OBS_DIR

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file added')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['OBS_DIR'], filename))
            return redirect(url_for('uploaded_file', filename = filename))
    
    return ''' 
    <!doctype html>
    <title> Upload file </title>
    <h1> Upload New File </h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type= submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['OBS_DIR'], filename)

if __name__ == "__main__":
    app.run(debug=True)


