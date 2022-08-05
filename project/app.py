import os
from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta

from helpers import apology, login_required, lookup, get_id_url

#config application
app = Flask(__name__)

#make sure to auto relode templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

#using file system for the session instead of cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

# connecting to the database
db = SQL("sqlite:///music.db")

@app.after_request
def after_request(response):
    """make sure responses arent cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/register",methods=["GET","POST"] )
def register():
    """registers someone into the data base"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        # get info
        password = request.form.get("password")
        conferm = request.form.get("conferm")
        name = request.form.get("username")

        # check if the info is there
        if not name:
            return apology("Input a Name")
        if not password:
            return apology("Input a Password")
        if not conferm:
            return apology("Input a Confermation Password")

        # check info
        rows = db.execute("SELECT * FROM users WHERE username = ?", name)
        if len(rows) != 0:
            return apology("Username Taken")

        if password != conferm:
            return apology("Confermation Failed")

        db.execute("INSERT INTO users (username,hash) VALUES (?,?)", name, generate_password_hash(password))

        # redirect to index
        return redirect("/")




@app.route("/login", methods=["GET","POST"])
def login():
    """logins in user"""
    if request.method == "GET":
        return render_template("login.html")
    else:
        # clear any old sessions
        session.clear()

        # get info from page
        password = request.form.get("password")
        name = request.form.get("username")

        # check if there is a input
        if not name:
            return apology("Input username")
        if not password:
            return apology("Input Password")

        #check the rest of the info before it is ready to login the user
        rows = db.execute("SELECT * FROM users WHERE username = ?", name)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"],password):
            return apology("Invalid Username Or Password")

        # when all checks have been passed:
        session["user_id"] = rows[0]["id"]

        # set them on there way to the homepage
        # get all the info i need, and pass it into the home page.
        return redirect("/")

@app.route("/logout")
def logout():
    # log out
    session.clear()
    # redirect
    return redirect("/")



@app.route("/", methods=["GET","POST"])
@login_required
def index():
    """Shows a list of most played songs"""
    # GET route
    if request.method == "GET":
        # Get all the songs and folders and send them on there way
        Srows = db.execute("SELECT * FROM songs WHERE user_id = ?", session["user_id"])
        Frows = db.execute("SELECT * FROM folders WHERE user_id = ?", session["user_id"])
        return render_template("index.html",songList=Srows, folderList=Frows)
    else:

        # Move Folder Region
        folder = request.form.get("selectedfolder")
        if folder:
            # a check
            row = db.execute("SELECT * FROM folders WHERE user_id = ? AND name = ?", session["user_id"], folder)
            if len(row) != 1:
                return apology("please input a valid folder")

            # convert the count to a int
            row[0]["count"] = int(row[0]["count"])

            # calculate total lenght of the folder in seconds
            h,m,s = row[0]["total_length"].split("-")
            h,m,s = int(h),int(m),int(s)
            total_seconds = timedelta(hours=h,seconds=s,minutes=m).total_seconds()

            # checking check boxes
            checkboxes = request.form.getlist("songCheckBox")
            # check if there is any sent checkBoxes
            if not checkboxes:
                pass
            else:
                for checkbox in checkboxes:
                    # check if the checkBox value is a int
                    try:
                        checkbox = int(checkbox)
                    except ValueError:
                        return apology("input a valid check")

                    # input the data into the connection database
                    row2 = db.execute("SELECT * FROM songs WHERE id=? AND user_id = ?", checkbox, session["user_id"])
                    if len(row2) != 1:
                        return apology("please input a valid song")
                    connectorSongs = db.execute("SELECT * FROM connector WHERE folder_id = ?", row[0]["id"])

                    # checks if there are any duplicate songs trying to enter the folder
                    songcopy = False
                    if len(connectorSongs) > 0:
                        for song in connectorSongs:
                            if checkbox == int(song["song_id"]):
                                songcopy = True

                    # we simply skip the duplicate and continue
                    if songcopy:
                        continue
                    db.execute("INSERT INTO connector (song_id, folder_id, user_id) VALUES (?, ?, ?)", checkbox, row[0]["id"], session["user_id"])

                    # update number of songs
                    row[0]["count"] += 1

                    # update total secods
                    h,m,s = row2[0]["length"].split("-")
                    h,m,s = int(h),int(m),int(s)
                    total_seconds_song = timedelta(hours=h,seconds=s,minutes=m).total_seconds()
                    total_seconds += total_seconds_song

                #convert back the seconds into the correct format:
                m,s = divmod(int(total_seconds),60)
                h,m = divmod(m,60)
                time = f"{h}-{m}-{s}"

                #insert the values into the folders database
                db.execute("UPDATE folders SET count = ?, total_length = ? WHERE user_id = ? AND name = ?",row[0]["count"], time ,session["user_id"], folder)

        # new song Region
        newsong = request.form.get("newSong")
        # check if the song exists
        if not newsong:
            pass
        else:
            url = get_id_url(newsong)
            copyCheck = db.execute("SELECT * FROM songs WHERE url = ? AND user_id = ?", url, session["user_id"])
            if len(copyCheck) > 0:
                pass
            else:
                dic = lookup(url)
                if not dic:
                    return apology("Insert a Youtube Url")
                db.execute("INSERT INTO songs (name, url, length, user_id) VALUES (?, ?, ?, ?)",dic["name"], url, f"{dic['length']['H']}-{dic['length']['M']}-{dic['length']['S']}", session["user_id"])

        # new folder Region
        newfolder = request.form.get("newFolder")
        if not newfolder:
            pass
        else:
            rows = db.execute("SELECT * FROM folders WHERE name = ? AND user_id = ?", newfolder, session["user_id"])
            # prevents a user making multiple files of the same name
            if len(rows) == 0:
                db.execute("INSERT INTO folders (name, user_id) VALUES (?, ?)", newfolder, session["user_id"])

        # get the song and folder data and send it to the page
        Srows = db.execute("SELECT * FROM songs WHERE user_id = ?", session["user_id"])
        Frows = db.execute("SELECT * FROM folders WHERE user_id = ?", session["user_id"])
        return render_template("index.html", songList=Srows, folderList=Frows)

