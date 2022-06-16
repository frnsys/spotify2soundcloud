This extracts tracks for a Spotify playlist and tries to find matching tracks on Soundcloud.

# Setup

Create `config.py` with the following values:

```
# Get these by opening up soundcloud in the browser
# and inspecting the requests to find one that has the OAuth token in the headers
# and getting the user_id and client_id params.
SOUNDCLOUD_TOKEN = ''
SOUNDCLOUD_USER_ID = ''
SOUNDCLOUD_CLIENT_ID = ''

SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
```

# Example Usage

```
# Given a spotify playlist url like https://open.spotify.com/playlist/PLAYLIST_ID
./main.py <PLAYLIST_ID> > /tmp/playlist.txt
```

Then you can e.g. play the tracks with `mpv`:

```
mpv --playlist=/tmp/playlist.txt
```