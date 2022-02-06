from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_folder="assets")
CORS(app)

from app import routes

if __name__ == '__main__':
    app.run(threaded=True, debug=True)