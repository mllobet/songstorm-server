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

ngrok_url = 'http://68d39f36.ngrok.com'


@app.route('/api/link', methods=['GET'])
def get_link():
    title = request.args['title']

    song_id = str(uuid.uuid1())[0: 8]
    song = get_spotify(title)
    song['youtube'] = get_youtube(title)
    song['apple'] = get_apple(title)
    SONG_DATA[song_id] = song

    url = ngrok_url + '/song/' + song_id
    return jsonify({'link': url})


@app.route('/api/linkk', methods=['GET'])
def get_linkk():
    title = request.args['title']

    song_id = str(uuid.uuid1())[0: 8]
    song = get_spotify(title)
    song['youtube'] = get_youtube(title)
    song['apple'] = get_apple(title)
    SONG_DATA[song_id] = song

    url = ngrok_url + '/song/' + song_id 
    return url


@app.route('/api/near', methods=['GET'])
def get_near():
    return 'OK'


@app.route('/api/send', methods=['POST'])
def post_send():
    return 'OK'


@app.route('/api/listening', methods=['POST'])
def post_listening():
    return 'OK'


@app.route('/song/<sid>', methods=['GET'])
def render_song(sid):
    song = SONG_DATA[sid]
    return render_template('song.html', name=song['name'], image=song['image'], spotify=song['spotify'],
                           youtube=song['youtube'], apple=song['apple'])


def get_spotify(link):
    url = 'https://api.spotify.com/v1/search?q=' + link.replace(' ', '%20') + '&type=track'
    res = json.loads(requests.get(url).text)
    items = res['tracks']['items']
    if len(items) < 1:
        return {'link': '', 'name': '', 'image': ''}
    track = items[0]['album']['external_urls']['spotify']
    return {'spotify': track, 'name': link, 'image': items[0]['album']['images'][0]['url']}

def get_youtube(link):
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=' + link.replace(' ', '+') + '+music&type=video&videoCaption=closedCaption&key=AIzaSyAn0Ctw-bCSefAjQFhyNI6HzMdWEuZXImI'
    res = json.loads(requests.get(url).text)
    vid_id = res['items'][0]['id']['videoId']
    return "http://youtube.com/watch?v=" + vid_id

def get_apple(link):
    url = 'https://itunes.apple.com/search?country=us&limit=1&term=' + link.replace(' ', '+')
    res = json.loads(requests.get(url).text)
    return res['results'][0]['trackViewUrl']

if __name__ == "__main__":

    app.run(debug=True)
