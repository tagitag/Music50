import os
from googleapiclient.discovery import build
import re
import requests
import urllib.parse

from flask import redirect, render_template, session
from functools import wraps

def apology(message, code=400):
    """render a apology message to the user using a meme"""
    def escape(s):
        """
        Escape special characters.
        so one can make cool memes as messages ofc ofc

        https://github.com/jacebrowning/memegen#special-characters
        """
        # gets rid of the old characters and replaces them with new ones that are used in the meme gen
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s.replace(old,new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code # i assume this is the return code given from the sever

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/

    so basically, you place one function inside another in a specific location, like how you can do that using the lay out abiliy of jinja
    """
    @wraps(f)
    def decoratedFunction(*args, **kwards):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwards)
    return decoratedFunction


#INFO FOR THE LOOK UP FUNCTION

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")
# else:
#     key = os.environ.get("API_KEY")
key = "AIzaSyB14Aw-kvQuATr2xUZ0rP-AgkfZPT0nlBg"
# build youtube api service
service = build("youtube","v3", developerKey=key)


# generate the parsing paterns
h_pattern = re.compile(r"(\d+)H")
m_pattern = re.compile(r"(\d+)M")
s_pattern = re.compile(r"(\d+)S")

def lookup(urlid):
    """look up a youtube url, return none if not valid, or if non existant return Name, Lenght of video, """
    try:
        #requesting both the sinnipet and the content detail, for the title and duration information
        vid_request = service.videos().list(
            part="snippet, contentDetails",
            id=urlid
        )
        response = vid_request.execute()

    except:
        return None

    #stuff
    try:
        #gets the duration key from the items list
        item = response[ 'items']
        content = item[0]["contentDetails"]
        duration = content["duration"]

        h = h_pattern.search(duration)
        m = m_pattern.search(duration)
        s = s_pattern.search(duration)

        H = int(h.group(1)) if h else 0
        M = int(m.group(1)) if m else 0
        S = int(s.group(1)) if s else 0

        #get the title from the dictionary response
        snippet = item[0]["snippet"]
        tittle = snippet["title"]

        return {
            "name": tittle,
            "length": {"H":H,"M":M,"S":S}
        }
        # i might use the thumbnail for something, i do not know rn tgb, like i might put it somewhere to make the thing look nicer
    except:
        return None

# url1 = "https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id=X8iBy-kKxbc&key=AIzaSyB14Aw-kvQuATr2xUZ0rP-AgkfZPT0nlBg&alt=json"
# print("------------------------------------")
# res = requests.get(url1)
# res.raise_for_status()
# p = url.json()
# print(p)

def get_id_url(url):
    url_data = urllib.parse.urlparse(url)
    return url_data.query[2::]
