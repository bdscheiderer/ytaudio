# This program download video and audio from a Youtube video

import sys
from pytubefix import YouTube
from pytubefix.cli import on_progress

# option to hard code download path
# if PATH = None, will dl to same directory as program is run from
# PATH = "your/download/path"
PATH = None


def main():

    # get user input for youtube video url
    url =  input("Enter Youtube url:")

    # verify url entered 
    print(f"Video url: {url}")

    # get yt object or exit if not found
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
    except:
        print(f'Error: video {url} is unavaialable.')
        sys.exit(0)
    else:
        print(f"Video found: {yt.title}")

    # ask if should download video and audio ("y") 
    # default "n" will downlonad audio file only
    try:
        message = "Download video along with audio? (y/n) "
        video_dl = (input(message)).lower()
    except:
        video_dl = "n"
        
    # option to download video...first resolution stream
    if video_dl == "y":
        print("Downloading Video...")
        yt.streams.first().download(output_path=PATH)
        print()

    # download audio (currently .m4a file)
    print(f"Downloading Audio...")
    ys = yt.streams.get_audio_only()
    ys.download(output_path=PATH)
    print()

    # print download path and program complete
    print(f"Download path: {PATH}")
    print(f"Program Completed")


if __name__ == "__main__":
    main()