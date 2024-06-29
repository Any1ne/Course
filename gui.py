import customtkinter as ctk
from sympy import sympify, symbols
from math import *
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

import csv
import json

import os
import subprocess
import threading
import sys

import cProfile
import pstats

class VNM(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VNM")
        size = "1500x700"
        self.geometry(size)

        # self.minsize(width, height)
        # self.maxsize(width, height)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 2), weight=1)

        self.label_font = ("Helvetica", 14)

        self.video_frame = Video_frame(self, fg_color = "gray", width =500)
        self.video_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe", rowspan=3)

        self.animation_frame = Animation_frame(self, height= 200, width =200)
        self.animation_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nswe")

        self.config_frame = Config_frame(self, height = 200, width =200)
        self.config_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        self.info_frame = Info_frame(self, height = 200, width =200)
        self.info_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nswe")

class Video_frame(ctk.CTkFrame):
    def __init__(self, master=None, width=100, height=100, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.video_panel = ctk.CTkFrame(self)
        self.video_panel.grid(row=0, column=0, padx=(5,5), pady=(5,5), sticky="nswe")

        self.video_panel.grid_columnconfigure(0, weight=1)
        self.video_panel.grid_rowconfigure(1, weight=1)
        
        self.video_l = ctk.CTkLabel(self.video_panel, text="Video player", font = ("Helvetica", 20))
        self.video_l.grid(row=0, column=0, padx=10, pady=5, sticky="nswe")

        self.video = ctk.CTkLabel(self.video_panel, text = None, width=width, height=height)
        self.video.grid(row=1, column=0, padx=(10,10), pady=(10,10), sticky="nswe")

        self.load_logo()

        self.control_panel = ctk.CTkFrame(self.video_panel)
        self.control_panel.grid(row=2, column=0, padx=10, pady=10,
                                #  sticky="nswe"
                                 )

        self.control_panel.grid_columnconfigure(3, weight=1)
        self.control_panel.grid_rowconfigure(0, weight=1)

        func_var = ctk.StringVar(value="Play mode")
        self.playmode_o = ctk.CTkOptionMenu(self.control_panel, values=["Full", "Steps"], command=self.play_mode, variable=func_var, font = self.master.label_font)
        self.playmode_o.grid(row=1, column=3, padx=20, pady=20, 
                            #   sticky="nse"
                             )

        self.play_pause_b = ctk.CTkButton(self.control_panel, text="▶", command=self.play_pause, font = self.master.label_font)
        self.play_pause_b.grid(row=1, column=1, padx=20, pady=20,
                                #  sticky="nse"
                                )

        self.stepF_b = ctk.CTkButton(self.control_panel, text="⏭", command=self.stepF, state = 'disabled', font = self.master.label_font)
        self.stepF_b.grid(row=1, column=2, padx=20, pady=20,
                        #    sticky="nse"
                           )

        self.stepB_b = ctk.CTkButton(self.control_panel, text="⏮", command=self.stepB, state = 'disabled', font = self.master.label_font)
        self.stepB_b.grid(row=1, column=0, padx=20, pady=20, 
                        #    sticky="nsw"
                          )

        self.default()

    def load_logo(self):
        project_dir = os.path.dirname(os.path.abspath(__file__))

        path_logo = os.path.join(project_dir, "media", "images", "logo", "Logo_ManimCE_v0.18.1.png")

        if not os.path.exists(path_logo):
            logo = ["manim", "-v", "WARNING", "logo.py", "Logo", "-ql"]
            process_logo = subprocess.Popen(logo)
            process_logo.wait()

        self.logo = Image.open(path_logo) 
        self.image = ctk.CTkImage(dark_image=self.logo, size=self.logo.size)
        self.video.configure(image=self.image)

    def load_manual(self):
        project_dir = os.path.dirname(os.path.abspath(__file__))

        path_logo = os.path.join(project_dir, "media", "images", "manual", "Manual_ManimCE_v0.18.1.png")

        if not os.path.exists(path_logo):
            logo = ["manim", "-v", "WARNING", "manual.py", "Manual", "-ql"]
            process_logo = subprocess.Popen(logo)
            process_logo.wait()

        self.logo = Image.open(path_logo) 
        self.image = ctk.CTkImage(dark_image=self.logo, size=self.logo.size)
        self.video.configure(image=self.image)

    def play_mode(self):
        pass

    def stepF(self):
        self.stepF_b.configure(state = 'disabled')
        if len(self.video_file_list) != 0:
            if self.index < len(self.video_file_list)-1:
                self.index += 1
                self.stepB_b.configure(state = 'normal')
                if self.fullmode:
                    self.index += 1
                    self.preview()
                else:
                    self.isplaying = True
                    self.next()
            else:
                self.master.info_frame.insert("END")
                self.play_pause_b.configure(state = 'disabled')

            self.isplaying = False
            self.play_pause_b.configure(text = "▶")
        else:
            self.master.info_frame.insert("video_file_list empty")

        if self.index < len(self.video_file_list)-1:
            self.stepF_b.configure(state = 'normal')

    def play_pause(self):
        if self.isplaying:
            button_text = "▶"
        else:
            button_text = "⏸"
            if len(self.video_file_list) != 0 and self.index >= 0 and self.index < len(self.video_file_list) :
                self.cap = cv2.VideoCapture(self.video_file_list[self.index])
                self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))
                self.update()
            else:
                self.master.info_frame.insert("video_file_list empty")
        self.play_pause_b.configure(text=button_text)
        self.isplaying = not self.isplaying

    def stepB(self):
        self.stepB_b.configure(state = 'disabled')
        if len(self.video_file_list) != 0:
            if self.index > 0:
                self.index -= 1
                self.stepF_b.configure(state = 'normal')
                self.play_pause_b.configure(state = 'normal')
                self.preview()
            else:
                self.master.info_frame.insert("Start")
                
            self.isplaying = False
            self.play_pause_b.configure(text = "▶")
        else:
            self.master.info_frame.insert("video_file_list empty")
        if self.index > 0:
            self.stepB_b.configure(state = 'normal')

    def next(self):
        if self.index < len(self.video_file_list)-1:
            self.index += 1
            self.stepB_b.configure(state = 'normal')
            self.cap = cv2.VideoCapture(self.video_file_list[self.index])
            self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))
            self.update()
        else:
            self.stepF_b.configure(state = 'disabled')
            
            self.isplaying = False
            self.play_pause_b.configure(text = "▶")
            
    def prev(self):
        self.index -= 1
        self.preview()

    def preview(self):
        # print("Preview", self.index)
        # if hasattr(self, "cap"):
        #     self.cap.release()
        self.cap = cv2.VideoCapture(self.video_file_list[self.index])
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame)
        self.image = ctk.CTkImage(pil_image, size=pil_image.size)
        self.video.configure(image=self.image)
        self.cap.release()

    def update(self):
        if self.isplaying:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert frame to PIL Image
                pil_image = Image.fromarray(frame)

                # Create CTkImage from PIL Image
                self.image = ctk.CTkImage(pil_image, size=pil_image.size)

                # Set CTkImage to video panel
                self.video.configure(image=self.image)
                self.master.after(self.delay, self.update)
            else:
                if hasattr(self, "cap"):
                    self.cap.release()
                if self.fullmode:
                    self.next()
                else:
                    self.isplaying = False
                    # self.stepB_b.configure(state = 'normal')
                    self.play_pause_b.configure(text = "▶")   
        else:
            self.master.after(self.delay, self.update)

    def load_video_list(self):
        self.video_file_list = self.get_video_files()
        self.index = 0
        # insert(self.video_file_list)
        # insert(self.index)
        if hasattr(self, "cap"):
            self.cap.release()
        self.cap = cv2.VideoCapture(self.video_file_list[self.index])
        self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))  

    def update_video_list(self):
        if len(self.video_file_list) == 0:
            self.load_video_list()
        else:
            self.video_file_list = self.get_video_files()
            for video_file in self.video_file_list:
                if not video_file in self.video_file_list: 
                    self.video_file_list.append(video_file)
    
    def get_video_files(self):
        with open('config.json') as f:
            config = json.load(f)

        method = config['Method']
    
        with open('PMFL_'+method+'.txt', 'r') as f:
            video_file_list = [line.strip() for line in f]
        return video_file_list
    
    def activate(self):
        self.playmode_o.configure (state = 'normal')
        self.play_pause_b.configure(state = 'normal')
        self.stepF_b.configure(state = 'normal')
        self.stepB_b.configure(state = 'normal')

    def default(self):
        self.playmode_o.configure (state = 'disabled')
        self.play_pause_b.configure(state = 'disabled')
        self.stepF_b.configure(state = 'disabled')
        self.stepB_b.configure(state = 'disabled')
        
        self.load_logo()
        self.video_file_list = []
        self.isplaying = False
        self.index = None
        self.play_pause_b.configure(text="▶")

