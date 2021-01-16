# MovieToGifs
## Creates a gif for each voice line in a movie 

# Installation

1. Download project
2. Install requiremtns.txt 
  - pip install -r requirements.txt
2. Create a "movie" and "gifs" folder inside the project
  - <img src="https://i.imgur.com/xMXPMJ2.png">
3. Put your movie/video mp4 into the "movie" folder
4. Find the subtitle file from https://yifysubtitles.org/ and put that file in the "movie" folder as well
  - <img src="https://i.imgur.com/VRg9l9K.png">
5. Run main.py
6. Optionally uncomment line 111 to send gifs to a discord channel (fill in your token and channel id)
  - [```send_gif("token", channel_id, f"gifs/{str(save_count)}.gif", f"Created gif: {save_count} from {str(sub.start)} -> {str(sub.end)}")```](https://github.com/NMan1/MovieToGifs/blob/a364b34fa6f677479bbd59f142fece7b0d0e72fa/main.py#L111)
  
  # Output
  
  <img src="https://i.imgur.com/hjbEd7d.png">
  
  With discord line:
  
  <img src="https://i.imgur.com/m4hfzJi.png">
