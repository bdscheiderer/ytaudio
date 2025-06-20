# This program downloads video and audio from a Youtube video

import sys
import time
from pytubefix import YouTube
from pytubefix.cli import on_progress

# option to hard code download path (e.g., a music folder)
# if PATH = None, will dl to same directory as program is run from
# PATH = "your/download/path"
PATH = None


def main():

    # get user input for YouYube video url
    url =  input("Enter Youtube url:")

    # verify url entered 
    print(f"Video url: {url}")

    # get yt object or exit if not found
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
    except:
        print(f'Error: video {url} is unavailable.')
        sys.exit(0)
    else:
        print(f"Video found: {yt.title}")

    # ask if should download video and audio ("y") 
    # default "n" will download audio file only
    try:
        message = "Download video along with audio? (y/n) "
        video_dl = (input(message)).lower()
    except:
        video_dl = "n"
        
    # option to download video...first resolution stream
    if video_dl == "y":
        print("Downloading video...")
        yt.streams.first().download(output_path=PATH)
        print()

    # download audio (currently a .m4a file)
    print(f"Downloading audio...")
    ys = yt.streams.get_audio_only()
    ys.download(output_path=PATH)
    print()

    # print download path and program complete
    print(f"Download path: {PATH}")
    print(f"Program completed.")
    time.sleep(1)


if __name__ == "__main__":
    main()