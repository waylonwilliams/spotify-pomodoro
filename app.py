from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect, render_template, jsonify
import time
import requests
import random
from os import urandom
from config import *

# configuring flask app
app = Flask(__name__)
app.secret_key = urandom(24).hex()
app.config["SESSION_COOKIE_NAME"] = "pomodoro-session"

# base page, creates a url for the user to give permissions
# see https://developer.spotify.com/documentation/web-api/concepts/authorization for authorization flow
@app.route("/")
def login():
    create_oauth = create_spotify_oauth()
    authorize_url = create_oauth.get_authorize_url()
    return redirect(authorize_url)

# after user accepts permissions, spotify redirects back here
@app.route("/authorize", methods=["GET", "POST"])
def authorize():
    # retrieves an access token with the information given to us from spotify
    create_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get("code")
    token_info = create_oauth.get_access_token(code)
    session["token_info"] = token_info
    # redirects user to my home page
    return render_template("index.html")

# when user presses "start timer" button
@app.route("/process", methods=["POST"])
def process():
    # ensuring access token
    session["token_info"], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect("/")
    access_token = session.get("token_info").get("access_token")
    headers = get_header(access_token)

    #checking if spotify open
    # issue: sometimes just opening spotify is not enough, spotify may need user to press play to register as open device
    response = requests.get(current_url, headers=headers)
    if not response.text:

        return render_template("err.html")
        return redirect("/") # could reroute to a different error page since toast is too complex with this stack
    
    # the same request holds info about volume level too
    previous_volume = response.json()
    previous_volume_num = int(previous_volume["device"]["volume_percent"])
    # sets volume to 0 to not make sound when clearing queue and queueing songs
    requests.put(volume_url.format(0), headers=headers)

    # html inputs -> flask session storage
    session["study_uri"] = (request.form["study_link"])
    session["study_time"] = int(request.form["study_time"])
    session["break_uri"] = (request.form["break_link"])
    session["break_time"] = int(request.form["break_time"])
    session["next_block"] = True # true for break, false for study


    # queues a placeholder song which signals the end of the user's queue
    response = requests.post(add_to_queue_url.format(temp_uri[14:]), headers=headers)

    # retrieves the queue, the reason i had to queue the song is because spotify normally
    # generates an endless queue for the user, so I only need to clear the songs manually queued
    # by the user because the songs i queue in the future will go ahead of the songs automatically
    # queued by spotify
    response = requests.get(queue_url, headers=headers)
    queue_info = response.json()
    # iterates the queue until the song i queued is found, clears all user-queued songs
    for i in queue_info["queue"]:
        requests.post(skip_url, headers=headers)
        if i["uri"] == temp_uri:
            break

    # pauses music and queues music for study and break periods
    requests.put(pause_url, headers=headers)

    # queues music for study and break periods
    study_tracks = get_tracks(session["study_uri"], headers)
    break_tracks = get_tracks(session["break_uri"], headers)
    for i in range(4):
        qq_songs(study_tracks, session["study_time"], headers)
        qq_songs(break_tracks, session["break_time"], headers)
    
    # begins playings music, or pauses if that is what user inputted
    response = requests.get(queue_url, headers=headers)
    queue_info = response.json()
    if queue_info["queue"][0]["uri"] == second_temp_uri:
        requests.post(skip_url, headers=headers)
        requests.put(pause_url, headers=headers)
        requests.put(volume_url.format(previous_volume_num), headers=headers)
        return render_template("timer.html", timer_val = session["study_time"])
    requests.post(skip_url, headers=headers)
    requests.put(volume_url.format(previous_volume_num), headers=headers)

    # opens the timer, the timing is handled in javascript
    return render_template("timer.html", timer_val = session["study_time"])

