import customtkinter as ctk
import cv2
from PIL import Image
import json
import subprocess
import os
import threading
import time

class Test(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TEST")
        self.geometry("1200x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.video_frame = Video_frame(self)
        self.video_frame.configure(fg_color = "orange")
        self.video_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nswe", columnspan=1, rowspan=4) 

        self.config_frame = Config_frame(self)
        self.config_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nswe", columnspan=2)

        self.animation_frame = Animation_frame(self)
        self.animation_frame.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="nswe", columnspan=2)

        self.text_frame = Text_frame(self)
        self.text_frame.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="nswe", columnspan=2)

class Video_frame(ctk.CTkFrame):
    def __init__(self, master=None, width=100, height=100, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.video_file_list = []
        self.isplaying = False

        self.video_panel = ctk.CTkLabel(self, width=width, height=height)
        self.grid_rowconfigure(0, weight=1)
        self.video_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nswe", columnspan=2)

        self.button_text = "Play"
        self.play_pause_b = ctk.CTkButton(self, text=self.button_text, command=self.play_pause)
        self.play_pause_b.grid(row=1, column=1, padx=20, pady=20, sticky="s")

        self.step_for_b = ctk.CTkButton(self, text="Step forward", command=self.step_for)
        self.step_for_b.grid(row=1, column=2, padx=20, pady=20, sticky="se")

        self.step_back_b = ctk.CTkButton(self, text="Step backward", command=self.step_back)
        self.step_back_b.grid(row=1, column=0, padx=20, pady=20, sticky="sw")

        # self.update_video_list()

    def step_for(self):
        if len(self.video_file_list) != 0:
            self.cap = cv2.VideoCapture(self.video_file_list[self.index])
            self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))

            self.update()

            if self.index < len(self.video_file_list)-1:
                self.index += 1
            else:
                self.master.text_frame.print_text("END")
        else:
            self.master.text_frame.print_text("video_file_list empty")

    def play_pause(self):
        if self.isplaying:
            self.button_text = "Play"
        else:
            self.button_text = "Pause"
        self.play_pause_b.configure(text=self.button_text)
        self.isplaying = not self.isplaying

    def step_back(self):
        if len(self.video_file_list) != 0:
            if self.index > 0:
                self.index -= 1
            else:
                self.master.text_frame.print_text("Start")

            self.cap = cv2.VideoCapture(self.video_file_list[self.index])
            self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))
        else:
            self.master.text_frame.print_text("video_file_list empty")

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

    def update_video_list(self):
        if len(self.video_file_list) == 0:
            self.video_file_list = get_video_files()
            self.index = 0
            print(self.video_file_list)
            print(self.index)
            self.cap = cv2.VideoCapture(self.video_file_list[self.index])
            self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))  
        else:
            video_file_list = get_video_files()
            for video_file in video_file_list:
                if not video_file in self.video_file_list: ### adding vided on the list !!!!
                    self.video_file_list.append(video_file)

class Config_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        switch_var = ctk.StringVar(value="build-in")
        self.func_s = ctk.CTkSwitch(self, text="Function", command=self.custom_build_in, variable=switch_var, onvalue="custom", offvalue="build-in")
        self.func_s.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")

        func_var = ctk.StringVar(value="x**2+2*x+1")
        self.func_o = ctk.CTkOptionMenu(self,values=["x**2+2*x+1", "x**4+3*x-4"], command=self.optionmenu_callback, variable=func_var)
        self.func_o.grid(row=1, column=0, padx=20, pady=20, sticky="nswe")

        self.toplevel_window= None

        self.xi_e = ctk.CTkEntry(self, placeholder_text="X")
        self.xi_e.grid(row=2, column=0, padx=20, pady=20, sticky="nswe")

        self.resta_e = ctk.CTkEntry(self, placeholder_text="a")
        self.resta_e.grid(row=3, column=0, padx=20, pady=20, sticky="nswe")

        self.restb_e = ctk.CTkEntry(self, placeholder_text="b")
        self.restb_e.grid(row=3, column=1, padx=20, pady=20, sticky="nswe")

        self.eps_e = ctk.CTkEntry(self, placeholder_text="eps")
        self.eps_e.grid(row=4, column=0, padx=20, pady=20, sticky="nswe")

        methods_var = ctk.StringVar(value="Newton's")
        self.methods_o = ctk.CTkOptionMenu(self,values=["Newton's"], variable= methods_var )
        self.methods_o.grid(row=5, column=0, padx=20, pady=20, sticky="nswe")

        self.iter_e = ctk.CTkEntry(self, placeholder_text="Number of Iterations")
        self.iter_e.grid(row=6, column=0, padx=20, pady=20, sticky="nswe")
        self.isvalid = True

    def custom_build_in(self):
        if self.func_s.get() == "build-in":
            self.func_o.grid_remove()  # Hide TopWindow
            self.func_o.grid(row=1, column=0, padx=20, pady=20, sticky="nswe") #Hide optionmenu 
        else:
            self.func_o.grid_remove()  # Hide optionmenu

             # Show TopWindow

        # if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
        #     self.toplevel_window = self.ToplevelWindow(self)  # create window if its None or destroyed
        # else:
        #     self.toplevel_window.focus()  # if window exists focus it

    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
        
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
        