class Config_frame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=0)

        #Head 
        self.config_l = ctk.CTkLabel(self, text="Configuration", font = ("Helvetica", 20))
        self.config_l.grid(row=0, column=0, padx=20, pady=20, sticky="nswe", columnspan=3)

        self.func_mode = "Function Build-in"
        switch_var = ctk.StringVar(value="build-in")
        self.func_s = ctk.CTkSwitch(self, text = self.func_mode, command=self.custom_build_in, variable=switch_var, onvalue="custom", offvalue="build-in", font = self.master.label_font)
        self.func_s.grid(row=1, column=0, padx=20, pady=20, sticky="nswe")

        # Function
        self.func_l = ctk.CTkLabel(self, text="Function", font = self.master.label_font)
        self.func_l.grid(row=2, column=0, padx=20, pady=20, sticky="nsw")

        func_var = ctk.StringVar(value="x**4+3*x-4")
        self.func_o = ctk.CTkOptionMenu(self, values=["x**4+3*x-4", "10**(-2)*E**(x**2)-3*E**x+2", "ln(x**2+1)-2", "cos(7*x)-x**2", "(x+2)/(x**2-3*x+2)-1"], variable=func_var, font = self.master.label_font)
        self.func_o.grid(row=2, column=1, padx=20, pady=20, sticky="nsw")

        self.func_e = ctk.CTkEntry(self, placeholder_text="Function", state="disabled", font = self.master.label_font)
        self.func_e.grid(row=2, column=2,  padx=20, pady=20, sticky="nsw")

        #Xi
        self.xi_l = ctk.CTkLabel(self, text="Xi", font = self.master.label_font)
        self.xi_l.grid(row=3, column=0, padx=20, pady=20, sticky="nsw")

        self.xi_e = ctk.CTkEntry(self, placeholder_text="X")
        self.xi_e.grid(row=3, column=1, padx=20, pady=20, sticky="nsw")

        #REST
        self.rest_l = ctk.CTkLabel(self, text="[a, b]", font = self.master.label_font)
        self.rest_l.grid(row=4, column=0, padx=20, pady=20, sticky="nsw")

        self.resta_e = ctk.CTkEntry(self, placeholder_text="a")
        self.resta_e.grid(row=4, column=1, padx=20, pady=20, sticky="nsw")
        
        self.restb_e = ctk.CTkEntry(self, placeholder_text="b")
        self.restb_e.grid(row=4, column=2, padx=20, pady=20, sticky="nsw")

        #EPS
        self.eps_l = ctk.CTkLabel(self, text="Eps", font = self.master.label_font)
        self.eps_l.grid(row=5, column=0, padx=20, pady=20, sticky="nsw")

        self.eps_e = ctk.CTkEntry(self, placeholder_text="eps")
        self.eps_e.grid(row=5, column=1, padx=20, pady=20, sticky="nsw")

        self.suggestion()
        
    def suggestion(self):
        self.xi_e.insert(0, "0")
        self.resta_e.insert(0, "-1")
        self.restb_e.insert(0, "1")
        self.eps_e.insert(0, "0.01")
        self.master.animation_frame.iter_e.insert(0, "5")

    def custom_build_in(self):
        if self.func_s.get() == "build-in":
            self.func_s.configure(text = "Function Build-in")
            self.func_o.configure(state="normal")
            self.func_e.configure(state="disabled")
        else:
            self.func_s.configure(text = "Function Custom")
            self.func_e.configure(state="normal")
            self.func_o.configure(state="disabled")

