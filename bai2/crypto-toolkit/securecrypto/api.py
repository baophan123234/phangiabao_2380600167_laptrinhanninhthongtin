from flask import Flask, request, jsonify
from securecrypto import aes_utils
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, 'upload')
os.makedirs(FILES_DIR, exist_ok=True)


class StripTrailingMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        if 'PATH_INFO' in environ:
            environ['PATH_INFO'] = environ['PATH_INFO'].rstrip()
            if environ['PATH_INFO'].endswith('/') and len(environ['PATH_INFO']) > 1:
                environ['PATH_INFO'] = environ['PATH_INFO'].rstrip('/')
        return self.wsgi_app(environ, start_response)

app.wsgi_app = StripTrailingMiddleware(app.wsgi_app)


@app.route('/encrypt', methods=['POST'])
@app.route('/encrypt\n', methods=['POST'])
def encrypt():
    f = request.files['file']
    password = request.form['password'].strip()
    save_path = os.path.join(FILES_DIR, f.filename)
    f.save(save_path)
    key = aes_utils.encrypt_file_aes(save_path, password)
    return jsonify({"key": key})


@app.route('/decrypt', methods=['POST'])
@app.route('/decrypt\n', methods=['POST'])
def decrypt():
    f = request.files['file']
    password = request.form['password'].strip()
    save_path = os.path.join(FILES_DIR, f.filename)
    f.save(save_path)
    out_path = aes_utils.decrypt_file_aes(save_path, password)
    return jsonify({"output": out_path})


if __name__ == '__main__':
    app.run()
