#!/usr/bin/env python2.7

from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":

    app.run(debug=True)
