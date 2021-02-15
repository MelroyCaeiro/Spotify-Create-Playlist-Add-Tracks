import os
import spotipy
import spotipy.util as util
import time

os.environ["SPOTIPY_CLIENT_ID"] = "CLIENT_ID_HERE"
os.environ["SPOTIPY_CLIENT_SECRET"] = "CLIENT_SECRET_HERE"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8080"
uri = "http://localhost:8080"
username = "melroy_caeiro"
scope = "user-top-read playlist-modify-private playlist-modify-public"    # only 2nd scope needed, others are unnecessary

token = util.prompt_for_user_token(username, scope, os.environ["SPOTIPY_CLIENT_ID"], os.environ["SPOTIPY_CLIENT_SECRET"], uri)
sp = spotipy.Spotify(auth=token)

playlist_name = "PLAYLIST_NAME_HERE"
limitNum = 10

# A minimum of 5 ID/URIs are required for each seeds
#seed_id = "https://open.spotify.com/track/7FiYF0ocZO3hwxrPkJ5wQs"   # Critical - Camelphat & Green Velvet (track seed example, pre-sliced)
#seed_artist = '240wlM8vDrf6S4zCyzGj2W'                              # Camelphat (artist seed example; sliced)
# Additional note on track ID as seeds: use slice(31, -1) to remove everything before the ID part
# Additional note on track URI as seeds: use slice(14, -1) to remove everything before the URI part
# Same applies for other ID values; use slice()

# Check if playlist of the same name exists (if yes, gets ID)
x = False           # Condition to create playlist if none exists
playlist_id = ''    # Create empty array for playlist ID
playlists = sp.user_playlists(username)
for playlist in playlists['items']:
    if playlist['name'] == playlist_name:  # Filter for newly created playlist
        playlist_id = playlist['id']
        #print("here: ", playlist_id)   # For debugging
        x = True

# Create playlist if none of the same name exists (for adding to playlist if it already exists)
if x == False:
    create = sp.user_playlist_create(username, playlist_name, public=True, collaborative=False, description="DESCRIPTION_HERE")
    playlist_id = ''
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:  # Filter for newly created playlist ID
            playlist_id = playlist['id']
            #print(playlist_id)   # For debugging

time.sleep(3)   # Delay adding tracks for playlist to be created first
results = sp.recommendations(seed_genres={'work-out', 'summer', 'dance', 'ambient', 'house'}, limit=10, target_energy=1)  # Get recommendations based on genre (genre seed)
for track in results['tracks']:
    #print('Recommendation: ', track['id'], "by", track['artists'][0]['name'], " ID: ", track['uri'][slice(14, -1)])    # For debugging
    id = track['uri']
    add = sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=[id])



