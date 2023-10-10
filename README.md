# Pomodoro Spotify Player

For a thorough demo visit [my portfolio](https://waylonwilliams.notion.site/Spotify-Pomodoro-Timer-cd76a6e450324ade8e6dbe16ab96e26e?pvs=4)

https://github.com/waylonwilliams/spotify_pomodoro/assets/145303505/7a648929-c326-47a7-87ac-56407ee8e64e

https://github.com/waylonwilliams/spotify_pomodoro/assets/145303505/65b606f6-8830-417a-bb74-60dddf6c7151

https://github.com/waylonwilliams/spotify_pomodoro/assets/145303505/ce9452d5-b588-4344-b12c-52ed5f0cb7f7



To use this application yourself:

0. Clone or download this repo

1. Create a Spotify app
    
    Because Spotify has not yet accepted my application for their “extended quota mode”, I would have to authorize each individual user before they could connect to my app and thus to Spotify’s API. To create your own Spotify app to run the Pomodoro program,
    
    Go to [https://developer.spotify.com/](https://developer.spotify.com/)
    
    Navigate to your dashboard
    
    Click “Create app”
    
    Fill in “App name” and “App description” with anything 
    
    Fill in “Redirect URIs” with :   http://localhost:5000/authorize
    
    Agree to Spotify’s terms and click save
    
    Click settings
    
    Scroll down and click “Edit”
    
    Add the following urls to the list of “Redirect URIs”
    
    https://localhost:5000/authorize
    
    http://localhost:5000/authorize
    
    https://localhost:5000/authorize/
    
    http://127.0.0.1:5000/authorize
    
    http://127.0.0.1:5000/authorize/
    
    https://127.0.0.1:5000/authorize
    
    https://127.0.0.1:5000/authorize/
    
    Click save
    
    Find your “Client ID” and “Client Secret” because you will use them in the next step
    
2. Run setup.py
    
    In your terminal change your directory to be of the downloaded program, something like
    
    ```bash
    cd Downloads/spotify_pomodoro-main
    ```
    
    Run the following command in your terminal
    
    ```bash
    python3 setup.py
    ```
    
    When prompted to enter client id and client secret, do so
    
    After this the app is running and you just need to open it in your browser
    
3. Open the application in your browser
    
    In your terminal it will say something like
    
    ```bash
    Running on http://127.0.0.1:5000
    ```
    
    Enter that link into your browser and use the application!


    

Possible issues:

Spotify sometimes won’t recognize your device as a “device” even after you open Spotify. If the application is still not working even after you have opened Spotify, try pressing play to register it as a device.
