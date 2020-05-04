# Made by David O in 1 night
#(c) 2020 David
# This code is licensed under Apache license (see LICENSE.txt for details)

# Imports
from pytube import YouTube 
import sys
from bs4 import BeautifulSoup
import urllib3
import regex
from pathlib import Path
from sys import platform as _platform
import socket

# Playlists 
def downloadPlaylist():

    # Stores array of urls 
    playlistVideoLinks = [] 

    # Initalization
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

    # Gets each url
    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            playlistVideoLinks.append(domain + href + '\n')

    # Stops download if Ctrl + C without error
    try:
        for video in playlistVideoLinks:
            processVideo(video, True)  
    except KeyboardInterrupt:
        print("Stopping Downlaods!")

# Single video
def downloadVideo():
    
    #Initalization
    while True:
        videoLink = input("Video Link: ")
        processVideo(videoLink)

        if(videoLink.lower() == "exit"):
            exit()
        break

# Downloads videos
def processVideo(link=None, isPlaylist=False):

    # Stores possible resolutions
    videoResolution = []

    # Creates a Youtube Object
    yt = YouTube(link)

    # If it is not a playlist video 
    if not isPlaylist:

        # Filters for progressive mp4s
        while True:
            for stream in yt.streams.filter(progressive=True, file_extension='mp4'):
                if(stream.resolution == None):
                    pass
                else:
                    videoResolution.append(stream.resolution)
            list(dict.fromkeys('videoResolution'))
        
            # Gives user the ability to pick resolution
            print("----Choose Resolution----")
            print("Pick: {}".format(videoResolution))
            videoResolution.clear()

            reso = input("(ex. 1080p) \n >>")

            stream = yt.streams.filter(res=reso, file_extension='mp4', progressive=True).first()

            # Gets title
            title = yt.title

            if sream == None: 
                print("No video of that quality!")
            else:
            # Output : This video is 00:00:00 minutes long and 0 MiBs. Are you sure you want to download?
                message = "This video is {:02d}:{:02d}:{:02d} minutes long and {} MiBs. Are you sure you want to download? (y/n): ".format(round(yt.length / 3600), round(yt.length / 60), yt.length % 60, round(stream.filesize / 1.049e+6))
                choice = input(message)

                # Determines choice
                if(choice.lower() == "y" or choice.lower() == "yes"):
                    print ("Fetching: {}...".format(title)) 
                    stream.download(output_path=path)
                    break
                else:
                    print("Bye!")
                    break 
                    exit()
    # If it is a playlist video
    else:
        # Strange issue where it downloads Youtube.mp4 
        if yt.title != "YouTube":
            stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
            title = yt.title
            # Output : Fetching [Video Name] - 00:00:00 - 0 MiBs...
            print ("Fetching: {} - {:02d}:{:02d}:{: 02d} - {} MiBs...".format(title, round(yt.length / 3600), round(yt.length / 60), yt.length % 60, round(stream.filesize / 1.049e+6)))
            stream.download(output_path=path)

# If no save point will result in default      
def defaultSave():
    global path

    # Finds hostname of computer
    hostname = socket.gethostname()

    # Dependant on that hostname it will save to the OS' Videos file
    if _platform == "linux" or _platform == "linux2":
        path = "/home/{}/Videos".format(hostname)
    elif _platform == "darwin":
        path = "/home/{}/Videos".format(hostname)
    elif _platform == "win32" or _platform == "win64":
        path = r"\Users\{}\Videos".format(hostname)

# main
def main():
    global path

    # Initalization
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
    # Outputs save location
    print("Save Location: " + path)

if __name__ == "__main__":
    main()
