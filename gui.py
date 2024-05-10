import customtkinter as ctk
from sympy import *
import cv2
from PIL import Image
import json
import os
import subprocess
import threading
import time


class GINM(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GINM")
        self.geometry("1200x800")
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

        self.video_frame = Video_frame(self)
        self.video_frame.configure(fg_color = "orange")
        self.video_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nswe", columnspan=1, rowspan=4) 

        self.config_frame = Config_frame(self)
        self.config_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nswe", columnspan=2)

        self.animation_frame = Animation_frame(self)
        self.animation_frame.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="nswe", columnspan=2)

        self.info_frame = Info_frame(self)
        self.info_frame.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="nswe", columnspan=2)

class Video_frame(ctk.CTkFrame):
    def __init__(self, master=None, width=100, height=100, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.video_file_list = []
        self.isplaying = False

        self.video_panel = ctk.CTkLabel(self, width=width, height=height)
        self.grid_rowconfigure(0, weight=1)
        self.video_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nswe", columnspan=2)

        func_var = ctk.StringVar(value="Play mode")
        self.playmode_o = ctk.CTkOptionMenu(self, values=["Steps", "Full"], command=self.play_mode, variable=func_var)
        self.playmode_o.grid(row=1, column=3, padx=20, pady=20, sticky="nswe")

        self.button_text = "Play"
        self.play_pause_b = ctk.CTkButton(self, text=self.button_text, command=self.play_pause)
        self.play_pause_b.grid(row=1, column=1, padx=20, pady=20, sticky="s")

        self.step_for_b = ctk.CTkButton(self, text="Step forward", command=self.step_for)
        self.step_for_b.grid(row=1, column=2, padx=20, pady=20, sticky="se")

        self.step_back_b = ctk.CTkButton(self, text="Step backward", command=self.step_back)
        self.step_back_b.grid(row=1, column=0, padx=20, pady=20, sticky="sw")

        # self.update_video_list()

    def play_mode(self):
        pass

    def step_for(self):
        if len(self.video_file_list) != 0:
            self.cap = cv2.VideoCapture(self.video_file_list[self.index])
            self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))

            self.update()

            if self.index < len(self.video_file_list)-1:
                self.index += 1
            else:
                self.master.info_frame.insert("END")
        else:
            self.master.info_frame.insert("video_file_list empty")

    def play_pause(self):
        if self.isplaying:
            self.button_text = "Play"
        else:
            self.button_text = "Pause"
            if len(self.video_file_list) != 0:
                self.update()
            else:
                self.master.info_frame.insert("video_file_list empty")
        

        self.play_pause_b.configure(text=self.button_text)
        self.isplaying = not self.isplaying

    def step_back(self):
        if len(self.video_file_list) != 0:
            if self.index > 0:
                self.index -= 1
            else:
                self.master.info_frame.insert("Start")

            self.cap = cv2.VideoCapture(self.video_file_list[self.index])
            self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))
            self.update()
        else:
            self.master.info_frame.insert("video_file_list empty")
        
        self.isplaying = False  

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

    def load_video_list(self):
        self.video_file_list = get_video_files()
        self.index = 0
        # insert(self.video_file_list)
        # insert(self.index)
        self.cap = cv2.VideoCapture(self.video_file_list[self.index])
        self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS)) 

    def update_video_list(self):
        if len(self.video_file_list) == 0:
            self.load_video_list()
        else:
            #self.master.info_frame.insert(f"updating{}")
            self.video_file_list = get_video_files()
            for video_file in self.video_file_list:
                if not video_file in self.video_file_list: ### adding vided on the list !!!!
                    self.video_file_list.append(video_file)