# runs when timer reaches 0 to reset timer
@app.route("/get_timer", methods=["POST"])
def get_timer():
    # ensuring access token
    session["token_info"], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect("/")
    access_token = session.get("token_info").get("access_token")
    headers = get_header(access_token)

    # checks whether a break or study session is next
    # javascript handles whether the next break is a long break
    if session["next_block"]: # if break
        # holds info for what next section is, flipping between study and break
        session["next_block"] = False
        timer_val = session["break_time"]
        # checks if next section is a break section
        response = requests.get(queue_url, headers=headers) # could just do this once and store in session?
        queue_info = response.json()
        if queue_info["queue"][0]["uri"] == second_temp_uri:
            response = requests.post(skip_url, headers=headers)
            response = requests.put(pause_url, headers=headers)
            return jsonify({"timer_val": timer_val, "text_val": "Short Break"})
        # skip to get to next sections music
        response = requests.post(skip_url, headers=headers)
        return jsonify({"timer_val": timer_val, "text_val": "Short Break"})
    else:
        # same as above just for study section
        session["next_block"] = True
        timer_val = session["study_time"]
        response = requests.get(queue_url, headers=headers)
        queue_info = response.json()
        if queue_info["queue"][0]["uri"] == second_temp_uri:
            requests.post(skip_url, headers=headers)
            requests.put(pause_url, headers=headers)
            return jsonify({"timer_val": timer_val, "text_val": "Study"})
        requests.post(skip_url, headers=headers)
        return jsonify({"timer_val": timer_val, "text_val": "Study"})

@app.route("/finished_timer", methods=["GET"])
def finished_timer():
    session["token_info"], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect("/")
    access_token = session.get("token_info").get("access_token")
    headers = get_header(access_token)

    response = requests.get(queue_url, headers=headers)
    queue_info = response.json()
    if queue_info["queue"][0]["uri"] == second_temp_uri:
        requests.post(skip_url, headers=headers)
        requests.put(pause_url, headers=headers)
        return render_template("end.html")
    requests.post(skip_url, headers=headers)
    return render_template("end.html")

# refreshes token
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    if not (session.get("token_info", False)):
        # if there is no token is invalid user is redirected to reauthenticate, signaled by token_valid = False 
        token_valid = False
        return token_info, token_valid

    # requires token to be refreshed if less than 60 seconds left, leeway
    now = int(time.time())
    # the access token lasts for about 1 hour
    is_token_expired = session.get("token_info").get("expires_at") - now < 60

    # if access token is expired, use refresh token to create new one
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get("token_info").get("refresh_token"))

    # successful token marked with token_valid = True
    token_valid = True
    return token_info, token_valid

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=url_for("authorize", _external=True),
            scope=SCOPE)

def get_tracks(link, headers):
    """returns a list of len 2 tuples each with a uri and duration"""
    if link[25:33] == "playlist":
        # good
        response = requests.get(get_playlist_info_url.format(link[34:56]), headers=headers)
        tracks = response.json()
        tracks = tracks["items"]
        uris = []
        for i in tracks:
            if i["is_local"]:
                continue
            uris.append((i["track"]["uri"], i["track"]["duration_ms"]))
        return uris
    elif link[25:30] == "album":
        # good
        response = requests.get(album_url.format(link[31:53]), headers=headers)
        tracks = response.json()
        tracks = tracks["items"]
        uris = []
        for i in tracks:
            if i["is_local"]:
                continue
            uris.append((i["uri"], i["duration_ms"]))
        return uris
    elif link[25:31] == "artist":
        # good
        response = requests.get(artist_url.format(link[32:54]), headers=headers)
        tracks = response.json()
        tracks = tracks["tracks"]
        uris = []
        for i in tracks:
            if i["is_local"]:
                continue
            uris.append((i["uri"], i["duration_ms"]))
        return uris
    elif link[25:30] == "track":
        # good
        response = requests.get(track_url.format(link[31:53]), headers=headers)
        track = response.json()
        uri = [(track["uri"], track["duration_ms"])]
        return uri
    elif link == "":
        # good
        return []
    
def qq_songs(tracks, time, headers):
    if tracks == []:
        requests.post(add_to_queue_url.format(second_temp_uri[14:]), headers=headers)
        return
    random_indices = random.sample(range(len(tracks)), len(tracks))
    total_song_time = 0
    i = 0
    i_max = len(random_indices)

    while total_song_time < time * 60000:
        requests.post(add_to_queue_url.format(tracks[random_indices[i]][0][14:]), headers=headers)
        total_song_time += tracks[i][1]
        i += 1
        if i == i_max:
            i = 0
            # if the playlist has been completely looped through, create a unique shuffle for the next loop
            random_indices = random.sample(range(len(tracks)), len(tracks))
    return
