# MUSIC50
#### Video Demo:  <URL https://youtu.be/buFjLKbFuRU>
#### Description: A Music Playlist on a Website

Music50 is a website you can store music from youtube.

The videos are stored in 2 ways:
1. Directly in the home page as a table
2. In folders
NOTE: When storing songs in a folder, it is not removed from the homepage, as it would make finding and listening to individual songs much more difficult.

You can directly watch the videos by simply clicking on them, or by clicking on a folder.

When a folder is click all the songs stored in it will automatically play. NOTE: sometimes due to the webrowser you use you may need to manually start the music. however i have observed that this is only for the first song in the list
A folder also allows for the fallowing actions: Next, Last, Loop Current, Loop List

    Next: plays the next song in in the List, it will stop at the end automatically

    Last: plays the Prevous song in the list, you can also use it to get to the last song of the list by clicking last at the start of the list. I decided to add this feature in as I thought it might make it more comfotable for a user to navigate there list

    Loop Current: Loops the current song, until you deactivate it

    Loop List: Loops the Whole List automatically, also In this instance when Next is clicked at the end of the list it will go back to the start.

The Homepage Contains:Song/Folder, New Song, New Folder, Add To Folder, Delete Mode

    Song/Folder: When clicked the table switches from displaing the songs a user has to the folders they have, and vise versa

    New Song: When clicked a input field, Submit Button, Cancle Button are displayed.
        - input field: Takes in a general youtube url.
        - Submit Button: makes the website store the video
        - Cancle Button: cancles the process, and removes the display of these elements

    New Folder: Works in much the same way as New Song, The only differance is that the user needs to input a name for the new folder.

    Add to Folder:
        this button opens a new page, where one must select the folder they want to add songs to and the songs they want to select
        the folder they want to select is selcted by the dropdown.
        While the songs they want to select are simlpy selected by clicking onto them. they turn light green to indicate they are selected

        you can canlce at any time, and return to the main page using the Cancle Button.

    Delete Mode:
        when this mode is activated. the color of the button will change to yellow and all the songs or folder names will change to red. this is a visual aid to inform the user Delete Mode is On.
        When in Delete Mode What ever song, or folder you click on will be deleted. Be careful in this mode as there is no confermation message.

    Note: you cant delete individual songs from a folder once set in the folder. you can however add as much music to them as you want, as many times as you want

## Files

app.py:
    app.py contains most of the code.

    it is use to load the webpages, gather the necisarry information from them, and to process it.

    it uses the flask library

    it has a login and log out system using the same logic from the one in the cs50 course

helpers.py
    this is a smaller file used to store and construct some functions that app.py will need to run

    this file uses the google api library called googleapiclient.

    the library is used to construct a youtube service object, witch allows me to easily send requests to the YouTube Data API. that i use to gather information from each youtube link that the user inputs. this is used in the lookup function.

music.db

    this is the data base used to store all the info of them webpage
    it contains 4 tables:
    1. users: has there name, pasword (using has generator) and unique id
    2. songs: has the youtube id (url), name, length, id of user, unique id
    3. folders: has name, user_id, total length of all songs, number of songs
    4. connector: has the folder id, the song id and the user id

templates folder:

    contains all the htm for the webpages in the website.
    index.html: homepage
    layout.htm: the layout used for easier coding
    login.html: the login page
    movefolder.html: the page one adds sonngs to a folder
    register.html: the register page
    videoplayer.html: the webpage one sees when they play a song/folder
    apology.html: used to give users error messages, same as in cs50 finance

static:

    contains all non changing information:
    java.js: contains all javaScrip for the videoplayer page
    .svg files are used in various locations to make the page look a little nicer