class Config_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.func_mode = "Function Build-in"
        switch_var = ctk.StringVar(value="build-in")
        self.func_s = ctk.CTkSwitch(self, text = self.func_mode, command=self.custom_build_in, variable=switch_var, onvalue="custom", offvalue="build-in")
        self.func_s.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")

        func_var = ctk.StringVar(value="x**2+2*x+1")
        self.func_o = ctk.CTkOptionMenu(self, values=["x**2+2*x+1", "x**4+3*x-4"], command=self.optionmenu_callback, variable=func_var)
        self.func_o.grid(row=1, column=0, padx=20, pady=20, sticky="nswe")

        self.func_e = ctk.CTkEntry(self, placeholder_text="Function", state="disabled")
        self.func_e.grid(row=1, column=1,  padx=20, pady=20, sticky="nswe")

        self.xi_e = ctk.CTkEntry(self, placeholder_text="X")
        self.xi_e.grid(row=2, column=0, padx=20, pady=20, sticky="nswe")
        self.xi_e.insert(0, "1")

        self.resta_e = ctk.CTkEntry(self, placeholder_text="a")
        self.resta_e.grid(row=3, column=0, padx=20, pady=20, sticky="nswe")
        self.resta_e.insert(0, "-1")

        self.restb_e = ctk.CTkEntry(self, placeholder_text="b")
        self.restb_e.grid(row=3, column=1, padx=20, pady=20, sticky="nswe")
        self.restb_e.insert(0, "1")

        self.eps_e = ctk.CTkEntry(self, placeholder_text="eps")
        self.eps_e.grid(row=4, column=0, padx=20, pady=20, sticky="nswe")
        self.eps_e.insert(0, "0.01")

    def custom_build_in(self):
        if self.func_s.get() == "build-in":
            self.func_s.configure(text = "Function Build-in")
            self.func_o.configure(state="normal")
            self.func_e.configure(state="disabled")
        else:
            self.func_s.configure(text = "Function Custom")
            self.func_e.configure(state="normal")
            self.func_o.configure(state="disabled")

    def optionmenu_callback(self, choice):
        self.master.info_frame.insert("optionmenu dropdown clicked: "+str(choice))
        
class Animation_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        methods_var = ctk.StringVar(value="Newtons")
        self.methods_o = ctk.CTkOptionMenu(self,values=["Newtons"], variable= methods_var)
        self.methods_o.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")

        self.iter_e = ctk.CTkEntry(self, placeholder_text="Number of Iterations")
        self.iter_e.grid(row=0, column=1, padx=20, pady=20, sticky="nswe")
        self.iter_e.insert(0, "10")
        self.isvalid = True


        self.anim_text = "Animate"
        self.anim_b = ctk.CTkButton(self, text=self.anim_text , command=self.animate)
        self.anim_b.grid(row=1, column=0, padx=20, pady=20, sticky="we")

        self.valid_b = ctk.CTkButton(self, text="Validate", command=self.update_config)
        self.valid_b.grid(row=1, column=1, padx=20, pady=20, sticky="we")
        self.valid_info = "Need to validate configurations"

        self.isvalid = False
        self.ischanged = False
        self.isanimated = False

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
        "Quality": "l",
        "Iteration": 0,
        "Number of Iteration": 20,
        "Stop_Criteria": False
        }
    
        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=4)

    def animate(self):
        if not self.isanimated:
            self.isanimated = True
            self.anim_text  = "Stop Animate"

            with open('config.json') as f:
                config = json.load(f)
            method = config['Method']

            if self.isvalid and self.ischanged:
                command_gap = ["python", "gap.py"]
                self.gap_process = subprocess.Popen(command_gap)

                self.monitor_thread = threading.Thread(target=fmt_run, args=(self.master,))
                self.monitor_thread.start()   
            elif self.isvalid and os.path.exists('PMFL_'+method+'.txt'):
                self.master.video_frame.load_video_list()
            else:
                self.master.info_frame.insert(self.valid_info)
        else:
            self.isanimated = False
            self.anim_text  = "Animate"

            self.gap_process.terminate()

            #kill process
            pass

    def update_config(self):
        self.validate()
        self.check_config_change()

        if self.isvalid and not self.ischanged:
            with open('config.json') as f:
                config = json.load(f)

            if self.master.config_frame.func_s.get() == "build-in":
                config['f(x)'] = self.master.config_frame.func_o.get()
            else:
                config['f(x)'] = self.master.config_frame.func_e.get() 
            config['xi'] = float(self.master.config_frame.xi_e.get())
            config['Eps'] = float(self.master.config_frame.eps_e.get())
            config['Rest'] = [float(self.master.config_frame.resta_e.get()), float(self.master.config_frame.restb_e.get())]
            config['Method'] = self.methods_o.get()
            config['Number of Iteration'] = int(self.iter_e.get())

            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
        else:
            self.master.info_frame.insert(self.valid_info)

    def validate(self):
        try:
            sympify(self.master.config_frame.func_o.get())
        except (TypeError, ValueError):
            self.valid_info = f"Invalid function format in f(x): {self.master.config_frame.func_o.get()}"
            self.isvalid = False
            return

        # Перевірка xi
        try:
            xi = float(self.master.config_frame.xi_e.get())
        except ValueError:
            self.valid_info = f"Invalid xi value: {self.master.config_frame.xi_e.get()}. Must be a float or integer."
            self.isvalid = False
            return

        # Перевірка Eps
        try:
            eps = float(self.master.config_frame.eps_e.get())
        except ValueError:
            self.valid_info = f"Invalid Eps value: {self.master.config_frame.eps_e.get()}. Must be a float."
            self.isvalid = False
            return

        # Перевірка Rest
        try:
            rest_a = float(self.master.config_frame.resta_e.get())
        except ValueError:
            self.valid_info = f"Invalid a value: {self.master.config_frame.resta_e.get()}. Must be a float or integer."
            self.isvalid = False
            return
        try:
            rest_b = float(self.master.config_frame.restb_e.get())
        except ValueError:
            self.valid_info = f"Invalid b value: {self.master.config_frame.restb_e.get()}. Must be a float or integer."
            self.isvalid = False
            return
        
        if rest_a >=rest_b:
            self.valid_info = f"Invalid Rest format: [{rest_a}, {rest_b}]. b must be larger than a."
            self.isvalid = False
            return

        # Перевірка Number of Iteration
        try:
            number_of_iterations = int(self.iter_e.get())
        except ValueError:
            self.valid_info = f"Invalid Number of Iteration value: {self.master.config_frame.iter_e.get()}. Must be an integer."
            self.isvalid = False
            return

       ### check all data configuration
       ### check if somethings changed
        self.valid_info = "Configuration is valid"
        self.isvalid = True
        return 
    
    def check_config_change(self):
        with open('config.json') as f:
            config = json.load(f)

        if float(self.master.config_frame.resta_e.get()) != config['Rest'][0] or float(self.master.config_frame.restb_e.get()) != config['Rest'][1]:
            self.ischanged = True
        elif float(self.master.config_frame.xi_e.get()) != config['xi']:
            self.ischanged = True
        elif float(self.master.config_frame.eps_e.get()) != config['Eps']:
            self.ischanged = True
        elif self.master.config_frames.func_s.get() == "build-in":
            if self.master.config_frame.func_o.get() != config['f(x)']:
                self.ischanged = True
            elif self.master.config_frame.func_e.get() != config['f(x)']:
                self.ischanged = True
    
