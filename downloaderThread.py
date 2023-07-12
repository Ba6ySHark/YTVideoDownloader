import downloader

from threading import Thread
import time
import os
import glob

class DThread(Thread):
    def __init__(self):
        super().__init__()
        self.logic = None
        self.link = None
        self.resolution = None
        self.file_type = None
        self.video_active = False
        self.audio_active = False
    
    def run(self):
        while True:
            
            if self.video_active:
                downloader.Loader(self.link).downloadVideo(self.resolution)
                self.logic.updateVideoList()
                self.video_active = False
                
                temp_video_files = glob.glob("temp/videos/*")
                for video in temp_video_files:
                    print(video)
                    os.remove(video)
                temp_audio_files = glob.glob("temp/music/*")
                for audio in temp_audio_files:
                    os.remove(audio)
            
            elif self.audio_active:
                downloader.Loader(self.link).downloadAudio(temp=False)
                self.logic.updateAudioList()
                self.audio_active = False
            
            time.sleep(10)
            
