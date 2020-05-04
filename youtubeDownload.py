from pytube import YouTube 
import sys
from bs4 import BeautifulSoup
import urllib3
import regex
from pathlib import Path
from sys import platform as _platform
import socket

def downloadPlaylist():
    playlistVideoLinks = [] 

    while True:
        try:
            playlistLink = input("Playlist Link: ")

            http = urllib3.PoolManager()

            page = http.request('GET', playlistLink)
            soup = BeautifulSoup(page.data, features="lxml")
            domain = 'https://www.youtube.com'
        except:
            if(playlistLink.lower() == "exit"):
                exit() 
            print("Something went wrong!")
            continue
        break

    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            playlistVideoLinks.append(domain + href + '\n')
    try:
        for video in playlistVideoLinks:
            processVideo(video, True)  
    except KeyboardInterrupt:
        print("Stopping Downlaods!")

def downloadVideo():
    while True:
        videoLink = input("Video Link: ")
        processVideo(videoLink)

        if(videoLink.lower() == "exit"):
            exit()
        break

def processVideo(link=None, isPlaylist=False):
    videoResolution = []

    yt = YouTube(link)

    if not isPlaylist:
        while True:
            for stream in yt.streams.filter(progressive=True, file_extension='mp4'):
                if(stream.resolution == None):
                    pass
                else:
                    videoResolution.append(stream.resolution)
            list(dict.fromkeys('videoResolution'))
        
            print("----Choose Resolution----")
            print("Pick: {}".format(videoResolution))
            videoResolution.clear()

            reso = input("(ex. 1080p) \n >>")

            stream = yt.streams.filter(res=reso, file_extension='mp4', progressive=True).first()

            title = yt.title

            if sFalsetream == None: 
                print("No video of that quality!")
            else:
                message = "This video is {:02d}:{:02d}:{:02d} minutes long and {} MiBs. Are you sure you want to download? (y/n): ".format(round(yt.length / 3600), round(yt.length / 60), yt.length % 60, round(stream.filesize / 1.049e+6))
                choice = input(message)

                if(choice.lower() == "y" or choice.lower() == "yes"):
                    print ("Fetching: {}...".format(title)) 
                    stream.download(output_path=path)
                    break
                else:
                    print("Bye!")
                    break 
                    exit()
    else:
        if yt.title != "YouTube":
            stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
            title = yt.title
            print ("Fetching: {} - {:02d}:{:02d}:{: 02d} - {} MiBs...".format(title, round(yt.length / 3600), round(yt.length / 60), yt.length % 60, round(stream.filesize / 1.049e+6)))
            stream.download(output_path=path)
        
def defaultSave():
    global path
    hostname = socket.gethostname()

    if _platform == "linux" or _platform == "linux2":
        path = "/home/{}/Videos".format(hostname)
    elif _platform == "darwin":
        path = "/home/{}/Videos".format(hostname)
    elif _platform == "win32" or _platform == "win64":
        path = r"\Users\{}\Videos".format(hostname)

def main():
    global path
    while True:
        options = input("Do you want to download a [P]laylist or [V]ideo? (Type 'exit' at any point to quit): ")
        if options.lower() == "v" or options.lower() == "video":
            path = input("Copy the path where you want to save this video? (Click enter for default save): ")
            
            if not path:
                defaultSave()

            Path(path).mkdir(parents=True, exist_ok=True)
            downloadVideo()

        elif options.lower() == "p" or options.lower() == "playlist":
            path = input("Copy the path where you want to save this video? (Leave empty for default save)")

            if not path:
                defaultSave()

            Path(path).mkdir(parents=True, exist_ok=True)
            downloadPlaylist()
        elif options.lower() == "exit":
            exit()
        else:
            continue
        break
    print("Save Location: " + path)

if __name__ == "__main__":
    main()