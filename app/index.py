from flask import Flask, request, redirect

app = Flask(__name__, static_url_path='/static/')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "Missing file"

    f = request.files['file']
    if f.filename == '':
        return "No file selected"
    print(f.read())
    return "Uploaded. Nice" 

if __name__ == "__main__":
    app.secret_key = 'tN8z8k0Ik6g4fbJ8wWgdSDR7SLLtdAzzy'
    app.run()