from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_folder="assets")
CORS(app)

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
