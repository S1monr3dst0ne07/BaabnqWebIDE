import flask
import threading
import sys
import io
import os
import subprocess

def error(x):
    raise Exception(x)

app = flask.Flask(__name__)


def run(xEditorContent=''):
    print(xEditorContent)

    with open("source.baabnq", "w") as xFile:
        xFile.write(xEditorContent)

    try:
        xCompilerOut = subprocess.run(
            ["python", "Compiler.py", "-i", "source.baabnq"], 
            timeout=10,
            capture_output=True    
        ).stdout.decode("ascii")
    except subprocess.TimeoutExpired:
        return 'Error: Compiler timed out, something took too long.'

    
    print(xCompilerOut)
    
    xErrorLine = xCompilerOut.split("\n")[-2]
    if ('error' in xErrorLine.lower()):
        return xErrorLine

    try:
        xVMOut = subprocess.run(
            ["python", "vm.py", "-f", "build.s1"], 
            timeout=10,
            capture_output=True
        )
    except subprocess.TimeoutExpired:
        return 'Error: Virtual Machine timed out, something took too long.'


    print(xVMOut)

    return (
        xVMOut.stderr if 
        xVMOut.returncode else 
        xVMOut.stdout
    ).decode("ascii")
    




@app.route("/")
def serveHome():
    return flask.render_template("index.html")    

@app.route("/favicon.ico")
def servrFavicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route("/run", methods = ['POST', 'GET', 'OPTIONS'])
def serveRun():
    if flask.request.method == 'GET':
        return flask.redirect('/')
    
    if flask.request.method == 'OPTIONS':
        xResponse = flask.make_response()
        xResponse.headers.add("Access-Control-Allow-Origin", "*")
        xResponse.headers.add('Access-Control-Allow-Headers', "*")
        xResponse.headers.add('Access-Control-Allow-Methods', "*")    
        return xResponse


    xRequest = flask.request.get_json()
    if 'source' not in xRequest.keys():
        return "Error: Malformed Request"

    xEditorContent = xRequest['source']
    xOutput = run(xEditorContent)
    xResponse = flask.Response(xOutput)
    xResponse.headers.add("Access-Control-Allow-Origin", "*")
    
    return xResponse
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
    
