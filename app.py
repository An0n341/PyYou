import threading
from pytube import YouTube, Playlist, exceptions
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

class App(tk.Tk):
    """
    PyYou is a minimal desktop application to download any YouTube video/playlist.
    With the ability to select how to download the video (video or audio)
    """

    def __init__(self):
        super().__init__()

        self.title("PyYou - Download Video YouTube")
        self.geometry("400x500")
        self.resizable(False, False)
        self.iconbitmap("assets/favicon.ico")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=50)

        self.directory = ""

        # call functions
        self.draw_app()

    def draw_app(self):
        """
        this function is used for create all design of this simple application. Header, entry, Radiobutton,
        Button and anothers functionality.
        """
        # draw header
        self.header = tk.Frame(self, bg="#E58181")
        self.title = tk.Label(self.header, text="YouTube Download Video", anchor="center", font=("Ubuntu 18 bold"), bg="#E58181", fg="white")
        self.title.pack(pady=10)
        self.header.grid(row=0, sticky="news")

        # content app
        self.content_app = tk.Frame(self)
        self.content_app.configure(background="white")

        # video link input
        self.video_url = tk.Entry(self.content_app, width=33, bg="#E3E3E3", borderwidth=0, font=("Ubuntu 14"))
        self.video_url.focus()
        self.video_url.insert(0, "Video URL".strip())
        self.video_url.pack(pady=10)

        # filename override input
        self.filename = tk.Entry(self.content_app, width=33, bg="#E3E3E3", borderwidth=0, font=("Ubuntu 14"))
        self.filename.insert(0, "Filename Override".strip())
        self.filename.pack(pady=10)

        # choose options
        self.container_choices = tk.Frame(self.content_app, bg="white")
        self.radio_value = tk.IntVar()

        # options
        self.r1 = tk.Radiobutton(self.container_choices, text="Video", bg="white", variable=self.radio_value, font=("12"), value=1).pack(side=tk.LEFT)
        self.r2 = tk.Radiobutton(self.container_choices, text="Audio", bg="white", variable=self.radio_value, font=("12"), value=2).pack(side=tk.LEFT, padx=20)
        self.r3 = tk.Radiobutton(self.container_choices, text="Playlist", bg="white", variable=self.radio_value, font=("12"), value=3).pack(side=tk.LEFT)
        self.container_choices.pack(pady=10)

        # buttons app
        self.download = tk.Button(self.content_app, text="Download", bg="#E58181", fg="white", borderwidth=0, width=28, height=1, font=("Ubuntu 16"), command=lambda: threading.Thread(target=self.download).start()).pack(pady=20, side=tk.BOTTOM)
        self.path = tk.Button(self.content_app, text="Select file Path", bg="#7FC887", fg="white", borderwidth=0, width=28, height=1, font=("Ubuntu 16"), command=self.select_directory).pack(side=tk.BOTTOM)

        self.content_app.grid(row=1, sticky="news")

    def select_directory(self):
        self.directory = filedialog.askdirectory(title="Select Folder Downlaod")
        print(self.directory)
        return self.directory

    def download(self):
        """
        all logic for download any video from youtube. The logic for change name, select format
        and directory of downloading all files
        """
        link = self.video_url.get()
        radio_val = self.radio_value.get()

        if link != "Video URL": # link not empty
            if self.directory: # user has select a directory
                if radio_val == 1: # video
                    try:
                        yt = YouTube(link)
                    except exceptions.RegexMatchError: # video not found
                        messagebox.showerror(title="Problem with Link", message="Please enter a valid link!")
                    else:
                        stream = yt.streams.filter(only_video=True)
                        name = "{}.mp4".format(self.filename.get())

                        if name != "Filename Override.mp4":
                            stream.first().download(output_path=self.directory, filename=name) # custom name from user

                        else:
                            stream.first().download(output_path=self.directory, filename=f"{yt.title}.mp4") # default name

                elif radio_val == 2: # audio
                    try:
                        yt = YouTube(link)
                    except exceptions.RegexMatchError as err: # video not found
                        messagebox.showerror(title="Problem with Link", message="Please enter a valid link!")
                        print(f"{err}")
                    except exceptions.VideoUnavailable:
                        messagebox.showerror(title="Problem with Video", message="Base video unavailable error!")
                    else:
                        stream = yt.streams.filter(only_audio=True)
                        name = "{}.mp3".format(self.filename.get())

                        if name != "Filename Override.mp3":
                            stream.first().download(output_path=self.directory, filename=name)
                        else:
                            stream.first().download(output_path=self.directory, filename=f"{yt.title}.mp3")

                elif radio_val == 3: # playlist
                    p = Playlist(link)
                    playlist_question = messagebox.askquestion(title="Question", message="You want download all file with video extension?")

                    for url in p.video_urls:
                        try:
                            yt = YouTube(url)

                        except exceptions.RegexMatchError: # video not found
                            messagebox.showerror(title="Problem with Link", message="Please enter a valid link!")
                            print(f"{err}")

                        except exceptions.VideoUnavailable:
                            messagebox.showerror(title="Problem with Video", message="Base video unavailable error!")
                        else:
                            if playlist_question == "yes":
                                stream = yt.streams.filter(only_video=True)
                                stream.first().download(output_path=self.directory)

                            elif playlist_question == "no":
                                stream = yt.streams.filter(only_audio=True)
                                stream.first().download(output_path=self.directory, filename=f"{yt.title}.mp3")

            else:
                messagebox.showerror(title="Select Path", message="You have to select a path where you can download the video!")
        else:
            messagebox.showerror(title="Problem with Link", message="Enter a youtube video/playlist link for continue!")

if __name__ == "__main__":
    app = App()
    app.mainloop()