class Animation_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.button_anim = ctk.CTkButton(self, text="Animate", command=self.animate)
        self.button_anim.grid(row=0, column=0, padx=20, pady=20, sticky="we")

        self.button_valid = ctk.CTkButton(self, text="Validate", command=self.validate)
        self.button_valid.grid(row=0, column=1, padx=20, pady=20, sticky="we")

    default_config = {
    "f(x)": "x**3+2*x+1",
    "dx": "3*x**2+2",
    "d2x": "6*x",
    "tangent": "5*x-1",
    "xi": 1.0,
    "xi+1": 0.0,
    "f(xi)": 0.0,
    "f(xi+1)": 0.0,
    "Eps": 0.01,
    "Rest": [0, 0],
    "Method": "Newtons",
    "Quality": "h",
    "Iteration": 0,
    "Number of Iteration": 20,
    "Stop_Criteria": False,
}
    
    with open('config.json', 'w') as f:
        json.dump(default_config, f, indent=4)

    def animate(self):
        command_gap = ["python", "Generate_animations_process.py"]
        gap_process = subprocess.Popen(command_gap)

        monitor_thread = threading.Thread(target=fmt_run, args=(self.master,))
        monitor_thread.start()

    def validate(self):
        self.isvalid()

        if self.master.config_frame.isvalid:
            with open('config.json') as f:
                config = json.load(f)

            if self.master.config_frame.func_s.get() == "build-in":
                config['f(x)'] = self.master.config_frame.func_o.get()
            else:
                pass # 
            config['xi'] = float(self.master.config_frame.xi_e.get())
            config['Eps'] = float(self.master.config_frame.eps_e.get())
            config['Rest'] = [self.master.config_frame.resta_e.get(), self.master.config_frame.restb_e.get()]
            config['Number of Iteration'] = int(self.master.config_frame.iter_e.get())

            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
        else:
            self.master.text_frame.print_text("Config is not valid")

    def isvalid(self):
       ### check all data configueation
       pass 
            
class Text_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.textbox = ctk.CTkTextbox(master=self, width=400, corner_radius=0, state = "disabled")
        self.textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nswe", columnspan=2)

        #self.print_text("Hi world!")

    def print_text(self, text):
        self.textbox.configure(state="normal")
        self.textbox.insert("0.0", str(text)+'\n')
        self.textbox.configure(state="disabled")

def get_video_files():
    with open("PMFL.txt", 'r') as f:
        video_file_list = [line.strip() for line in f]
    return video_file_list

def fmt_run(master):
    with open('PMFL.txt', 'w') as f:
        f.write('')
    last_mtime = os.path.getmtime('PMFL.txt')

    stopCriteria = False
    while not stopCriteria :
        current_modified = os.path.getmtime('PMFL.txt')
        
        if current_modified != last_mtime:                                        ### Checking ???
            master.text_frame.print_text("Updating!!!")
            master.video_frame.update_video_list()
            master.text_frame.print_text(len(master.video_frame.video_file_list))
        
        with open('config.json') as f:
            config = json.load(f)

        stopCriteria = config["Stop_Criteria"] or (config["Iteration"]>=config["Number of Iteration"])
        time.sleep(1)

    master.text_frame.print_text("Finished!!!")

def main():
    test = Test()
    test.mainloop()

if __name__ == "__main__":
    main()
