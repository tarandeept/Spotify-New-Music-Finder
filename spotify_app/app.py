from flask import Flask, render_template
from script import *


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/new-music')
def new_music():
    username = 'tar_12'  #sys.argv[1]
    scope = 'user-library-modify user-library-read user-follow-read playlist-modify-public playlist-modify-private user-top-read'
    token = util.prompt_for_user_token(username, scope, client_id='1ce54d1e7bbc4456a3f9711a3b082ac4', client_secret='842faf09eea44621b4cfdfa9b65d8b8d', redirect_uri='https://www.google.com/')

    spotify = create_client(token)
    currently_saved_albums = gather_saved_albums(spotify)
    artist_list = gather_favorite_artists(spotify)
    album_ids = gather_new_music(spotify, artist_list, currently_saved_albums)

    #album_ids = ['1hMWqSv9nSRkRvNO6ExaMD', '4g1ZRSobMefqF6nelkgibi', '65T18oWoikW2MAilg9j8lW']
    albums = dict()
    for album in album_ids:
        album_JSON = spotify.album(album)
        albums[album] = album_JSON


    return render_template('new_albums.html', albums=albums)



if __name__ == "__main__":
    app.run(debug=True)