@app.route("/movetofolder", methods=["GET"])
@login_required
def movetofolder():
    """ Makes the page responsible for moving songs into folders """
    # a just incase check
    if request.method == "GET":
        songlist = db.execute("SELECT name,id FROM songs WHERE user_id = ?", session["user_id"])
        folderlist = db.execute("SELECT name,id FROM folders WHERE user_id = ?", session["user_id"])
        return render_template("movefolder.html",folderList=folderlist, songList=songlist)

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """changes the password of a user"""
    if request.method == "GET":
        return render_template("changepass.html")
    else:
        # gets the info, and double checks the user has inputed it. so that they cant be sneaky on the client side of things
        pas = request.form.get("password")
        if not pas:
            return apology("must provide password")
        # if len(pas) < 8:
        #     return apology("must be 8 characters or more")
        conf = request.form.get("confirmation")
        if not conf:
            return apology("must provide confermation")

        # checks if the conferm = the pass
        if pas == conf:
            # inputs into the data base
            db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(pas), session["user_id"])
        else:
            return apology("Confermation Failed\n Try Again")

        return redirect("/login")

@app.route("/play", methods=["POST","GET"])
@login_required
def play():
    """"plays music"""
    # Get will be for individual songs, post will be for folders
    if request.method == "GET":
        #get song id to play
        song_id = request.args.get("Sid")
        if not song_id:
            return apology("click on a song")
        # check if the song belongs to the user
        row = db.execute("SELECT * FROM songs WHERE id=? AND user_id =?", song_id, session["user_id"])
        if len(row) != 1:
            return apology("Input valid song")
        #update views:
        row[0]["views"] += 1
        db.execute("UPDATE songs SET views = ? WHERE id=? AND user_id=?", row[0]["views"], song_id, session["user_id"])
        # render the player template
        return render_template("videoplayer.html", currentSong=row[0]["url"])
    #folder Route
    else:
        #check if the folder id is a valid int
        try:
            folder_id = int(request.form.get("folder"))
        except ValueError:
            return apology("Ïnput a valid Folder")
        # check if the folder belongs to the user
        row = db.execute("SELECT * FROM folders WHERE id = ? AND user_id = ?", folder_id, session["user_id"])
        if len(row) != 1:
            return apology("Input a valid Folder")
        # get the song ids found in the folder
        songIds = db.execute("SELECT * FROM connector WHERE folder_id = ?",folder_id)
        # create a list to store them
        musicList = []
        for songId in songIds:
            s = db.execute("SELECT * FROM songs WHERE id = ?", songId["song_id"])
            # a final check to see that indeed the song exists, perhaps there was a error somewhere
            if s:
                musicList.append(s[0])
        # load the page
        return render_template("videoplayer.html",currentSong=musicList[0]["url"], musicList=musicList)

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    # get the info:
    F_id = request.form.get("delFolder")
    S_id = request.form.get("Did")
    print("-----DLEELTEE-------------",F_id,"---------------------",S_id)

    # song delete route
    # check if inputed delete
    if not S_id:
        pass
    else:
        # check if song id is a valid int
        try:
            S_id = int(S_id)
            # if so check if the song id belongs to the user
            row = db.execute("SELECT * FROM songs WHERE user_id = ? AND id = ?",session["user_id"], S_id)
            if len(row) != 1:
                return apology("delete a valid song")

            #delete the song from songs, and connectors
            db.execute("DELETE FROM songs WHERE id = ?", S_id)
            db.execute("DELETE FROM connector WHERE song_id = ?", S_id)
        except ValueError:
            return apology("Get a Valid Song/Folder")

    #check if there is a folder id input
    if not F_id:
        pass
    else:
        # check if the folder id is a valid int
        try:
            F_id = int(F_id)
            # check if the folder id belongs to the user
            row = db.execute("SELECT * FROM folders WHERE user_id = ? AND id = ?",session["user_id"], F_id)
            if len(row) != 1:
                return apology("delete a valid folder")
            # delete the folder from folders, and connectors
            db.execute("DELETE FROM folders WHERE id = ?", F_id)
            db.execute("DELETE FROM connector WHERE folder_id = ?", F_id)

        except ValueError:
            return apology("Get a Valid Song/Folder")

    # send them back to the homepage
    return redirect("/")