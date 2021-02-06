import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
import importpythonmodule

UPLOAD_FOLDER = 'static/uploadedvideo'
# UPLOAD_FOLDER = os.path.dirname('./uploadedvideo')
ALLOWED_EXTENSIONS = {'avi', 'wmv', 'mpeg', 'mov', 'divx', 'dat', 'flv', 'mp4', 'avchd', 'webm', 'mkv'}   

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='template') 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/videofromupload', methods=['GET', 'POST'])     
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('upload.html')

@app.route("/echo")
def echo():
    # return "You said: " + request.args.get('text', '')
    return Response(generate_text())

# @app.route('/videofromupload/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

# @app.route('/videofromlink', methods=['GET', 'POST'])
# def home():
#     return render_template("link.html")

# @app.route('/videofromupload/display/<filename>')
# def display_video(filename):
# 	print('display_video filename: ' + filename)
# 	return redirect(url_for('uploadedvideo', filename= filename), code=301)

# @app.route('/videofromupload/display/<filename>'  #, methods=['GET', 'POST'])
# def video_generated():
#     return Response(generate())


if __name__=="__main__":
    app.run(host='localhost', port=5000, debug=True)