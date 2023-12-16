from pytube import Playlist
import tkinter as tk
from tkinter import ttk
import os

def download_videos():
    url = url_entry.get()
    max_resolution = resolution_var.get()
    download_playlist(url, download_folder, max_resolution)

def download_playlist(url, download_folder, max_resolution):
    playlist = Playlist(url)
    for video in playlist.videos:
        try:
            file_path = os.path.join(download_folder, f"{video.title}.mp4")
            if not os.path.exists(file_path):
                if max_resolution == "Highest":
                    stream = video.streams.get_highest_resolution()
                else:
                    stream = video.streams.filter(res=max_resolution).first() or video.streams.get_highest_resolution()
                stream.download(download_folder)
                print(f"Downloaded: {video.title}")
            else:
                print(f"Already exists: {video.title}")
        except Exception as e:
            print(f"Failed to download {video.title}: {e}")

# Tkinter GUI setup
root = tk.Tk()
root.title("YouTube Playlist Downloader")

# URL entry
tk.Label(root, text="Playlist URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Resolution selection
tk.Label(root, text="Max Resolution:").pack()
resolution_var = tk.StringVar()
resolution_var.set("Highest")  # default value
resolution_choices = ["Highest", "1080p", "720p", "480p", "360p", "240p"]
resolution_menu = ttk.Combobox(root, textvariable=resolution_var, values=resolution_choices)
resolution_menu.pack()

# Download folder - hardcoded for simplicity, can be made dynamic with a folder dialog
download_folder = 'C:/Users/Pkram/OneDrive/Desktop/songs'

# Download button
download_button = tk.Button(root, text="Download", command=download_videos)
download_button.pack()

# Run the application
root.mainloop()
