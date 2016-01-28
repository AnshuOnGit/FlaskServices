__author__ = 'anshu'

from flask import Flask, send_from_directory
import os.path as opath

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def hello():
    return 'Hello, World!'

@app.route("/file/<file_name>")
def spit_file_on_browser(file_name):
    print(file_name)
    if opath.exists('uploads/'+str(file_name)):
        return send_from_directory('uploads',file_name)
    else:
        return("File does not exist on server.")

def read_file(file_path):

    if not opath.exists(file_path):
        return 'Sorry you have wrong file'
    with open(file_path,'r') as file:
        for line in file.readlines():
            yield line

if __name__ == "__main__":
    app.run()
    #print(read_file('readFile.py'))
