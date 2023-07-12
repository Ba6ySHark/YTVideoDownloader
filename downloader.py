from database import DataBase
from lyricsscraper import Scraper

from pytube import YouTube, Playlist
import os
import pathlib
from moviepy.editor import *
# pytube git: https://github.com/oncename/pytube/tree/master

class Loader:
    def __init__(self, url):
        self.video = YouTube(url)
        self.videos_dir = "videos"
        self.music_dir = "music"
    
    def update_url(self, new_url):
        self.video = YouTube(new_url)
        
    def downloadVideo(self, resolution="144p"):
        print(self.video.streams.filter(res=resolution, progressive=True))
        if len(self.video.streams.filter(res=resolution, progressive=True)) != 0:
            self.video.streams.filter(res=resolution).first().download(self.videos_dir)
        else:
            vid = self.video.streams.filter(res=resolution).first().download(f"temp/{self.videos_dir}").split("/")[-1]
            print(vid)
            aud = self.downloadAudio(True)
            vclip = VideoFileClip(f"temp/{vid}")
            aclip = AudioFileClip(f"temp/{aud}")
            final = vclip.set_audio(aclip)
            final.write_videofile(os.path.join(self.videos_dir, f"{self.video.title}.mp4"), fps=30, threads=1, codec="libx264")
        
    def downloadAudio(self, temp=False):
        downloaded_file = ""
        if temp:
            music_directory = f"temp/{self.music_dir}"
            downloaded_file = self.video.streams.filter(only_audio=True).first().download(music_directory).split("/")[-1]
        else:
            music_directory = self.music_dir
            downloaded_file = self.video.streams.filter(only_audio=True).first().download(music_directory).split("/")[-1]
            os.rename(f"{downloaded_file}", (downloaded_file.split(".")[0] + ".mp3"))
            downloaded_file = downloaded_file.split(".")[0] + ".mp3"
            db = DataBase()
            data_len = db.getLength()
            lyrics = Scraper().get_lyrics(self.video.title, self.video.author)
            title = pathlib.PurePath(downloaded_file)
            #print(title.name)
            #print(lyrics, self.video.title, self.video.author)
            item = (data_len, f"{title.name}", f"{lyrics}", f"{self.video.author}")
            db.addItem(item)
            db.abort()
        return downloaded_file
    