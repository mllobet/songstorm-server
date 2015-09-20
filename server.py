#!/usr/bin/env python2.7

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

import requests
import json
import uuid

app = Flask(__name__)

SONG_DATA = {}


@app.route('/api/link', methods=['GET'])
def get_link():
    title = request.args['title']

    song_id = str(uuid.uuid1())[0: 8]
    song = get_spotify(title)
    SONG_DATA[song_id] = song

    return jsonify(SONG_DATA[song_id])


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
    res = json.loads(requests.get(url).text)
    items = res['tracks']['items']
    if len(items) < 1:
        return {'link': '', 'name': '', 'image': ''}
    track = items[0]['album']['external_urls']['spotify']
    return {'spotify': track, 'name': link, 'image': items[0]['album']['images'][0]['url']}


if __name__ == "__main__":

    app.run(debug=True)
