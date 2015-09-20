#!/usr/bin/env python2.7

from flask import Flask
# from flask import request

app = Flask(__name__)


@app.route('/api/link', methods=['GET'])
def get_link():
    return 'OK'


@app.route('/api/near', methods=['GET'])
def get_near():
    return 'OK'


@app.route('/api/send', methods=['POST'])
def post_send():
    return 'OK'


@app.route('/api/listening', methods=['POST'])
def post_listening():
    return 'OK'


@app.route('/song', methods=['GET'])
def render_song():
    return 'OK'

if __name__ == "__main__":

    app.run(debug=True)
