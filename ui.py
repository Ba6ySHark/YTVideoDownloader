import downloader
import logic

import tkinter
import customtkinter
from tkVideoPlayer import TkinterVideo
import os
import vlc

class ScrollFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.dir = "videos"
        self.video = None
        self.videos = os.listdir(self.dir)
        self.stream = []

class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, app, thread, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.thread = thread
        
        self.add("Download")
        self.add("Videos")
        self.add("Music")
        self.add("Completed tasks")
        
        lg = logic.Logic(self)
        
        #Download page (1)
        self.empty_space_left = customtkinter.CTkFrame(master=self.tab("Download"), fg_color="transparent")
        self.empty_space_left.pack(padx=10, pady=10, expand=True, side=customtkinter.LEFT)
        self.downloader_frame = customtkinter.CTkFrame(master=self.tab("Download"), width=575, fg_color="transparent")
        self.top = customtkinter.CTkFrame(master=self.downloader_frame, width=575, height=140, fg_color="transparent")
        self.link_entry = customtkinter.CTkEntry(master=self.top, width=400, height=30, corner_radius=5, placeholder_text="Enter your youtube url here...")
        self.link_entry.place(x=0, y=40)
        self.download_button = customtkinter.CTkButton(master=self.top, width=60, height=30, corner_radius=5, text="Download")
        self.download_button.place(x=420, y=40)
        self.clear_button = customtkinter.CTkButton(master=self.top, width=60, height=30, corner_radius=5, text="Clear")
        self.clear_button.place(x=510, y=40)
        self.folder_type_label = customtkinter.CTkLabel(master=self.top, text="File type: ", fg_color="transparent", width=75, height=30)
        self.folder_type_label.place(x=0, y=90)
        self.folder_type_options = customtkinter.CTkOptionMenu(master=self.top, values=["Video", "Music"], width=75, height=30, corner_radius=5, command=lg.setFileType)
        self.folder_type_options.place(x=95, y=90)
        self.video_resolution = customtkinter.CTkLabel(master=self.top, text="Resolution: ", fg_color="transparent", width=75, height=30)
        self.video_resolution.place(x=190, y=90)
        self.video_resolution_select = customtkinter.CTkOptionMenu(master=self.top, values=["144p", "240p", "360p", "480p", "720p", "1080p"], width=75, height=30, corner_radius=5, command=lg.setResolution)
        self.video_resolution_select.place(x=285, y=90)
        self.show_file_label = customtkinter.CTkLabel(master=self.top, text="Open in File Manager: ", fg_color="transparent", width=95, height=30)
        self.show_file_label.place(x=380, y=90)
        self.show_file_select = customtkinter.CTkOptionMenu(master=self.top, values=["Yes", "No"], width=55, height=30, corner_radius=5)
        self.show_file_select.place(x=510, y=90)
        self.top.pack(padx=0, pady=0)
        self.log_window = customtkinter.CTkTextbox(master=self.downloader_frame, width=570, height=425, corner_radius=15, state="disabled")
        self.log_window.pack(padx=0, pady=0, expand=True, fill="both")
        self.downloader_frame.pack(padx=10, pady=10, side=customtkinter.LEFT, fill="both")
        self.empty_space_right = customtkinter.CTkFrame(master=self.tab("Download"), fg_color="transparent")
        self.empty_space_right.pack(padx=10, pady=10, expand=True, side=customtkinter.LEFT)
        
        #Videos page (2)
        self.playerFrame = customtkinter.CTkFrame(master=self.tab("Videos"), corner_radius=15) #width=850, height=580
        self.playerFrame.pack(padx=10, pady=10, fill="both", expand=True, side=customtkinter.LEFT)
        #self.vidPlayer = TkinterVideo(master=self.playerFrame, scaled=True, keep_aspect=True, consistant_frame_rate=True, bg="black")
        #self.vidPlayer.set_resampling_method(1)
        self.vlc_frame = customtkinter.CTkFrame(master=self.playerFrame)
        self.vlc_frame.pack(padx=20, pady=20, fill=customtkinter.BOTH, expand=True)
        self.vidPlayer = tkinter.Canvas(self.vlc_frame, bg="black", highlightthickness=0).pack(fill=tkinter.BOTH, expand=True)
        #self.vidPlayer.pack(padx=20, pady=20, expand=True, fill="both")
        self.progress_slider = customtkinter.CTkSlider(master=self.playerFrame, from_=0, to=1000) #width=810
        self.progress_slider.set(-1)
        self.progress_slider.pack(fill="both", padx=20, pady=0)
        self.status_frame = customtkinter.CTkFrame(master=self.playerFrame, height=50, fg_color="transparent")
        self.status_frame.pack(padx=20, pady=20, fill="both")
        self.pause_button = customtkinter.CTkButton(master=self.status_frame, width=85, text="Play ▶")
        self.pause_button.pack(pady=10, padx=10, side=customtkinter.LEFT)
        self.stop_button = customtkinter.CTkButton(master=self.status_frame, width=85, text="Stop ☐", fg_color="red",command=lg.stop)
        self.stop_button.pack(pady=10, padx=10, side=customtkinter.LEFT)
        self.now_playing = customtkinter.CTkLabel(master=self.status_frame, text="Now playing: ", fg_color="transparent", font=("Trebuchet MS", 17))
        self.now_playing.pack(padx=10, pady=10, expand=True, side=customtkinter.LEFT)
        self.video_list = ScrollFrame(self.tab("Videos"), width=340)
        lg.createVideoList()
        self.video_list.pack(padx=10, pady=10, fill="both", side=customtkinter.LEFT)
        
        self.clear_button.configure(command=lg.clearEntry)
        self.download_button.configure(command=lg.downloadVideo)
        
        self.progress_slider.configure(command=lg.seekSliderValue)
        self.pause_button.configure(command=lg.playPause)
        
        
        #Music page (3)
        self.empty_space_left_new = customtkinter.CTkLabel(master=self.tab("Music"), text="", fg_color="transparent")
        self.empty_space_left_new.pack(padx=10, pady=10, expand=True, side=customtkinter.LEFT)
        self.audPlayerFrame = customtkinter.CTkFrame(master=self.tab("Music"), width=480, corner_radius=15)
        self.audPlayer = customtkinter.CTkTextbox(master=self.audPlayerFrame, width=460, corner_radius=15)
        self.audPlayer.pack(padx=10, pady=10, expand=True, fill="both")
        self.music_slider = customtkinter.CTkSlider(master=self.audPlayerFrame, width=460)
        self.music_slider.pack(padx=0, pady=10)
        self.controls = customtkinter.CTkFrame(master=self.audPlayerFrame, width=460, fg_color="transparent")
        self.es1 = customtkinter.CTkLabel(master=self.controls, text="", fg_color="transparent")
        self.es1.pack(expand=True, fill="both", side=customtkinter.LEFT)
        self.previous_button = customtkinter.CTkButton(master=self.controls, width=70, text="≪", font=("Calibri", 20))
        self.previous_button.pack(padx=5, pady=0, side=customtkinter.LEFT)
        self.play_button = customtkinter.CTkButton(master=self.controls, width=70, text="Play ▶", font=("Calibri", 15))
        self.play_button.pack(padx=5, pady=0, side=customtkinter.LEFT)
        self.next_button = customtkinter.CTkButton(master=self.controls, width=70, text="≫", font=("Calibri", 20))
        self.next_button.pack(padx=5, pady=0, side=customtkinter.LEFT)
        self.es2 = customtkinter.CTkLabel(master=self.controls, text="", fg_color="transparent")
        self.es2.pack(expand=True, fill="both", side=customtkinter.LEFT)
        self.controls.pack(fill="both")
        self.stop_button = customtkinter.CTkButton(master=self.audPlayerFrame, width=70, text="Stop ☐", fg_color="red", font=("Calibri", 15))
        self.stop_button.pack(padx=10, pady=10)
        self.audPlayerFrame.pack(padx=0, pady=20, fill="both", side=customtkinter.LEFT)
        self.audio_list = customtkinter.CTkScrollableFrame(master=self.tab("Music"), width=340, corner_radius=15)
        lg.createAudioList()
        self.audio_list.pack(padx=20, pady=20, fill="both", side=customtkinter.LEFT)
        self.empty_space_right_new = customtkinter.CTkLabel(master=self.tab("Music"), text="", fg_color="transparent")
        self.empty_space_right_new.pack(padx=10, pady=10, expand=True, side=customtkinter.LEFT)
        
        