class Info_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        launch_text = "Made by Arthur Dombrovskij\n"
        self.textbox = ctk.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox.insert("0.0", launch_text)
        self.textbox.configure(state="disabled")

        self.textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nswe", columnspan=2)\
    
        self.instruction_b = ctk.CTkButton(self, text="Instruction", command=self.instruction)
        self.instruction_b.grid(row=1, column=0, padx=20, pady=20, sticky="we")

        #self.insert("Hi world!")

    def instruction(self):
        with open('Instruction_Functions.txt', 'r') as inst:
            instruction = [line.strip() for line in inst]
        
        self.delete()
        for line in instruction:
            self.insert(line)

    def print(self, text):
        self.delete()
        self.textbox.configure(state="normal")
        self.textbox.insert('end', str(text)+'\n')
        self.textbox.configure(state="disabled")

    def delete(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", 'end')
        self.textbox.configure(state="disabled")

    def insert(self, text):
        self.textbox.configure(state="normal")
        self.textbox.insert('end', str(text)+'\n')
        self.textbox.configure(state="disabled")

def get_video_files():
    with open('config.json') as f:
            config = json.load(f)
    method = config['Method']
    
    with open('PMFL_'+method+'.txt', 'r') as f:
        video_file_list = [line.strip() for line in f]
    return video_file_list

def fmt_run(master):
    time.sleep(1)
    with open('config.json') as f:
            config = json.load(f)
    method = config['Method']
    
    stopCriteria = False
    while not stopCriteria :
        master.info_frame.insert("Magnificent")
        with open('PMFL_'+method+'.txt', 'r') as f:
            file_lines = f.readlines()
        file_lines_stripped = [line.strip() for line in file_lines]

        print(file_lines_stripped)
        print(master.video_frame.video_file_list)
        if len(file_lines_stripped) > len(master.video_frame.video_file_list):                                      ### Checking ???
            master.info_frame.insert("Updating!!!")
            master.video_frame.update_video_list()
            master.info_frame.insert(len(master.video_frame.video_file_list))
        
        master.info_frame.insert(str(len(file_lines_stripped))+" "+str(len(master.video_frame.video_file_list)) )

        with open('config.json') as f:
            config = json.load(f)

        stopCriteria = config["Stop_Criteria"] or (config["Iteration"]>=config["Number of Iteration"])
        time.sleep(2)

    master.info_frame.insert("Finished!!!")
    master.animation_frame.isanimated = False