class Animation_frame(ctk.CTkFrame):
    """
    Animation frame 
        |--Animation logic                      -   
            |-- New animation
            |-- Continue animation
            |-- Loading animation
            |-- Stop animation

        |-- Update config
            |-- Check validate
            |-- Validate
            |-- Update
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_rowconfigure((1,2), weight=1)

        self.anim_l = ctk.CTkLabel(self, text="Render", font = ("Helvetica", 20))
        self.anim_l.grid(row=0, column=0, padx=20, pady=20, sticky="nswe", columnspan=3)

        methods_var = ctk.StringVar(value="Newtons")
        self.methods_o = ctk.CTkOptionMenu(self,values=["Newtons"], variable=methods_var, font = self.master.label_font)
        self.methods_o.grid(row=1, column=0, padx=20, pady=20, sticky="nsw")

        self.iter_l = ctk.CTkLabel(self, text="Number of Iterations", font = self.master.label_font)
        self.iter_l.grid(row=1, column=1, padx=20, pady=20)

        self.iter_e = ctk.CTkEntry(self, placeholder_text="Number of Iterations")
        self.iter_e.grid(row=1, column=2, padx=20, pady=20, sticky="nse")

        self.anim_text = "Animate"
        self.anim_b = ctk.CTkButton(self, text=self.anim_text, command=self.animate, font = self.master.label_font)
        self.anim_b.grid(row=2, column=0, padx=20, pady=20, sticky="nsw")

        sequence_var = ctk.StringVar(value="1 Iteration")
        self.sequence_o = ctk.CTkOptionMenu(self, values=["1 Iteration", "Full"], command=self.sequence_update, variable=sequence_var, font = self.master.label_font)
        self.sequence_o.grid(row=2, column=1, padx=20, pady=20, sticky="nsw")

        self.update_config_button = ctk.CTkButton(self, text="Update config", command=self.update_config, font = self.master.label_font)
        self.update_config_button.grid(row=2, column=2, padx=20, pady=20, sticky="nse")
        self.valid_info = "Need to validate configurations"

        self.isvalid = False
        self.ischanged = False
        self.isanimated = False
        self.default()

    def default(self): 
        default_config = {
        "f(x)": "x**3+2*x-1",
        "dx": "",
        "d2x": "",
        "tangent": "",
        "x0": .0,
        "xi-1": .0,
        "xi": .0,
        "xi+1": .0,
        "f(x0)": .0,
        "f(xi-1)": .0,
        "f(xi)": .0,
        "f(xi+1)": .0,
        "Eps": 0.01,
        "Rest": [0, 0],
        "Method": "Newtons",
        "Quality": "l",
        "Iteration": 0,
        "Number of Iteration": 10,
        "Stop_Criteria": False,
        "Stop_animation": False,
        "Sequence": True,
        }
    
        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=4)

    def animate(self):
        self.master.info_frame.delete()
        with open('config.json') as f:
            config = json.load(f)
            
        if not self.isanimated:
            if self.isvalid:
                if not config["Stop_Criteria"] :
                    # print("Changed", self.ischanged)
                    if self.ischanged:
                        self.master.info_frame.insert("Rendering new animation\n")
                        self.master.video_frame.load_logo()
                    else:
                        self.master.info_frame.insert("Continue rendering animation\n")


                    config["Stop_animation"] = False
                    config["isFinished"] = False
                    
                    with open('config.json', 'w') as f:
                        json.dump(config, f, indent=4)

                    self.isanimated = True
                    self.ischanged = False
                    self.anim_text  = "Stop rendering animation"
                    self.master.gap_process = threading.Thread(target=gap_run, args=(self.master,))
                    # self.master.gap_process = threading.Thread(target=gap_run, args=(self.master,))
                    self.master.gap_process.start()
                elif os.stat('PMFL_'+config['Method']+'.txt').st_size !=0:
                    self.master.info_frame.insert("Loading animation\n")
                    self.master.video_frame.load_video_list()
            else:
                self.master.info_frame.insert(self.valid_info)
        else:
            config["Stop_animation"] = True
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            
            self.master.animation_process.kill()
            self.master.calculation_process.kill()
           
            method = config['Method']
            with open ('PMFL_'+method+'.txt', 'w') as pmfl_file:
                pmfl_file.write("")

            self.isanimated = False
            self.anim_text  = "Animate"

        self.anim_b.configure(text=self.anim_text)

        config["Stop_animation"] = False
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

    def update_config(self):
        self.master.info_frame.delete()
        self.validate()
        self.check_config_change()

        if self.isvalid and self.ischanged:
            self.default()
            self.master.info_frame.default()
            self.master.video_frame.default()

            self.master.info_frame.insert("Updating config!")
            with open('config.json') as f:
                config = json.load(f)

            config['f(x)'] = self.master.config_frame.func_o.get() if self.master.config_frame.func_s.get() == "build-in" else self.master.config_frame.func_e.get()
            config['xi'] = float(self.master.config_frame.xi_e.get())
            config['Eps'] = float(self.master.config_frame.eps_e.get())
            config['Rest'] = [float(self.master.config_frame.resta_e.get()), float(self.master.config_frame.restb_e.get())]
            config['Method'] = self.methods_o.get()
            config["Iteration"] = 0
            config['Number of Iteration'] = int(self.iter_e.get())
            config['Sequence'] = True if (self.sequence_o.get() == "1 Iteration") else False
            config['Stop_Criteria'] = False
            
            with open('PMFL_'+self.methods_o.get()+'.txt', 'w') as f:
                f.write('')

            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)

        self.master.info_frame.insert(self.valid_info)

    def sequence_update(self, choice):
        with open('config.json') as f:
            config = json.load(f)

        config['Sequence'] = True if (choice == "1 Iteration") else False

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

    def validate(self):
        if self.master.config_frame.func_s.get() == "build-in":
            try:
                sympify(self.master.config_frame.func_o.get())
            except (TypeError, ValueError):
                self.valid_info = f"Invalid function format in f(x): {self.master.config_frame.func_o.get()}"
                self.isvalid = False
                return
        else:
            try:
                sympify(self.master.config_frame.func_e.get())
            except (TypeError, ValueError):
                self.valid_info = f"Invalid function format in f(x): {self.master.config_frame.func_e.get()}"
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

        if xi > rest_b or xi < rest_a:
            self.valid_info = f"Invalid X0: {xi}. Must be in restriction [{rest_a}, {rest_b}]."
            self.isvalid = False
            return
        
        if eps <= 0 or eps>1:
            self.valid_info = f"Invalid Eps: {eps}. Must be in restriction [0, 1]."
            self.isvalid = False
            return
        
        if number_of_iterations <=0:
            self.valid_info = f"Invalid Number of iteration: {number_of_iterations}. Must be positive."
            self.isvalid = False
            return
    
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
        elif self.master.config_frame.func_s.get() == "build-in" and self.master.config_frame.func_o.get() != config['f(x)']:
            self.ischanged = True
        elif self.master.config_frame.func_s.get() == "custom" and self.master.config_frame.func_e.get() != config['f(x)']:
            self.ischanged = True
        else:
           self.ischanged = False

class Info_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_rowconfigure((1,2), weight=0)

        self.info_l = ctk.CTkLabel(self, text="Infobox", font = ("Helvetica", 20))
        self.info_l.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        launch_text = "Made by Arthur Dombrovskij\n"
        self.textbox = ctk.CTkTextbox(master=self, height = 100, width=400, corner_radius=0, font = ("Helvetica", 16))
        self.textbox.insert("0.0", launch_text)
        self.textbox.configure(state="disabled")

        self.textbox.grid(row=1, column=0, padx=20, pady=20, sticky="nswe", columnspan=3)
    
        self.instruction_b = ctk.CTkButton(self, text="Instruction", command=self.instruction, font = self.master.label_font)
        self.instruction_b.grid(row=2, column=0, padx=20, pady=20, sticky="we")

        self.plot_b = ctk.CTkButton(self, text="Plot", command=self.plot_result,  font = self.master.label_font)
        self.plot_b.grid(row=2, column=2, padx=20, pady=20, sticky="we")
        self.default()

    def default(self):
        if os.path.exists('result.csv'):
            os.remove('result.csv')

        if os.path.exists('memory_analysis.csv'):
            os.remove('memory_analysis.csv')
        
        with open('result.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['xi', 'f(xi)'])

    def instruction(self):
        with open('Instruction_Functions.txt', 'r') as inst:
            instruction = [line.strip() for line in inst]
        self.master.video_frame.load_manual()

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

    def plot_result(self):
        with open("result.csv", 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)

            x_data =[] 
            y_data = []

            for row in csvreader:
                x_data.append(float(row[0]))
                x_data.append(float(row[0]))
                y_data.append(0)
                y_data.append(float(row[1]))

        # print(x_data, y_data)
        with open('config.json') as f:
            config = json.load(f)

        x = symbols('x', real = True)
        f_x = sympify(config['f(x)'])

        if len(x_data) == 0:
            a =float(self.master.config_frame.resta_e.get())
            b =float(self.master.config_frame.restb_e.get())       
        else:
            a = np.min(x_data)
            b = np.max(x_data)

            a = min(a, float(self.master.config_frame.resta_e.get()))
            b = max(b, float(self.master.config_frame.restb_e.get()))
            
        # print("a, b", a, b)
        a -= 1
        b += 1
        
        x_plot = np.linspace(float(a), float(b), 1000)
        y_plot = [f_x.subs('x', v).evalf() for v in x_plot]

        x_plot_filtered=[]
        y_plot_filtered=[]
        flag = False
        for i, y_val in enumerate(y_plot):
            if y_val.is_real:
                x_plot_filtered.append(x_plot[i])
                y_plot_filtered.append(y_val)
                if not flag and not -100<y_val<100:
                    flag = True

        fig, ax =plt.subplots()

        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_position('zero')

        ax.plot(x_plot_filtered, y_plot_filtered, label='f(x)')

        plt.scatter(x_data, y_data, label='Data Points')

        ax.plot(x_data, y_data, 'b-', label='Data Connection')

        plt.xlabel('x')
        plt.ylabel('f(x)')

        plt.title('Graph of f(x) with Data Points')
        plt.legend()
        if flag:
            plt.ylim(-100, 100)
        plt.show()

def gap_run(master):
    with open('config.json') as f:
            config = json.load(f)

    isStop = config["Stop_Criteria"] or config["Stop_animation"]
    size = 0

    x = config["xi"]
    fx = config["f(xi)"]
    iter = config["Iteration"]

    master.info_frame.insert(f"Initial approximation:")
    master.info_frame.insert(f"x{iter}: {x} | f(x{iter}): {fx} \n")    

    while not isStop:
        pr = cProfile.Profile()
        with pr:
            command_calculation = [sys.executable, "methods.py"]
            master.calculation_process = subprocess.Popen(command_calculation)
            master.calculation_process.wait()

            with open('config.json') as f:
                config = json.load(f)

            x = config["xi+1"]
            fx = config["f(xi+1)"]
            iter = config["Iteration"]
            
            master.info_frame.insert(f"Iteration of calculation {iter} complete:")
            master.info_frame.insert(f"x{iter}: {x} | f(x{iter}): {fx} ")    
            
            iter = config["Iteration"]
            
            if not isStop:
                command_animation = ["manim", "-v", "WARNING", "anim.py", config['Method'], "-q"+config['Quality']]
                master.animation_process = subprocess.Popen(command_animation)

                master.animation_process.wait()

                master.info_frame.insert(f"Animation {iter} complete\n")

                with open('config.json') as f:
                    config = json.load(f)

                if not config["Stop_animation"]:
                    write_PMFL()
                    master.video_frame.update_video_list()
                    master.video_frame.activate()

            with open('config.json') as f:
                config = json.load(f)
            isStop = config["Stop_Criteria"] or config["Stop_animation"] or config["Sequence"]
            
        pr.disable()
        pr.dump_stats('cprofile_results')
        size = memory_analyse(size)
        
        with open('cprofiling_results.txt', 'a') as file: 
            file.write(f"Iteration {iter} - Profile Statistics:\n")
            profile = pstats.Stats('cprofile_results', stream=file)
            profile.print_stats()
            file.close()

    master.animation_frame.isanimated = False
    master.animation_frame.anim_b.configure(text="Animated")
    if config["Stop_Criteria"]: 
        master.info_frame.insert("Finished!!!")

def write_PMFL():
    with open('config.json') as f:
        config = json.load(f)

    qualitys = {
        "l": "480p15",
        "m": "720p30",
        "h": "1080p60"
    }
    
    quality = qualitys.get(config["Quality"])
    method = config['Method']

    project_dir = os.path.dirname(os.path.abspath(__file__))  # Get project directory

    file_path = os.path.join(project_dir, "media", "videos", "anim", quality, "partial_movie_files", method, "partial_movie_file_list.txt")

    with open(file_path, 'r') as partial_list_file, \
            open('PMFL_'+method+'.txt', 'a') as pmfl_file:
            for line in partial_list_file:
                if line.startswith('file \'file:'):
                    pmfl_file.write(line[11:-2]+ '\n')   

def memory_analyse(size):
    with open('config.json') as f:
        config = json.load(f)

    qualitys = {
        "l": "480p15",
        "m": "720p30",
        "h": "1080p60"
    }
    
    quality = qualitys.get(config["Quality"])
    method = config['Method']

    previous_size = size

    project_dir = os.path.dirname(os.path.abspath(__file__))
    media_folder_path = os.path.join(project_dir, "media", "videos", "anim", quality, "partial_movie_files", method)

    current_size = get_folder_size(media_folder_path)

    size_change = current_size - previous_size

    result = [
      current_size,
      size_change,
    #   os.path.getctime(media_folder_path)
  ]

  # Append result to the CSV file
    with open("memory_analysis.csv", "a", newline="") as f:
      writer = csv.writer(f)
      if not f.tell():  # Check if file is empty
          writer.writerow(["Total Memory", "Memory Change", "Timestamp"])
      writer.writerow(result)

    return current_size

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_size = os.path.getsize(file_path)
            total_size += file_size
    return total_size