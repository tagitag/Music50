function SetUp()
  {
      if (musiclist.length !=0 )
      {
          //create the buttons and the list of next songs
          LoadSongs();

          updatetableUI(0);
      }
      else
      {
        document.getElementById("songstable").style="display:none;";
      }
  }

  window.onload = function () {
      SetUp();
      buttonSetup();
  }

  function buttonSetup()
  {
      btn = document.getElementById("NextButton");
      btn.addEventListener("click", function(){NextButton()}, false);
      btn = document.getElementById("LastButton");
      btn.addEventListener("click", function(){LastButton()}, false);
      btn = document.getElementById("LoopCurrentButton");
      btn.addEventListener("click", function(event){LoopCurrentButton(event)}, false);
      btn = document.getElementById("LoopListButton");
      btn.addEventListener("click", function(event){LoopListButton(event)}, false);
  }

  let prevousRow = -1;
  function updatetableUI(row)
  {
      tr = document.getElementById("tr:"+row);
      tr.classList.add("table-success");
      if (prevousRow != -1)
      {
          trp = document.getElementById("tr:"+prevousRow);
          trp.classList.remove("table-success");
          prevousRow = row;
      }
      prevousRow = row;
  }

  let stoplist = false;
  let cur = 0;
  function Next()
  {
      if (cur < musiclist.length-1 )
      {
          cur++;
          currentSong = musiclist[cur]["url"];
          updatetableUI(cur);
      }
      else if (listloop)
      {
          cur = 0;
          currentSong = musiclist[cur]["url"];
          updatetableUI(cur);
      }
      else
      {
          stoplist = true;
      }
  }
  function Last()
  {
      if (cur > 0)
      {
          cur--;
          currentSong = musiclist[cur]["url"];
          updatetableUI(cur);
      }
      else
      {
          cur = musiclist.length - 1;
          currentSong = musiclist[cur]["url"];
          updatetableUI(cur);
      }
      stoplist = false;
  }
  function LoadSongs()
  {
      // goes through each song in the list and adds it to the div for songs
      let table = document.getElementById("songstable");
      for (let i = 0; i < musiclist.length; i++ )
      {
          let song = musiclist[i];
          // song will have id, views, name. send back (id, views)
          let tr = document.createElement("tr");
          tr.id = "tr:"+i;
          let tdi = document.createElement("td");
          let tdn = document.createElement("td");
          let tdl = document.createElement("td");
          tdi.innerHTML = i + 1;
          tdn.innerHTML = song["name"];
          tdl.innerHTML = song["length"].replace(/-/g,":");
          tr.appendChild(tdi);
          tr.appendChild(tdn);
          tr.appendChild(tdl);
          table.appendChild(tr);
      }

  }

  let loop = false;
  function LoopCurrent()
  {
      if (!loop)
      {
          loop = true;
          // update the link of the current song to handle loops
      }
      else
      {
          loop = false;
          // remove the loop feature and carry on with the rest of the list
      }

  }

  function NextButton()
  {
      Next();
      if (!stoplist)
      {
          player.loadVideoById(currentSong);
          player.playVideo();
      }
  }
  function LastButton()
  {
      Last();
      if(!stoplist)
      {
          player.loadVideoById(currentSong);
          player.playVideo();
      }
  }

  let loopCurrent = false;
  function LoopCurrentButton(event)
  {
    if (!loopCurrent)
    {
        // the program will automatically go through each song, so all that this will do is allow the list to start at 0 once more
        loopCurrent = true;
        event.target.classList.remove("btn-info")
        event.target.classList.add("btn-primary")
    }
    else
    {
        loopCurrent = false;
        event.target.classList.remove("btn-primary")
        event.target.classList.add("btn-info")
    }
  }

  let listloop = false;
  function LoopListButton()
  {
      if (!listloop)
      {
          // the program will automatically go through each song, so all that this will do is allow the list to start at 0 once more
          listloop = true;
          event.target.classList.remove("btn-info")
          event.target.classList.add("btn-primary")
      }
      else
      {
          listloop = false;
          event.target.classList.remove("btn-primary")
          event.target.classList.add("btn-info")
      }

  }