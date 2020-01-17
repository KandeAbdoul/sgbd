from flask import Flask
import requests
from main import sgbd
app = Flask(__name__)
@app.route('/')
def test():
    sgbd()

if __name__ == "__main__":
    sgbd()
    # app.run(host='127.0.0.1',port='8888', debug=True)
