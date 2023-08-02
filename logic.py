from database import DataBase
import customtkinter
import os
import vlc
import time
import tkinter
from threading import Thread, Event

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
        self.audio = None
        self.file_type = "video"
        self.resolution = "144p"
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.mp = self.Instance.media_player_new()
        self.timeslider_last_update = 0
        self.musicslider_last_update = 0
        self.scale_var = tkinter.DoubleVar()
        self.stream = []
        self.log_frames = []
        
        self.timer = ttkTimer(self.updateScale, 1.0)
        self.timer.start()
        self.mp_timer = ttkTimer(self.updateMScale, 1.0)
        self.mp_timer.start()
    
    def downloadVideo(self):
        self.tabView.log_window.delete("0.0", "end")
        if self.file_type == "video":
            try:
                self.tabView.log_window.insert("end", f"Trying to download video from {self.tabView.link_entry.get()}\n")
                self.tabView.thread.link = self.tabView.link_entry.get()
                self.tabView.thread.resolution = self.resolution
                self.tabView.file_type = self.file_type
                self.tabView.thread.logic = self
                self.tabView.thread.video_active = True
            
            except:
                self.tabView.log_window.insert("end", "Unable to download the video file\n")
            
        elif self.file_type == "audio":
            try:
                self.tabView.log_window.insert("end", f"Trying to download an audio from {self.tabView.link_entry.get()}\n")
                self.tabView.thread.link = self.tabView.link_entry.get()
                self.tabView.file_type = self.file_type
                self.tabView.thread.logic = self
                self.tabView.thread.audio_active = True
            except:
                self.tabView.log_window.insert("end", "Unable to download the audio file\n")
            
        
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
            self.tabView.video_list.stream.append((video, frame))
            self.tabView.video_list.stream[i][1].grid(row=i, column=0, padx=10, pady=5)
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
                self.tabView.video_list.stream.append((self.tabView.video_list.videos[i], frame))
                self.tabView.video_list.stream[len(self.tabView.video_list.stream)-1][1].grid(row=len(self.tabView.video_list.stream)-1, column=0, padx=10, pady=5)
    
    def createAudioList(self):
        i = 0
        self.audio_list = os.listdir(self.audio_dir)
        for audio in self.audio_list:
            frame = customtkinter.CTkFrame(master=self.tabView.audio_list, width=320, height=60, corner_radius=15)
            name = audio.split(".")[0]
            db = DataBase()
            try:
                author = list(db.searchItem("Name", f"{audio}"))[0][3]
            except:
                author = "Unknown"
                item = (0, audio, "Not found", author)
                db.addItem(item)
            db.abort()
            if len(name) > 18:
                name = name[:17] + "..."
            if len(author) > 19:
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
            self.stream.append((audio, frame))
            self.stream[i][1].grid(row=i, column=0, padx=10, pady=5)
            i += 1
            
    def updateAudioList(self):
        old_list = self.audio_list[:]
        self.audio_list = os.listdir(self.audio_dir)
        for i in range(len(self.audio_list)):
            if self.audio_list[i] not in old_list:
                frame = customtkinter.CTkFrame(master=self.tabView.audio_list, width=320, height=60, corner_radius=15)
                name = self.audio_list[i].split(".")[0]
                db = DataBase()
                try:
                    author = list(db.searchItem("Name", f"{self.audio_list[i]}"))[0][3]
                except:
                    author = "Unknown"
                    item = (0, audio, "Not found", author)
                    db.addItem(item)
                db.abort()
                if len(name) > 18:
                    name = name[:17] + "..."
                if len(author) > 19:
                    author = author[:19] + "..."
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
                self.stream.append((self.audio_list[i], frame))
                self.stream[len(self.stream)-1][1].grid(row=len(self.stream)-1, column=0, padx=10, pady=5)
                
    def createLogList(self):
        with open("logs.txt", "r") as file:
            array = file.read().split("\n\n")
            for data in array:
                if len(data) > 2:
                    frame = customtkinter.CTkFrame(master=self.tabView.logFrame, corner_radius=15)
                    info = customtkinter.CTkLabel(master=frame, text=data)
                    info.pack(padx=10, pady=10, expand=True, fill="both")
                    frame.pack(padx=10, pady=10, fill="both")
                    self.log_frames.append(frame)
                    
    def updateLogList(self, new_log):
        frame = customtkinter.CTkFrame(master=self.tabView.logFrame, corner_radius=15)
        info = customtkinter.CTkLabel(master=frame, text=new_log)
        info.pack(padx=10, pady=10, expand=True, fill="both")
        frame.pack(padx=10, pady=10, fill="both")
        self.log_frames.append(frame)
    
    def clearLogs(self):
        open("logs.txt", "w").close()
        for frame in self.log_frames:
            frame.destroy()
    
    def getHandle(self):
        return self.tabView.vlc_frame.winfo_id()
    
    def playVideo(self, video):
        self.tabView.video_list.video = video
        try:
            if self.mp.is_playing():
                self.mp.set_pause(1)
                self.tabView.play_button.configure(text="Play ▶")
            self.Media = self.Instance.media_new(f"videos\{self.tabView.video_list.video}")
            self.player.set_media(self.Media)
            self.player.set_hwnd(self.getHandle())
            self.player.play()
            self.setNowPlaying()
            self.tabView.progress_slider.set(-1)
            self.tabView.pause_button.configure(text="Pause ||")
        except:
            print("unable to load the file")
            
    def playAudio(self, audio):
        self.tabView.audPlayer.delete("0.0", "end")
        self.audio = audio
        try:
            db = DataBase()
            lyrics = db.searchItem("Name", f"{audio}")[0][2]
            self.tabView.audPlayer.insert("0.0", lyrics)
            if self.player.is_playing():
                self.player.set_pause(1)
                self.tabView.pause_button.configure(text="Play ▶")
            self.MMedia = self.Instance.media_new(f"music\{self.audio}")
            self.mp.set_media(self.MMedia)
            self.mp.play()
            self.tabView.music_slider.set(-1)
            self.tabView.play_button.configure(text="Pause ||")
            db.abort()
        except:
            print("unabletoload the file")
        
    def deleteVideo(self, video):
        with open("logs.txt", "a") as file:
            try:
                self.player.stop()
                for element in self.tabView.video_list.stream:
                    if video == element[0]:
                        #print(element)
                        element[1].destroy()
                        self.tabView.video_list.stream.remove(element)
                os.remove(f"videos/{video}")
                fb = f"Trying to delete a file at videos/{video}\nDeleting...\nSuccessfully deleted the file!\n\n"
                file.write(fb)
                self.updateLogList(fb)
            except:
                error_message = f"Trying to delete a file at videos/{video}\nDeleting...\nFailed to delete the file.\n\n"
                file.write(error_message)
                self.updateLogList(error_message)
    
    def deleteAudio(self, audio):
        with open("logs.txt", "a") as file:
            try:
                self.mp.stop()
                for element in self.stream:
                    if audio == element[0]:
                        element[1].destroy()
                        self.stream.remove(element)
                db = DataBase()
                db.deleteItem(audio)
                db.abort()
                os.remove(f"music/{audio}")
                fb = f"Trying to delete a file at music/{audio}\nDeleting...\nSuccessfully deleted the file!\n\n"
                file.write(fb)
                self.updateLogList(fb)
            except:
                error_message = f"Trying to delete a file at music/{audio}\nDeleting...\nFailed to delete the file.\n\n"
                file.write(error_message)
                self.updateLogList(error_message)
    
    def nextAudio(self):
        if self.audio and (self.audio in self.audio_list):
            index = self.audio_list.index(self.audio)
            next_index = (index + 1)%(len(self.audio_list))
            self.stopMp()
            self.playAudio(self.audio_list[next_index])
        else:
            pass
    
    def previousAudio(self):
        if self.audio and (self.audio in self.audio_list):
            index = self.audio_list.index(self.audio)
            previous_index = (index - 1)
            if previous_index < 0:
                previous_index = len(self.audio_list) - 1
            self.stopMp()
            self.playAudio(self.audio_list[previous_index])
        else:
            pass
                
    def stop(self):
        self.player.stop()
        self.tabView.progress_slider.set(-1)
    
    def stopMp(self):
        self.mp.stop()
        self.tabView.music_slider.set(-1)
        self.tabView.audPlayer.delete("0.0", "end")
        
    def playPause(self):
        if self.tabView.video_list.video:
            if not bool(self.player.is_playing()):
                self.mp.set_pause(1)
                self.tabView.play_button.configure(text="Play ▶")
                self.player.play()
                self.tabView.pause_button.configure(text="Pause ||")
            else:
                self.player.set_pause(1)
                self.tabView.pause_button.configure(text="Play ▶")
        
    def playMPause(self):
        if self.audio:
            if not bool(self.mp.is_playing()):
                self.player.set_pause(1)
                self.tabView.pause_button.configure(text="Play ▶")
                self.mp.play()
                self.tabView.play_button.configure(text="Pause ||")
            else:
                self.mp.set_pause(1)
                self.tabView.play_button.configure(text="Play ▶")
    
    def updateScale(self):
        if self.player == None:
            return
        else:
            try:
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
            except:
                pass
            
    def updateMScale(self):
        if self.mp == None:
            return
        else:
            try:
                length = self.mp.get_length()
                dbl = length * 0.001
                self.tabView.music_slider.configure(to=dbl)
                
                tyme = self.mp.get_time()
                if tyme == -1:
                    tume = 0
                dbl = tyme * 0.001
                self.musicslider_last_val = ("%.0f" % dbl) + ".0"
                
                if time.time() > (self.musicslider_last_update + 2.0):
                    self.tabView.music_slider.set(dbl+0.001)
            except:
                pass
        
    def seekSliderValue(self, value):
        if self.player == None:
            return
        if self.tabView.video_list.video:
            try:
                self.timeslider_last_update = time.time()
                mval = self.tabView.progress_slider.get()
                self.player.set_time(int(mval)*1000)
            except:
                print("failed")
                
    def seekMSliderValue(self, value):
        if self.mp == None:
            return
        if self.audio:
            try:
                self.musicslider_last_update = time.time()
                mval = self.tabView.music_slider.get()
                self.mp.set_time(int(mval)*1000)
            except:
                print("failed")
         
    '''
    def updateDuration(self, event):
        try:
            duration = int(self.tabView.vidPlayer.video_info()["duration"])
            self.tabView.progress_slider.configure(from_=-1, to=duration, number_of_steps=duration)
        except:
            pass
    
    def updateMDuration(self, event):
        try:
            duration = int(self.mp.video_info()["duration"])
            self.tabView.music_slider.configure(from_=-1, to=duration, number_of_steps=duration)
        except:
            pass
    '''
        
    def videoEnded(self, event):
        self.tabView.pause_button.configure(text="Play ►")
        self.tabView.progress_slider.set(-1)
        
    def setNowPlaying(self):
        title = self.tabView.video_list.video.split('.')[0]
        if len(title) <= 56:
            self.tabView.now_playing.configure(text=f"Now playing: {title}")
        else:
            title = title[:53] + "..."
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