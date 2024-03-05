from pytube import Playlist, YouTube
import tkinter as tk
from tkinter import ttk, scrolledtext
import os
import webbrowser

def download():
    url = url_entry.get()
    max_resolution = resolution_var.get()
    download_type = download_type_var.get()
    if download_type == 'Playlist':
        download_playlist(url, folder_entry.get(), max_resolution)
    elif download_type == 'Single Video':
        download_video(url, folder_entry.get(), max_resolution)
    elif download_type == 'Audio':
        download_audio(url, folder_entry.get())

def download_playlist(url, download_folder, max_resolution):
    playlist = Playlist(url)
    output_text.delete('1.0', tk.END)
    for video in playlist.videos:
        download_video(video.watch_url, download_folder, max_resolution)

def download_video(url, download_folder, max_resolution):
    try:
        video = YouTube(url)
        file_path = os.path.join(download_folder, f"{video.title}.mp4")
        if not os.path.exists(file_path):
            if max_resolution == "Highest":
                stream = video.streams.get_highest_resolution()
            else:
                stream = video.streams.filter(res=max_resolution).first() or video.streams.get_highest_resolution()
            stream.download(download_folder)
            output_text.insert(tk.END, f"Downloaded: {video.title}\n")
        else:
            output_text.insert(tk.END, f"Already exists: {video.title}\n")
    except Exception as e:
        output_text.insert(tk.END, f"Failed to download {video.title}: {e}\n")

def download_audio(url, download_folder):
    try:
        video = YouTube(url)
        file_path = os.path.join(download_folder, f"{video.title}.mp3")
        if not os.path.exists(file_path):
            stream = video.streams.filter(only_audio=True).first()
            stream.download(download_folder, filename=f"{video.title}.mp3")
            output_text.insert(tk.END, f"Downloaded audio: {video.title}\n")
        else:
            output_text.insert(tk.END, f"Audio already exists: {video.title}\n")
    except Exception as e:
        output_text.insert(tk.END, f"Failed to download audio {video.title}: {e}\n")

def open_browser():
    webbrowser.open_new(url_entry.get())

# Tkinter GUI setup
root = tk.Tk()
root.title("YouTube Downloader")

# URL entry
tk.Label(root, text="URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Download Type
tk.Label(root, text="Download Type:").pack()
download_type_var = tk.StringVar()
download_type_var.set("Playlist")  # default value
download_type_choices = ["Playlist", "Single Video", "Audio"]
download_type_menu = ttk.Combobox(root, textvariable=download_type_var, values=download_type_choices)
download_type_menu.pack()

# Resolution selection
tk.Label(root, text="Max Resolution:").pack()
resolution_var = tk.StringVar()
resolution_var.set("Highest")  # default value
resolution_choices = ["Highest", "1080p", "720p", "480p", "360p", "240p"]
resolution_menu = ttk.Combobox(root, textvariable=resolution_var, values=resolution_choices)
resolution_menu.pack()

# Download folder entry
tk.Label(root, text="Download Folder:").pack()
folder_entry = tk.Entry(root, width=50)
folder_entry.pack()

# Download and Preview buttons
download_button = tk.Button(root, text="Download", command=download)
download_button.pack()

preview_button = tk.Button(root, text="Preview", command=open_browser)
preview_button.pack()

# Output text area
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
output_text.pack()

# Run the application
root.mainloop()
