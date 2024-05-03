import cv2
from PIL import Image
import customtkinter as ctk
import os

class VideoPlayer:
    def __init__(self, video_file, master=None, width=100, height=100):
        self.video_file = video_file
        self.index = 0

        self.cap = cv2.VideoCapture(self.video_file[self.index])
        self.master = master
        self.video_panel = ctk.CTkLabel(master, width=width, height=height)
        self.video_panel.grid(row=0, column=1, padx=20, pady=20, sticky="w", columnspan=2)
        self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))
        self.state = True

        # Create the button within the class initialization
        self.button_text = "play"
        self.button = ctk.CTkButton(master, text=self.button_text, command=self.play_pause)
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky="e")

        self.button_step = ctk.CTkButton(master, text="step", command=self.step)
        self.button_step.grid(row=1, column=2, padx=20, pady=20, sticky="w")
        
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_rowconfigure((0, 3), weight=1)

    def step(self):
        self.cap = cv2.VideoCapture(self.video_file[self.index])
        self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))

        print(self.video_file[self.index], self.index)
        self.update()

        if self.index < len(self.video_file)-1:
            self.index += 1
        else:
            print("END")

    def update(self):
        if self.state:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert frame to PIL Image
                pil_image = Image.fromarray(frame)

                # Create CTkImage from PIL Image
                ctk_image = ctk.CTkImage(pil_image, size=pil_image.size)

                # Set CTkImage to video panel
                self.video_panel.configure(image=ctk_image)
                self.master.after(self.delay, self.update)
            else:
                self.cap.release()
        else:
            self.master.after(self.delay, self.update)

    def play_pause(self):
        if self.state:
            self.button_text = "play"
        else:
            self.button_text = "pause"
        self.button.configure(text=self.button_text)
        self.state = not self.state

    def is_playing(self):
        return self.button_text == "pause"

    def update_button_text(self):
        self.button_text = "play" if self.is_playing() else "pause"
        # Update the button text in the main window (assuming it's accessible)
        ctk.button.configure(text=self.button_text)

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))  # Get project directory
    file_path = os.path.join(project_dir, 'media/videos/example/480p15/partial_movie_files/PointMovingOnShapes/partial_movie_file_list.txt')

    with open(file_path, 'r') as f:
        video_file_list = [line.strip()[11:-1] for line in f if line.startswith('file \'file:')]

    # Create the main window
    window = ctk.CTk()
    window.geometry('800x800')

    # Create the video player
    video = VideoPlayer(video_file_list, master=window, width=500, height=500)

    # Start the mainloop
    window.mainloop()

if __name__ == "__main__":
    main()
