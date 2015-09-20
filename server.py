#!/usr/bin/env python2.7

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

import requests

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
    return render_template('song.html')


def get_spotify(link):
    url = 'https://api.spotify.com/v1/search?q=' + link.replace(' ', '%20') + '&type=track'
    res = requests.get(url)
    items = res['tracks']['items']
    if len(items) < 1:
        return {'link': ''}
    track = items['album']['external_urls']['spotify']
    return {'link': track}


if __name__ == "__main__":

    app.run(debug=True)
