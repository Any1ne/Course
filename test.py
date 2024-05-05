import cv2
from PIL import Image
import customtkinter as ctk
import os
import subprocess

class Test(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TEST")
        self.geometry("1000x1000")
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_rowconfigure(0, weight=1)

        self.video_frame = Video_frame(self)
        self.video_frame.configure(fg_color = "orange")
        self.video_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw", rowspan=4) 

        self.config_frame = Config_frame(self)
        self.config_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="ne")

        self.animation_frame = Animation_frame(self)
        self.animation_frame.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="e")

        self.text_frame = Text_frame(self)
        self.text_frame.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="se")

        self.video_file = []

class Video_frame(ctk.CTkFrame):
    def __init__(self, master=None, width=100, height=100, **kwargs):
        super().__init__(master, **kwargs)
        self.video_file = []
        self.index = 0
        self.isplaying = False

        self.video_panel = ctk.CTkLabel(self, width=width, height=height)
        self.grid_rowconfigure(0, weight=1)
        self.video_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nswe", columnspan=2)

        self.button_text = "Play"
        self.button = ctk.CTkButton(self, text=self.button_text, command=self.play_pause)
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky="e")

        self.button_step = ctk.CTkButton(self, text="Step forward", command=self.step)
        self.button_step.grid(row=1, column=2, padx=20, pady=20, sticky="w")

    def step(self):
        self.cap = cv2.VideoCapture(self.video_file[self.index])
        self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))

        #print(self.video_file[self.index], self.index)
        self.update()

        if self.index < len(self.video_file)-1:
            self.index += 1
        else:
            print("END")

    def update(self):
        if self.isplaying:
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
        if self.isplaying:
            self.button_text = "Play"
        else:
            self.button_text = "Pause"
        self.button.configure(text=self.button_text)
        self.isplaying = not self.isplaying

class Config_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self, text="Function", command=self.open_toplevel, variable=switch_var, onvalue="on", offvalue="off")
        self.switch.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")

        optionmenu_var = ctk.StringVar(value="option 2")
        self.optionmenu = ctk.CTkOptionMenu(self,values=["option 1", "option 2"], command=self.optionmenu_callback, variable=optionmenu_var)
        self.optionmenu.grid(row=1, column=0, padx=20, pady=20, sticky="nswe")

        self.toplevel_window= None

        self.Xi = ctk.CTkEntry(self, placeholder_text="X")
        self.Xi.grid(row=2, column=0, padx=20, pady=20, sticky="nswe")

        self.eps = ctk.CTkEntry(self, placeholder_text="eps")
        self.eps.grid(row=3, column=0, padx=20, pady=20, sticky="nswe")
        
        optionmenu_var = ctk.StringVar(value="option 2")
        self.methods = ctk.CTkOptionMenu(self,values=["option 1", "option 2"], command=self.optionmenu_callback, variable=optionmenu_var)
        self.methods.grid(row=4, column=0, padx=20, pady=20, sticky="nswe")

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = self.ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    class ToplevelWindow(ctk.CTkToplevel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.geometry("400x300")

            self.label = ctk.CTkLabel(self, text="ToplevelWindow")
            self.label.pack(padx=20, pady=20)

            self.entry = ctk.CTkEntry(self, placeholder_text="Entry")
            self.entry.grid(row=1, column=0, padx=20, pady=20, sticky="nswe")

            self.button= ctk.CTkButton(self, text="CTkButton")
            self.button.grid(row=1, column=1, padx=20, pady=20, sticky="nswe")
            self.entry.grid_remove()
            self.button.grid_remove()
        
    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    def switch_event(self):
        if self.switch.get() == "on":
            self.optionmenu.grid_remove()  # Hide optionmenu
            self.entry.grid(row=1, column=0, padx=20, pady=20, sticky="nswe")  # Show entries
            self.button.grid(row=1, column=1, padx=20, pady=20, sticky="nswe")
        else:
            self.entry.grid_remove()  # Hide optionmenu
            self.button.grid_remove()
            self.optionmenu.grid(row=1, column=0, padx=20, pady=20, sticky="nswe")  # Show entries



class Animation_frame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.button_anim = ctk.CTkButton(self, text="Animate", command=self.animate)
        self.button_anim.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    def animate(self):
        command = ["manim", "-ql", "example.py", "PointMovingOnShapes"]
        process = subprocess.Popen(command)
        process.wait()

        self.master.video_frame.video_file = get_video_files()
        self.master.video_frame.index = 0
        self.master.video_frame.cap = cv2.VideoCapture(self.master.video_frame.video_file[self.master.video_frame.index])
        self.master.video_frame.delay = int(1000 / self.master.video_frame.cap.get(cv2.CAP_PROP_FPS))
        self.master.video_frame.state = True

class Text_frame(ctk.CTkFrame):
     def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

def get_video_files():
    project_dir = os.path.dirname(os.path.abspath(__file__))  # Get project directory
    file_path = os.path.join(project_dir, 'media/videos/example/480p15/partial_movie_files/PointMovingOnShapes/partial_movie_file_list.txt')

    with open(file_path, 'r') as f:
        video_file_list = [line.strip()[11:-1] for line in f if line.startswith('file \'file:')]
        
    return video_file_list

def main():
    test = Test()
    test.mainloop()

if __name__ == "__main__":
    main()
