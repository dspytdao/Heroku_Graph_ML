from flask import Flask

app = Flask(__name__, static_folder="assets")

from app import routes

if __name__ == '__main__':
    app.run(threaded=True, debug=True)