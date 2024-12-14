import customtkinter 
from pytubefix import YouTube
from PIL import Image
from moviepy.editor import VideoFileClip,AudioFileClip
import os
import csv

class YoutubeVideoDownloader: # The Downloader
    def __init__(self, url):
        self.ytUrl = url
        self.youtubeObject = None
    def catchLink(self):
        try:
            self.youtubeObject = YouTube(self.ytUrl)
        except Exception as e:
            raise Exception(f"Found An error : {e}")
        
    def mp4downloader(self):
        try:
            self.catchLink()
            with open("logs.csv","a") as f:
                csv.writer(f,delimiter=",").writerow(["mp4",self.youtubeObject.title,self.ytUrl])
            videoStream = self.youtubeObject.streams.filter(resolution="1440p", progressive=False).first()
            if not videoStream:
                videoStream = self.youtubeObject.streams.filter(progressive=True).order_by('resolution').desc().first()
            audioStream = self.youtubeObject.streams.filter(only_audio=True).first()
            if videoStream and audioStream:
                video_path = videoStream.download()
                audio_path = audioStream.download(mp3=True)

                video = VideoFileClip(video_path)
                audio = AudioFileClip(audio_path)

                video_clip = video.set_audio(audio)
                combined_path = os.path.join(f"{self.youtubeObject.title}-SPEEDY.mp4")
                video_clip.write_videofile(combined_path)

                os.remove(audio_path)
                os.remove(video_path)
                return f"{self.youtubeObject.title} was successfull downloaded as mp4"
            else:
                raise Exception("Something went wrong")
        except Exception as e:
            return f"Error while downloading as MP4: {e}"
    def mp3downloader(self):
        try:
            self.catchLink()
            with open("logs.csv","a") as f:
                csv.writer(f,delimiter=",").writerow(["mp3",self.youtubeObject.title,self.ytUrl])
            audio = self.youtubeObject.streams.get_audio_only()
            audio.download(mp3=True)
            return f"{self.youtubeObject.title} has completed downloading"
        except Exception as e:
            return f"Error while The video as MP3: {e}"
        
class SpeedYUI: #UI
    def __init__(self,app):
        self.app = app
        self.app.geometry("750x500")
        self.app.resizable(False,False)
        self.app.title("SPEEDY CONVERTER")
        self.logoPath= os.path.abspath('SPEEDY/icon.ico')
        self.app.iconbitmap(self.logoPath)
        customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("dark")

        self.downloader = None

        self.Widgets()
    
    def Widgets(self):
        self.background_image_path = os.path.abspath("SPEEDY/new.png")
        print(self.background_image_path)
        if os.path.exists(self.background_image_path):
            self.myImage = customtkinter.CTkImage(dark_image=Image.open(self.background_image_path), size=(750, 500))
            self.imageLabel = customtkinter.CTkLabel(self.app, image=self.myImage, text="")
            self.imageLabel.place(relwidth=1, relheight=1)
        else:
            print("bg image not found")


        self.retro_font = ("Harlow Solid Italic", 48, "bold") #OCR A Extended
        self.title = customtkinter.CTkLabel(self.app,text=" =SPEEDY= ",font=self.retro_font,bg_color="#FDAF3E")
        self.title.pack(padx=0,pady=(170,0))

        self.link = customtkinter.CTkEntry(self.app,
                                           width=300, height=30, 
                                           placeholder_text="Paste The URL Here",
                                           bg_color="#FDAF3E",
                                           fg_color="white",
                                           border_color="white",
                                           text_color="black")
        self.link.pack(padx=0, pady=(10,10))

        self.datatype = customtkinter.CTkSegmentedButton(self.app, values=["MP3", "MP4"],
                                                        bg_color="#FDAF3E",
                                                        selected_color="red",
                                                        selected_hover_color="red",
                                                        unselected_color="#FDAF3E",
                                                        unselected_hover_color="#FDAF3E",
                                                        fg_color="#FDAF3E",
                                                        text_color="black"
                                                        )
        self.datatype.pack()

        self.download_button = customtkinter.CTkButton(self.app, text="Download",
                                                       command=self.download,
                                                       fg_color="red",
                                                       hover="blue",
                                                       bg_color="#FDAF3E")
        self.download_button.pack(padx=10, pady=10)

        self.debug_label = customtkinter.CTkLabel(self.app, text="",bg_color="#FDAF3E")
        self.debug_label.pack(padx=10)


    def download(self):
        try:
            url = self.link.get()
            if not url:
                self.debug_label.configure(text="Please enter a URL")
                return
            self.downloader = YoutubeVideoDownloader(url)

            datatype = self.datatype.get()
            if datatype == "MP4":
                result = self.downloader.mp4downloader()
            elif datatype == "MP3":
                result = self.downloader.mp3downloader()
            else:
                self.debug_label.configure(text="Please select a valid format (MP3 or MP4).")
                return

            self.debug_label.configure(text=result)
            self.link.delete(0, customtkinter.END)
        except Exception as e:
            self.debug_label.configure(text=f"Something went wrong: {e}")
            

if __name__ == "__main__":
    app = customtkinter.CTk()
    app_ui = SpeedYUI(app)
    app.mainloop()
