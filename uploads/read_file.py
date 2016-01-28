__author__ = 'anshu'

from flask import Flask, request,redirect,url_for, render_template, send_from_directory
from werkzeug import secure_filename
import os.path as opath

app = Flask(__name__)
app.config.from_object(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','py'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/<user_name>")
def hello(user_name):
    return 'Hello and Hi, '+user_name

@app.route("/file/<file_name>")
def spit_file_on_browser(file_name):
    lines = ''
    for line in read_file(file_name):
        lines = lines + line + '<br>'
    return lines

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload():
    print('upload called')
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(opath.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def read_file(file_path):

    if not opath.exists(file_path):
        return 'Sorry you have wrong file'
    with open(file_path,'r') as file:
        for line in file.readlines():
            yield line

if __name__ == "__main__":
    app.run()
    #print(read_file('readFile.py'))
