#!/usr/bin/env python2.7

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

import argparse
import requests
import json
import uuid

app = Flask(__name__)

SONG_DATA = {}

URL = 'http://67722f.ngrok.com'


@app.route('/api/link', methods=['GET'])
def get_link():
    title = request.args['title']
    artist = request.args['artist']

    search_term = title + ' ' + artist

    song_id = str(uuid.uuid1())[0: 8]
    song = get_spotify(search_term)
    song['name'] = title
    song['artist'] = artist
    song['youtube'] = get_youtube(search_term)
    song['apple'] = get_apple(search_term)
    song['soundcloud'] = get_soundcloud(search_term)
    SONG_DATA[song_id] = song

    url = URL + '/song/' + song_id
    return jsonify({'link': url, 'youtube': song['youtube'],
                    'apple': song['apple'], 'spotify': song['spotify'],
                    'image': song['image']})


@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404


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
    song_name = song['name']
    song_artist = song['artist']
    if len(song['name']) > 25:
        song_name = song_name[0:22] + "..."
    if len(song['artist']) > 25:
        song_artist = song_artist[0:22] + "..."
    return render_template('song.html', name=song_name, image=song['image'], spotify=song['spotify'],
                           youtube=song['youtube'], apple=song['apple'], artist=song_artist,
                           soundcloud=song['soundcloud'])


def get_spotify(link):
    url = 'https://api.spotify.com/v1/search?q=' + link.replace(' ', '%20') + '&type=track'
    res = json.loads(requests.get(url).text)
    items = res['tracks']['items']
    if len(items) < 1:
        return {'link': '', 'name': '', 'image': ''}
    track = items[0]['album']['external_urls']['spotify']
    return {'spotify': track, 'image': items[0]['album']['images'][0]['url']}

def get_youtube(link):
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=' + link.replace(' ', '+') + '+music&type=video&videoCaption=closedCaption&key=AIzaSyAn0Ctw-bCSefAjQFhyNI6HzMdWEuZXImI'
    res = json.loads(requests.get(url).text)
    if len(res['items']) < 1:
        return ""
    vid_id = res['items'][0]['id']['videoId']
    return "http://youtube.com/watch?v=" + vid_id

def get_apple(link):
    url = 'https://itunes.apple.com/search?country=us&limit=1&term=' + link.replace(' ', '+')
    res = json.loads(requests.get(url).text)
    if len(res['results']) < 1:
        return ""
    return res['results'][0]['trackViewUrl']


def get_soundcloud(link):
    url = 'http://api.soundcloud.com/tracks?client_id=12e835d0b472be346823494a1ed7f3fe&q=' + link.replace(' ', '+')
    res = json.loads(requests.get(url).text)

    if len(res) < 1:
        return ""
    return res[0]['permalink_url']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch the songstorm server")
    parser.add_argument('-u', '--url', help='the URL the service is hosted on', required=True)
    args = parser.parse_args()

    URL = args.url

    app.run(debug=True)