class App(customtkinter.CTk):
    def __init__(self, thread=None):
        super().__init__()
        self.thread = thread
        
    def change_theme(self):
        if self.switch.get() == "on":
            customtkinter.set_appearance_mode("dark")
        elif self.switch.get() == "off":
            customtkinter.set_appearance_mode("light")
            
    def setThread(self, new_thread):
        self.thread = new_thread
        
    def callWidgets(self):
        self.top_frame = customtkinter.CTkFrame(master=self, height=50, fg_color="transparent")
        self.top_frame.pack(padx=10, pady=10, fill="both")
        self.name = customtkinter.CTkLabel(master=self.top_frame, text="Loader+", fg_color="transparent", font=("Trebuchet MS", 21))
        self.name.pack(padx=10, pady=10, side=customtkinter.LEFT)
        self.empty_space = customtkinter.CTkLabel(master=self.top_frame, text="", fg_color="transparent")
        self.empty_space.pack(padx=10, pady=10, expand=True, side=customtkinter.LEFT)
        self.theme = customtkinter.CTkLabel(master=self.top_frame, text="Dark Theme", fg_color="transparent", font=("Trebuchet MS", 17))
        self.theme.pack(padx=10, pady=10, side=customtkinter.LEFT)
        self.switch_var = customtkinter.StringVar(value="on")
        self.switch = customtkinter.CTkSwitch(master=self.top_frame, text="", width=35, command=self.change_theme, variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.pack(padx=10, pady=10, side=customtkinter.LEFT)
        self.tab_view = MyTabView(master=self, app=self, thread=self.thread)
        self.tab_view.pack(padx=10, pady=10, fill="both", expand=True)