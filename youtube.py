import customtkinter
import tkinter               
from pytubefix import YouTube
import os

def mp4download():
    try:
        ytUrl = link.get() #inserted URL
        ytObject = YouTube(ytUrl) 

        videoStream = ytObject.streams.filter(resolution='1440p', progressive=False).first()
        if not videoStream:
            videoStream = ytObject.streams.filter(progressive=False).order_by('resolution').desc().first()
        audioStream = ytObject.streams.filter(only_audio=True).first()
        #check if both streams are available
        if videoStream and audioStream:
            video_file_path = videoStream.download()
            audio_file_path = audioStream.download(mp3=True)

            #combine audio and video using ffmpeg
            combined_file_path = os.path.join(f'{ytObject.title}.mp4')
            os.system(f'ffmpeg -i "{video_file_path}" -i "{audio_file_path}" -c:v copy -c:a aac "{combined_file_path}"')
            #clears the audio and video files that was used to merge
            os.remove(video_file_path)
            os.remove(audio_file_path)
            link.delete(0, customtkinter.END) #delete the link after downloading
        else:
            debugLabel.configure(text="Audio and Video file not supporting")
    except Exception as e:
        debugLabel.configure(text=f"Something went wrong: {e}")

def mp3download(): #download youtube videos in mp3 file type
    try:
        ytUrl=link.get() #inserted url 
        ytObject=YouTube(ytUrl)
        audio=ytObject.streams.get_audio_only()
        audio.download(mp3=True)
        link.delete(0, customtkinter.END)
    except:
        debugLabel.configure(text="something went wrong")

def DownloadMenu(): #main menu
    try:
        dt=datatype.get() #takes the datatype from the segment button and routes to the function
        #menu
        if dt=="MP4":
            mp4download()
        elif dt=="MP3":
            mp3download()
        else:
            debugLabel.configure(text="select a datatype")
    except:
        debugLabel.configure(text="something went wrong")

#main settings => UI configuration
app=customtkinter.CTk()
app.geometry("720x720")
app.resizable(False,False)
app.title("Youtube Vid Downloader")
app.iconbitmap('/home/xenon/youtube/icon.ico')
customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("dark")

#UI => user interface setup
title=customtkinter.CTkLabel(app,text="Paste the URL here")
title.pack(padx=10,pady=10)

#input => input the link over here
linkVariable=tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=480, height=30, textvariable=linkVariable)
link.pack(padx=10,pady=10)

#datatype => [MP3/MP4]
lsd=["MP3","MP4"]
datatype=customtkinter.CTkSegmentedButton(app,values=lsd)
datatype.pack()

#button => Download Button
download=customtkinter.CTkButton(app, text="Download",command=DownloadMenu,fg_color="red",hover="blue")
download.pack(padx=10,pady=10)

#debug label => shows error
debugLabel=customtkinter.CTkLabel(app,text="")
debugLabel.pack(padx=10)

#progress bar => 0 to 100
progressBar=customtkinter.CTkLabel(app,text="0")
progressBar.pack(padx=10)

#loop => open the window
app.mainloop()
