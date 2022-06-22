import config
import base64
import requests

PLAYLIST_URL = 'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

def spotify_auth():
    msg = '{client_id}:{client_secret}'.format(
            client_id=config.SPOTIFY_CLIENT_ID,
            client_secret=config.SPOTIFY_CLIENT_SECRET)
    msg = base64.b64encode(msg.encode()).decode()
    resp = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'client_credentials',
        # 'scope': 'playlist-read-public',
    }, headers={
        'Authorization': 'Basic {}'.format(msg)
    })
    json = resp.json()
    return json['access_token']

def get_playlist(playlist_id: str):
    token = spotify_auth()
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    url = PLAYLIST_URL.format(playlist_id=playlist_id)
    resp = requests.get(url, headers=headers)
    json = resp.json()
    tracks = [i['track'] for i in json['items']]
    return [{
        'name': t['name'],
        'artist': ', '.join(a['name'] for a in t['artists'])
    } for t in tracks]

def search_soundcloud(query: str):
    params = {
        'q': query,
        'user_id': config.SOUNDCLOUD_USER_ID,
        'client_id': config.SOUNDCLOUD_CLIENT_ID,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Authorization': 'OAuth {}'.format(config.SOUNDCLOUD_TOKEN),
    }
    resp = requests.get('https://api-v2.soundcloud.com/search/tracks', params=params, headers=headers)
    json = resp.json()
    results = json['collection']

    # Sort by number of likes, assuming
    # the more likes, the more legit it is
    results = sorted(results, key=lambda r: -(r['likes_count'] or 0))
    return results

def main(playlist_id: str):
    tracks = get_playlist(playlist_id)
    for track in tracks:
        query = '{} {}'.format(track['name'], track['artist'])
        results = search_soundcloud(query)
        url = results[0]['permalink_url']
        print(url)

if __name__ == '__main__':
    import sys
    playlist_id = sys.argv[1]
    main(playlist_id)
