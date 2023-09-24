# Spotify Pomodoro Player

Pomodoro is a productivity strategy in which the user focuses on a task deeply for a period(usually 25 minutes), takes a short break(usually 5 minutes), and repeats this cycle 4 times before taking a longer break.

In this application the user is able to ascribe certain Spotify playlists, albums, artists, or songs to play during the study or break periods of their Pomodoro. The user is also able to have their music pause during these periods. My application keeps a timer for each section of the Pomodoro and adjusts playback accordingly. The app is purposefully minimized in functionality and styling to keep the tool distraction free, while still offering user customization to create the best individual productivity. 

Flow of app:

authorize with spotify → input listening content and section length → timer runs for 4 cycles while playing relevant music

Demo: 

Upon opening the application the user will be redirected to log in with Spotify

![Screenshot 2023-09-23 at 6.35.46 PM.png](Spotify%20Pomodoro%20Player%20c39534d340694054b6de30c27ffc8c24/Screenshot_2023-09-23_at_6.35.46_PM.png)

After logging in the user is prompted to allow the application access to certain aspects of their Spotify account

![Image-6.jpg](Spotify%20Pomodoro%20Player%20c39534d340694054b6de30c27ffc8c24/Image-6.jpg)

Once the user accepts, they will be redirected to the home page of the application where they are prompted to enter a link for their study section’s music, their study section’s time, their break section’s music, and their break sections time.

- Allows the user to play any different kind of Spotify data (playlists, songs, artists, albums) or pause for their study or break section by processing the input link and making related API calls.

![Screenshot 2023-09-23 at 6.38.46 PM.png](Spotify%20Pomodoro%20Player%20c39534d340694054b6de30c27ffc8c24/Screenshot_2023-09-23_at_6.38.46_PM.png)

For this example, I will be using a playlist with 2 songs by Ryan Gosling for my study section, and an artist Macabre Plaza for my break section. Also, I’ll be using the standard Pomodoro timing of 25:5.

![Image-7.jpg](Spotify%20Pomodoro%20Player%20c39534d340694054b6de30c27ffc8c24/Image-7.jpg)

Previous to pressing “Start Pomodoro”, my queue is cleared as shown below

![IMG_0375.jpg](Spotify%20Pomodoro%20Player%20c39534d340694054b6de30c27ffc8c24/IMG_0375.jpg)

After pressing “Start Pomodoro”, my application clears the user’s queue, queues relevant amounts of songs from relevant links, and skips to the first song of the first study section. As you can see, there is 25 minutes worth of study music, 5 minutes worth of break music, and so on for 4 Pomodoros.

- Though more than the relative amount of music is queued for each section, my application skips to the next sections music when the section is over. In this case the total amount of study songs queued is about 30 seconds longer than 25 minutes, but when the 25 minutes is up the song will be skipped and the break music will begin.

![IMG_0376.jpg](Spotify%20Pomodoro%20Player%20c39534d340694054b6de30c27ffc8c24/IMG_0376.jpg)

The application changes to the timer page which presents the current section and time left

- The user has the option to hide the timer to become more immersed in the study session
- The user has the option to quit the timer, redirecting them to the home page where another time may be started

![Screenshot 2023-09-23 at 6.43.18 PM.png](Spotify%20Pomodoro%20Player%20c39534d340694054b6de30c27ffc8c24/Screenshot_2023-09-23_at_6.43.18_PM.png)

When the timer reaches 0, the song is skipped and break music begins

![IMG_0386.jpg](Spotify%20Pomodoro%20Player%20c39534d340694054b6de30c27ffc8c24/IMG_0386.jpg)

On the application, the timer is updated along with the name of the section

![Screenshot 2023-09-23 at 7.35.13 PM.png](Spotify%20Pomodoro%20Player%20c39534d340694054b6de30c27ffc8c24/Screenshot_2023-09-23_at_7.35.13_PM.png)

This continues for 4 study sections and 3 short breaks, and on what would be the 4th break this page is shown on the application

![Screenshot 2023-09-23 at 7.50.57 PM.png](Spotify%20Pomodoro%20Player%20c39534d340694054b6de30c27ffc8c24/Screenshot_2023-09-23_at_7.50.57_PM.png)

Left in the queue is the break section’s time worth of break music to lead the user into a longer break

![IMG_0387.jpg](Spotify%20Pomodoro%20Player%20c39534d340694054b6de30c27ffc8c24/IMG_0387.jpg)

To use this application yourself:

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
    
    [https://localhost:5000/authorize](https://localhost:5000/authorize) 
    
    [http://localhost:5000/authorize](http://localhost:5000/authorize/) 
    
    [https://localhost:5000/authorize/](https://localhost:5000/authorize/) 
    
    [http://127.0.0.1:5000/authorize](http://127.0.0.1:5000/authorize) 
    
    [http://127.0.0.1:5000/authorize/](http://127.0.0.1:5000/authorize/) 
    
    [https://127.0.0.1:5000/authorize](https://127.0.0.1:5000/authorize) 
    
    [https://127.0.0.1:5000/authorize/](https://127.0.0.1:5000/authorize/)
    
    Click save
    
    Find your “Client ID” and “Client Secret” because you will use them in the next step
    
2. Run setup.py
    
    In your terminal change your directory to be of the downloaded program, something like
    
    ```bash
    cd Downloads/spotify_pomodoro
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
