import downloader
from database import DataBase
import customtkinter
import os
import vlc
import time
import tkinter
from threading import Timer, Thread, Event

class ttkTimer(Thread):
    #a class serving same function as wxTimer... but there may be better ways to do this
    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        #print("callback= ", callback())
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()
            #print("ttkTimer start")

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters

class Logic:
    def __init__(self, tabView):
        self.tabView = tabView
        self.dir = "videos"
        self.audio_dir = "music"
        self.file_type = "video"
        self.resolution = "144p"
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.mp = self.Instance.media_player_new()
        self.timeslider_last_update = 0
        self.scale_var = tkinter.DoubleVar()
        self.stream = []
        
        self.timer = ttkTimer(self.updateScale, 1.0)
        self.timer.start()
        self.mp_timer = ttkTimer(self.updateMScale, 1.0)
        self.mp_timer.start()
    
    def downloadVideo(self):
        if self.file_type == "video":
            try:
                self.tabView.thread.link = self.tabView.link_entry.get()
                self.tabView.thread.resolution = self.resolution
                self.tabView.file_type = self.file_type
                self.tabView.thread.logic = self
                self.tabView.thread.video_active = True
                print("done")
            
            except:
                pass
            
        elif self.file_type == "audio":
            try:
                self.tabView.thread.link = self.tabView.link_entry.get()
                self.tabView.file_type = self.file_type
                self.tabView.thread.logic = self
                self.tabView.thread.audio_active = True
                print("done")
                #downloader.Loader(self.tabView.link_entry.get()).downloadAudio()
                #self.tabView.music_list.updateMusicList()
            except:
                pass
            
        
    def clearEntry(self):
        self.tabView.link_entry.delete(0, len(self.tabView.link_entry.get()))
        
    def createVideoList(self):
        i = 0
        for video in self.tabView.video_list.videos:
            frame = customtkinter.CTkFrame(master=self.tabView.video_list, width=320, height=60, corner_radius=15)
            name = video.split(".")[0]
            if len(name) > 18:
                name = name[:18] + "..."
            form = video.split(".")[1].upper()
            form_label = customtkinter.CTkLabel(master=frame, text=form, width=40, height=40, corner_radius=5, fg_color="gray", text_color="white")
            form_label.place(x=10, y=10)
            name_label = customtkinter.CTkLabel(master=frame, text=name, width=150, height=40, corner_radius=5, anchor="w", font=("Calibri", 17))
            name_label.place(x=60, y=10)
            play_button = customtkinter.CTkButton(master=frame, text="Play", width=40, height=40, corner_radius=5, font=("Calibri", 17), command=lambda video=video: self.playVideo(video))
            play_button.place(x=220, y=10)
            delete_button = customtkinter.CTkButton(master=frame, text="Del", width=40, height=40, corner_radius=5, font=("Calibri", 17), command=lambda video=video: self.deleteVideo(video))
            delete_button.place(x=270, y=10)
            self.tabView.video_list.stream.append(frame)
            self.tabView.video_list.stream[i].grid(row=i, column=0, padx=10, pady=5)
            i += 1
            
    def updateVideoList(self):
        old_list = self.tabView.video_list.videos[:]
        self.tabView.video_list.videos = os.listdir(self.dir)
        for i in range(len(self.tabView.video_list.videos)):
            if self.tabView.video_list.videos[i] not in old_list:
                frame = customtkinter.CTkFrame(master=self.tabView.video_list, width=320, height=60, corner_radius=15)
                name = self.tabView.video_list.videos[i].split(".")[0]
                if len(name) > 18:
                    name = name[:18] + "..."
                form = self.tabView.video_list.videos[i].split(".")[1].upper()
                form_label = customtkinter.CTkLabel(master=frame, text=form, width=40, height=40, corner_radius=5, fg_color="gray", text_color="white")
                form_label.place(x=10, y=10)
                name_label = customtkinter.CTkLabel(master=frame, text=name, width=150, height=40, corner_radius=5, anchor="w", font=("Calibri", 17))
                name_label.place(x=60, y=10)
                play_button = customtkinter.CTkButton(master=frame, text="Play", width=40, height=40, corner_radius=5, font=("Calibri", 17), command=lambda video=self.tabView.video_list.videos[i]: self.playVideo(video))
                play_button.place(x=220, y=10)
                delete_button = customtkinter.CTkButton(master=frame, text="Del", width=40, height=40, corner_radius=5, font=("Calibri", 17), command=lambda video=self.tabView.video_list.videos[i]: self.deleteVideo(video))
                delete_button.place(x=270, y=10)
                self.tabView.video_list.stream.append(frame)
                self.tabView.video_list.stream[len(self.tabView.video_list.stream)-1].grid(row=len(self.tabView.video_list.stream)-1, column=0, padx=10, pady=5)
    
    def createAudioList(self):
        i = 0
        self.audio_list = os.listdir(self.audio_dir)
        for audio in self.audio_list:
            frame = customtkinter.CTkFrame(master=self.tabView.audio_list, width=320, height=60, corner_radius=15)
            name = audio.split(".")[0]
            db = DataBase()
            author = list(db.searchItem("Name", f"{audio}"))[0][3]
            db.abort()
            if len(name) > 18:
                name = name[:18] + "..."
            if len(author) > 18:
                author = author[:18] + "..."
            form = audio.split(".")[1].upper()
            form_label = customtkinter.CTkLabel(master=frame, text=form, width=40, height=40, corner_radius=5, fg_color="gray", text_color="white")
            form_label.place(x=10, y=10)
            name_label = customtkinter.CTkLabel(master=frame, text=name, width=150, height=20, corner_radius=5, anchor="w", font=("Calibri", 17))
            name_label.place(x=60, y=10)
            author_label = customtkinter.CTkLabel(master=frame, text=author, width=150, height=20, corner_radius=5, anchor="w", font=("Calibri", 15))
            author_label.place(x=60, y=30)
            play_button = customtkinter.CTkButton(master=frame, text="Play", width=40, height=40, corner_radius=5, font=("Calibri", 17), command=lambda audio=audio: self.playAudio(audio))
            play_button.place(x=220, y=10)
            delete_button = customtkinter.CTkButton(master=frame, text="Del", width=40, height=40, corner_radius=5, font=("Calibri", 17), command=lambda audio=audio: self.deleteAudio(audio))
            delete_button.place(x=270, y=10)
            self.stream.append(frame)
            self.stream[i].grid(row=i, column=0, padx=10, pady=5)
            i += 1
            
    def updateAudioList(self):
        old_list = self.audio_list[:]
        self.audio_list = os.listdir(self.audio_dir)
        for i in range(len(self.audio_list)):
            if self.audio_list[i] not in old_list:
                frame = customtkinter.CTkFrame(master=self.tabView.audio_list, width=320, height=60, corner_radius=15)
                name = self.audio_list[i].split(".")[0]
                db = DataBase()
                author = list(db.searchItem("Name", f"{self.audio_list[i]}"))[0][3]
                db.abort()
                if len(name) > 18:
                    name = name[:18] + "..."
                if len(author) > 18:
                    author = author[:18] + "..."
                form = self.audio_list[i].split(".")[1].upper()
                form_label = customtkinter.CTkLabel(master=frame, text=form, width=40, height=40, corner_radius=5, fg_color="gray", text_color="white")
                form_label.place(x=10, y=10)
                name_label = customtkinter.CTkLabel(master=frame, text=name, width=150, height=20, corner_radius=5, anchor="w", font=("Calibri", 17))
                name_label.place(x=60, y=10)
                author_label = customtkinter.CTkLabel(master=frame, text=author, width=150, height=20, corner_radius=5, anchor="w", font=("Calibri", 15))
                author_label.place(x=60, y=30)
                play_button = customtkinter.CTkButton(master=frame, text="Play", width=40, height=40, corner_radius=5, font=("Calibri", 17), command=lambda audio=self.audio_list[i]: self.playAudio(audio))
                play_button.place(x=220, y=10)
                delete_button = customtkinter.CTkButton(master=frame, text="Del", width=40, height=40, corner_radius=5, font=("Calibri", 17), command=lambda audio=self.audio_list[i]: self.deleteAudio(audio))
                delete_button.place(x=270, y=10)
                self.stream.append(frame)
                self.stream[len(self.stream)-1].grid(row=len(self.stream)-1, column=0, padx=10, pady=5)
    
    def getHandle(self):
        return self.tabView.vlc_frame.winfo_id()
    
    def playVideo(self, video):
        self.tabView.video_list.video = video
        try:
            self.Media = self.Instance.media_new(f"videos\{self.tabView.video_list.video}")
            self.player.set_media(self.Media)
            self.player.set_hwnd(self.getHandle())
            self.player.play()
            self.setNowPlaying()
            self.tabView.progress_slider.set(-1)
            self.tabView.pause_button.configure(text="Pause ||")
        except:
            print("unable to load the file")
            
    def deleteVideo(self, video):
        self.player.stop()
        print("deleted " + video)
        
    def playAudio(self, audio):
        pass
    
    def deleteAudio(self, audio):
        pass
            
    def stop(self):
        self.player.stop()
        self.tabView.progress_slider.set(-1)
        
    def playPause(self):
        if self.tabView.video_list.video:
            if not bool(self.player.is_playing()):
                self.player.play()
                self.tabView.pause_button.configure(text="Pause ||")
            else:
                self.player.set_pause(1)
                self.tabView.pause_button.configure(text="Play ▶")
    
    def updateScale(self):
        if self.player == None:
            return
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        length = self.player.get_length()
        dbl = length * 0.001
        self.tabView.progress_slider.configure(to=dbl)

        # update the time on the slider
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"
        # don't want to programatically change slider while user is messing with it.
        # wait 2 seconds after user lets go of slider
        if time.time() > (self.timeslider_last_update + 2.0):
            self.tabView.progress_slider.set(dbl)
            
    def updateMScale(self):
        pass
        
    def seekSliderValue(self, value):
        if self.player == None:
            return
        current_val = str(self.tabView.progress_slider.get())
        if self.tabView.video_list.video:
            try:
                self.timeslider_last_update = time.time()
                mval = self.tabView.progress_slider.get()
                self.player.set_time(int(mval)*1000)
            except:
                print("failed")
            
    def updateDuration(self, event):
        try:
            duration = int(self.tabView.vidPlayer.video_info()["duration"])
            self.tabView.progress_slider.configure(from_=-1, to=duration, number_of_steps=duration)
        except:
            pass
        
    def videoEnded(self, event):
        self.tabView.pause_button.configure(text="Play ►")
        self.tabView.progress_slider.set(-1)
        
    def setNowPlaying(self):
        title = self.tabView.video_list.video.split('.')[0]
        if len(title) <= 60:
            self.tabView.now_playing.configure(text=f"Now playing: {title}")
        else:
            title = title[:56] + "..."
            self.tabView.now_playing.configure(text=f"Now playing: {title}")
        
    def setFileType(self, event):
        state = self.tabView.folder_type_options.get()
        if state == "Music":
            self.tabView.video_resolution_select.configure(state="disabled")
            self.file_type = "audio"
        elif state == "Video":
            self.tabView.video_resolution_select.configure(state="normal")
            self.file_type = "video"
            
    def setResolution(self, event=None):
        value = self.tabView.video_resolution_select.get()
        self.resolution = value
        return value