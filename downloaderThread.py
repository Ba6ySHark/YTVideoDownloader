import downloader

from threading import Thread
import webbrowser as wb
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
                self.logic.tabView.download_button.configure(state="disabled")
                downloader.Loader(self.link).downloadVideo(self.resolution, self.logic.tabView.log_window)
                self.logic.updateVideoList()
                self.logic.tabView.log_window.insert("end", "Video list has been updated\n")
                self.video_active = False
                self.logic.tabView.download_button.configure(state="normal")
                self.logic.tabView.log_window.insert("end", "Successfully downloaded a file!\n\n")
                self.logic.clearEntry()
                
                if self.logic.tabView.show_file_select.get() == "Yes":
                    wb.open("videos")
                
                with open("logs.txt", "a") as file:
                    activity = self.logic.tabView.log_window.get("0.0", "end")
                    print(activity)
                    file.write(activity)
                    self.logic.updateLogList(activity)
                
                temp_video_files = glob.glob("temp/videos/*")
                for video in temp_video_files:
                    #print(video)
                    os.remove(video)
                temp_audio_files = glob.glob("temp/music/*")
                for audio in temp_audio_files:
                    os.remove(audio)
            
            elif self.audio_active:
                self.logic.tabView.download_button.configure(state="disabled")
                downloader.Loader(self.link).downloadAudio(temp=False, log=self.logic.tabView.log_window)
                self.logic.updateAudioList()
                self.logic.tabView.log_window.insert("end", "Music list has been updated\n")
                self.audio_active = False
                self.logic.tabView.download_button.configure(state="normal")
                self.logic.tabView.log_window.insert("end", "Successfully downloaded a file!\n\n")
                self.logic.clearEntry()
                
                if self.logic.tabView.show_file_select.get() == "Yes":
                    wb.open("music")
                
                with open("logs.txt", "a") as file:
                    activity = self.logic.tabView.log_window.get("0.0", "end")
                    file.write(activity)
                    self.logic.updateLogList(activity)
            
            time.sleep(10)
            
