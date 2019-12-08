import sys
import pprint
import spotipy
import spotipy.util as util
from datetime import datetime, timedelta
from dateutil.parser import parse as dateparse



def create_client(token):
    if not token:
        print("Failure. Invalid Token")
        sys.exit()
    else:
        return spotipy.Spotify(auth=token)



def gather_saved_albums(spotify):
    result = set()

    offset = 0
    while True:
        album = spotify.current_user_saved_albums(limit=50, offset=offset)['items']
        offset += 50
        if album == []:
            break
        else:
            for item in album:
                id = item['album']['id']
                result.add(id)
    return result



def gather_favorite_artists(spotify):
    result = spotify.current_user_followed_artists(limit=50)['artists']['items']
    last_artist = result[-1]['id']

    while True:
        sub_list = spotify.current_user_followed_artists(limit=50, after=last_artist)['artists']['items']
        if sub_list == []:
            break
        last_artist = sub_list[-1]['id']
        result += sub_list
    return result



def gather_new_music(spotify, artist_list, currently_saved_albums):
    result = []

    for artist in artist_list:
        id = artist['id']
        artist_albums = spotify.artist_albums(id, album_type='album', limit=5)['items']
        album_set = set()

        for album in artist_albums:
            release_date = datetime.now() - dateparse(album['release_date'])
            album_id = album['id']
            album_name = album['name']

            if release_date.days > 30:
                break
            else:
                if album_name not in album_set and album_id not in currently_saved_albums:
                    album_set.add(album_name)
                    currently_saved_albums.add(album_id)
                    result.append(album_id)
    return result



def display_new_music(spotify, new_music):
    for album in new_music:
        album = spotify.album(album)
        print(', '.join(artist['name'] for artist in album['artists']))
        print(album['name'])
        print('Total Tracks: ' + str(album['total_tracks']))
        print('Released: ' + str(album['release_date']))
        image = album['images'][0]['url']
        print()


        tracks = album['tracks']['items']
        for track in tracks:
            print('\t' + track['name'])
            preview = track['preview_url']
        print()




if __name__ == "__main__":
    username = 'tar_12'  #sys.argv[1]
    scope = 'user-library-modify user-library-read user-follow-read playlist-modify-public playlist-modify-private user-top-read'
    token = util.prompt_for_user_token(username, scope, client_id='1ce54d1e7bbc4456a3f9711a3b082ac4', client_secret='842faf09eea44621b4cfdfa9b65d8b8d', redirect_uri='https://www.google.com/')

    spotify = create_client(token)
    #currently_saved_albums = gather_saved_albums(spotify)
    #artist_list = gather_favorite_artists(spotify)
    #new_music = gather_new_music(spotify, artist_list, currently_saved_albums)

    album_ids = ['1hMWqSv9nSRkRvNO6ExaMD', '4g1ZRSobMefqF6nelkgibi', '65T18oWoikW2MAilg9j8lW']


    display_new_music(spotify, album_ids)









#######
