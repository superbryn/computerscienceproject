import customtkinter
from pytubefix import YouTube
import tkinter
from moviepy import VideoFileClip,AudioFileClip
import os

class YoutubeVideoDownloader:
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
            videoStream = self.youtubeObject.streams.filter(resolution="1080p", progressive=False).first()
            if not videoStream:
                videoStream = self.youtubeObject.streams.filter(progressive=True).order_by('resolution').desc().first()
            audioStream = self.youtubeObject.streams.filter(only_audio=True).first()
            if videoStream and audioStream:
                video_path = videoStream.download()
                audio_path = audioStream.download(mp3=True)

                video = VideoFileClip(video_path)
                audio = AudioFileClip(audio_path)

                video_clip = video.set_audio(audio)
                combined_path = os.path.join(f"{self.youtubeObject.title}.mp4")
                video_clip.write_videofile(combined_path, codec='libx264',audio_encode='aac')

                os.remove(audio_path)
                os.remove(video_path)
                return f"{self.youtubeObject.title} was successfull downloaded as mp4"
            else:
                raise Exception("Something went wrong")
        except Exception as e:
            return f"Error while downloading as MP4: {e}"
    def mp3download(self):
        try:
            self.catchLink()
            audio = self.youtubeObject.streams.get_audio_only()
            audio.download(mp3=True)
            return f"{self.youtubeObject.title} has completed downloading"
        except Exception as e:
            return f"Error while The video as MP3: {e}"
        
class SpeedYUI:
    def __init__(self,app):
        self.app = app
        self.app.geometry("720x720")
        self.app.resizable(False,False)
        self.app.title("Youtube Vid Downloader")
        customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("dark")

        self.downloader = None

        self.Widgets()
    
    def Widgets(self):
        self.title = customtkinter.CTkLabel(self.app, text="Paste the URL here")
        self.title.pack(padx=10, pady=10)

        # Input Entry for URL
        self.link_variable = tkinter.StringVar()
        self.link = customtkinter.CTkEntry(self.app, width=480, height=30, textvariable=self.link_variable)
        self.link.pack(padx=10, pady=10)

        # Segment Button (MP3/MP4)
        self.datatype = customtkinter.CTkSegmentedButton(self.app, values=["MP3", "MP4"])
        self.datatype.pack()

        # Download Button
        self.download_button = customtkinter.CTkButton(self.app, text="Download", command=self.download, fg_color="red", hover="blue")
        self.download_button.pack(padx=10, pady=10)

        # Debug Label
        self.debug_label = customtkinter.CTkLabel(self.app, text="")
        self.debug_label.pack(padx=10)

        # Progress Bar (Currently not functional)
        self.progress_bar = customtkinter.CTkLabel(self.app, text="0")

        self.progress_bar.pack(padx=10)

        def download(self):
            try:
                url = self.link.get()
                if not url:
                    self.debug_label.configure(text="Please enter a URL.")
                    return
                
                self.downloader = YoutubeVideoDownloader(url)

                datatype = self.datatype.get()
                if datatype == "MP4":
                    result = self.downloader.download_mp4()
                elif datatype == "MP3":
                    result = self.downloader.download_mp3()
                else:
                    self.debug_label.configure(text="Please select a valid format (MP3 or MP4).")
                    return

                self.debug_label.configure(text=result)
                self.link.delete(0, customtkinter.END)  # Clear the URL input field
            except Exception as e:
                self.debug_label.configure(text=f"Something went wrong: {e}")

if __name__ == "__main__":
    app = customtkinter.CTk()
    app_ui = SpeedYUI(app)
    app.mainloop()
