CLIENT_ID = input("Enter client id: ")
CLIENT_SECRET = input("Enter client secret: ")

SCOPE = "user-library-read playlist-read-private playlist-read-collaborative user-modify-playback-state user-read-playback-state user-read-currently-playing"
def get_header(access_token):
     return {'Authorization': f'Bearer {access_token}'}

temp_uri = "spotify:track:3hhpgCAXnT51WikEgQXHgt"
second_temp_uri = "spotify:track:4opvLRUmTwSXWeVpm4FOf8"
add_to_queue_url = "https://api.spotify.com/v1/me/player/queue?uri=spotify%3Atrack%3A{}"
pause_url = 'https://api.spotify.com/v1/me/player/pause'
get_playlist_info_url = "https://api.spotify.com/v1/playlists/{}/tracks"
skip_url = "https://api.spotify.com/v1/me/player/next"
queue_url = "https://api.spotify.com/v1/me/player/queue"
volume_url = "https://api.spotify.com/v1/me/player/volume?volume_percent={}"
current_url = "https://api.spotify.com/v1/me/player"
album_url = "https://api.spotify.com/v1/albums/{}/tracks"
artist_url = "https://api.spotify.com/v1/artists/{}/top-tracks?market=US"
track_url = "https://api.spotify.com/v1/tracks/{}"