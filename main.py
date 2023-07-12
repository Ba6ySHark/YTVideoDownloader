import customtkinter
import os
from ui import MyTabView, App
from downloaderThread import DThread

def leave(app):
    app.quit()
    app.destroy()
    os._exit(True)

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    
    app = App()
    app.geometry("1280x720")
    app.title("Loader+")
    app.minsize(1280, 720)
        
    app.protocol("WM_DELETE_WINDOW", lambda app=app: leave(app))
    
    thread = DThread()
    thread.daemon = True
    thread.start()
    
    #ui.setThread(thread)
    app.setThread(thread)
    app.callWidgets()
    app.mainloop()