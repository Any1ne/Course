import customtkinter as ctk

from sympy import *
from PIL import Image
from numpy import linspace
import cv2
import csv
import json
import os
import subprocess
import threading
import time
import matplotlib.pyplot as plt
import sys

class GINM(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GINM")
        self.geometry("1400x900")

        # self.minsize(width, height)
        # self.maxsize(width, height)

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 2), weight=1)

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

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.video_panel = ctk.CTkFrame(self)
        self.video_panel.grid(row=0, column=0, padx=(5,5), pady=(5,5), sticky="swe")

        self.video = ctk.CTkLabel(self.video_panel, width=width, height=height)
        self.video.grid(row=0, column=0, padx=(20,20), pady=(10,10), sticky="swe")

        self.load_logo()

        self.control_panel = ctk.CTkFrame(self)
        self.control_panel.grid(row=1, column=0, padx=10, pady=10, sticky="swe")

        func_var = ctk.StringVar(value="Play mode")
        self.playmode_o = ctk.CTkOptionMenu(self.control_panel, values=["Steps", "Full"], command=self.play_mode, variable=func_var)
        self.playmode_o.grid(row=1, column=3, padx=20, pady=20, sticky="se")

        self.button_text = "Play"
        self.play_pause_b = ctk.CTkButton(self.control_panel, text=self.button_text, command=self.play_pause)
        self.play_pause_b.grid(row=1, column=1, padx=20, pady=20, sticky="s")

        self.stepF_b = ctk.CTkButton(self.control_panel, text="Step forward", command=self.stepF, state = 'disabled')
        self.stepF_b.grid(row=1, column=2, padx=20, pady=20, sticky="s")

        self.stepB_b = ctk.CTkButton(self.control_panel, text="Step backward", command=self.stepB, state = 'disabled')
        self.stepB_b.grid(row=1, column=0, padx=20, pady=20, sticky="sw")

        self.default()

    def load_logo(self):
        project_dir = os.path.dirname(os.path.abspath(__file__))

        path_logo = os.path.join(project_dir, "media", "images", "logo", "ManimCELogo_ManimCE_v0.18.1.png")

        if not os.path.exists(path_logo):
            logo = ["manim", "-v", "WARNING", "logo.py", "ManimCELogo", "-qh"]
            process_logo = subprocess.Popen(logo)
            process_logo.wait()

        self.logo = Image.open(path_logo) 
        self.image = ctk.CTkImage(dark_image=self.logo, size=self.logo.size)
        self.video.configure(image=self.image)

    def play_mode(self):
        pass

    def stepF(self):
        if self.index!=None:
            self.master.info_frame.insert(str(self.index))
        if len(self.video_file_list) != 0:
            self.cap = cv2.VideoCapture(self.video_file_list[self.index])
            self.delay = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))

            self.update()

            if self.index < len(self.video_file_list)-2:
                self.index += 1
                self.stepB_b.configure(state = 'normal')
            else:
                self.master.info_frame.insert("END")
                self.button_text
                self.play_pause_b.configure(text=self.button_text)
                self.stepF_b.configure(state = 'disabled')
                self.isplaying = False

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

    def stepB(self):
        if self.index!=None:
            self.master.info_frame.insert(str(self.index))
        if len(self.video_file_list) != 0:
            if self.index > 1:
                self.index -= 1
                self.stepF_b.configure(state = 'normal')
            else:
                self.master.info_frame.insert("Start")
                self.stepB_b.configure(state = 'disabled')
                self.isplaying = False

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
                self.image = ctk.CTkImage(pil_image, size=pil_image.size)

                # Set CTkImage to video panel
                self.video.configure(image=self.image)
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
                if not video_file in self.video_file_list: ### adding video on the list !!!!
                    self.video_file_list.append(video_file)
        print(self.video_file_list)
    
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
        self.button_text = "Play"
        self.play_pause_b.configure(text=self.button_text)

class Config_frame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.grid_columnconfigure((1,2), weight=0)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=0)

        #Head 
        self.config_l = ctk.CTkLabel(self, text="Configuration")
        self.config_l.grid(row=0, column=0, padx=20, pady=20, sticky="nsw")

        self.func_mode = "Function Build-in"
        switch_var = ctk.StringVar(value="build-in")
        self.func_s = ctk.CTkSwitch(self, text = self.func_mode, command=self.custom_build_in, variable=switch_var, onvalue="custom", offvalue="build-in")
        self.func_s.grid(row=1, column=1, padx=20, pady=20, sticky="nswe", columnspan = 2 )

        # Function
        self.func_l = ctk.CTkLabel(self, text="Function")
        self.func_l.grid(row=2, column=0, padx=20, pady=20, sticky="nsw")

        func_var = ctk.StringVar(value="x**2+2*x+1")
        self.func_o = ctk.CTkOptionMenu(self, values=["x**2+2*x+1", "x**4+3*x-4"], command=self.optionmenu_callback, variable=func_var)
        self.func_o.grid(row=2, column=1, padx=20, pady=20, sticky="nsw")

        self.func_e = ctk.CTkEntry(self, placeholder_text="Function", state="disabled")
        self.func_e.grid(row=2, column=2,  padx=20, pady=20, sticky="nsw")

        #Xi
        self.xi_l = ctk.CTkLabel(self, text="Xi")
        self.xi_l.grid(row=3, column=0, padx=20, pady=20, sticky="nsw")

        self.xi_e = ctk.CTkEntry(self, placeholder_text="X")
        self.xi_e.grid(row=3, column=1, padx=20, pady=20, sticky="nsw")

        #REST
        self.rest_l = ctk.CTkLabel(self, text="[a, b]")
        self.rest_l.grid(row=4, column=0, padx=20, pady=20, sticky="nsw")

        self.resta_e = ctk.CTkEntry(self, placeholder_text="a")
        self.resta_e.grid(row=4, column=1, padx=20, pady=20, sticky="nsw")
        
        self.restb_e = ctk.CTkEntry(self, placeholder_text="b")
        self.restb_e.grid(row=4, column=2, padx=20, pady=20, sticky="nsw")

        #EPS
        self.eps_l = ctk.CTkLabel(self, text="Eps")
        self.eps_l.grid(row=5, column=0, padx=20, pady=20, sticky="nsw")

        self.eps_e = ctk.CTkEntry(self, placeholder_text="eps")
        self.eps_e.grid(row=5, column=1, padx=20, pady=20, sticky="nsw")

        self.suggestion()
        
    def suggestion(self):
        self.xi_e.insert(0, "1")
        self.resta_e.insert(0, "-1")
        self.restb_e.insert(0, "1")
        self.eps_e.insert(0, "0.01")
        self.master.animation_frame.iter_e.insert(0, "10")

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
    """
    
    App                                         - root frame 
        |-- Edit_File_Menu                      - file level functions
                |-- Dialog_Export_Xflr5_Flz     - handle export to Xflr5 and FLZ_vortex 
                |-- Dialog_Export_Dxf           - handle export to DXF file 
                |-- Dialog_Load_DXF             - import DXF as reference or a main planform  
        |-- Edit                                - parent frame for  edit sub frames 
                |-- Edit_Wing                   - main wing data 
                |-- Edit_Wing_Planform          - parameters for a specific planform type 
                |-- Edit_WingSection            - select and edit a single wing section 
                        :
                        |-- Widgets             - wrapper for CTk widgets - get, set their data 
                        |-- Field_Widget        - entry field with label and spin buttons
                        |-- Header_Widget       - a page header  
                        ...                     - ...

        |-- Diagrams                            - the master to select one of the diagrams
                |-- Diagram_Planform            - the planform (outline) of a half wing 
                |-- ChordDistribution           - normalized chord distribution of the wing
                |-- Airfoils                    - the airfoils at the wing sections 
                        :
                        |-- Artists             - helper to plot a wing object on a matplotlib axes
                        |-- PlanformArtist      - plots the planform 
                        |-- SectionArtist       - plots the wing sections 
                        ...                     - ...


    Animation frame 
        |--Animate
            |-- New animation
            |-- Continue animation
            |-- Old config
            |-- Stop animation

        |-- Update config
            |-- Check validate
            |-- Validate
            |-- Update

                -----
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.grid_columnconfigure((0,2), weight=1)
        self.grid_rowconfigure((0,1), weight=1)

        methods_var = ctk.StringVar(value="Newtons")
        self.methods_o = ctk.CTkOptionMenu(self,values=["Newtons"], variable= methods_var)
        self.methods_o.grid(row=0, column=0, padx=20, pady=20, sticky="nsw")

        self.iter_l = ctk.CTkLabel(self, text="Number of Iterations")
        self.iter_l.grid(row=0, column=1, padx=20, pady=20)

        self.iter_e = ctk.CTkEntry(self, placeholder_text="Number of Iterations")
        self.iter_e.grid(row=0, column=2, padx=20, pady=20, sticky="nse")

        self.anim_text = "Animate"
        self.anim_b = ctk.CTkButton(self, text=self.anim_text, command=self.animate)
        self.anim_b.grid(row=1, column=0, padx=20, pady=20, sticky="nsw")

        sequence_var = ctk.StringVar(value="1 Iteration")
        self.sequence_o = ctk.CTkOptionMenu(self, values=["1 Iteration", "Full"], variable=sequence_var)
        self.sequence_o.grid(row=1, column=1, padx=20, pady=20, sticky="nsw")

        self.valid_b = ctk.CTkButton(self, text="Update config", command=self.update_config)
        self.valid_b.grid(row=1, column=2, padx=20, pady=20, sticky="nse")
        self.valid_info = "Need to validate configurations"

        self.isvalid = False
        self.ischanged = False
        self.isanimated = False
        self.default()

    def default(self):
         
        default_config = {
        "f(x)": "x**3+2*x+1",
        "dx": "",
        "d2x": "",
        "tangent": "",
        #"xi-1": 0.0,
        "xi": 1.0,
        "xi+1": 0.0,
        #"f(xi-1)": 0.0,
        "f(xi)": 0.0,
        "f(xi+1)": 0.0,
        "Eps": 0.01,
        "Rest": [0, 0],
        "Method": "Newtons",
        "Quality": "l",
        "Iteration": 0,
        "Number of Iteration": 20,
        "Stop_Criteria": False,
        "Stop_animation": False,
        "Sequence": True,
        "isFinished": False
        }
    
        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=4)

    def animate(self):
        #print(self.isanimated)
        with open('config.json') as f:
            config = json.load(f)
            
        if not self.isanimated:
            if self.isvalid:
                if self.ischanged or not config["isFinished"]:
                    if config['Iteration'] == 0:
                        self.master.video_frame.load_logo()


                    config['Stop_Criteria'] = False
                    config["Stop_animation"] = False
                    config["isFinished"] = False

                    with open('config.json', "w") as f:
                        json.dump(config, f)

                    self.isanimated = True
                    self.anim_text  = "Stop Animate"
                    command_gap = [sys.executable, "gap.py"]
                    self.gap_process = subprocess.Popen(command_gap)

                    self.monitor_thread = threading.Thread(target=fmt_run, args=(self.master,))
                    self.monitor_thread.start()
                elif os.stat('PMFL_'+config['Method']+'.txt').st_size !=0:

                    self.master.video_frame.load_video_list()
            else:
                self.master.info_frame.insert(self.valid_info)
        else:
            self.isanimated = False
            self.anim_text  = "Animate"

            config["Stop_animation"] = True

            with open('config.json', "w") as f:
                json.dump(config, f)

        self.anim_b.configure(text=self.anim_text)
        print(self.isanimated)
        print(f"PMFL size: {os.stat('PMFL_'+config['Method']+'.txt').st_size}")

    def update_config(self):
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
            config['Number of Iteration'] = int(self.iter_e.get())
            config['Sequence'] = True if (self.sequence_o.get() == "1 Iteration") else False
            config["isFinished"] = False

            with open('PMFL_'+self.methods_o.get()+'.txt', 'w') as f:
                f.write('')

            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)

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

        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1), weight=1)

        launch_text = "Made by Arthur Dombrovskij\n"
        self.textbox = ctk.CTkTextbox(master=self, height = 100, width=400, corner_radius=0)
        self.textbox.insert("0.0", launch_text)
        self.textbox.configure(state="disabled")

        self.textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nswe", columnspan=3)\
    
        self.instruction_b = ctk.CTkButton(self, text="Instruction", command=self.instruction)
        self.instruction_b.grid(row=1, column=0, padx=20, pady=20, sticky="we")

        self.plot_b = ctk.CTkButton(self, text="Plot", command=self.plot_result)
        self.plot_b.grid(row=1, column=2, padx=20, pady=20, sticky="we")
        self.default()

    def default(self):
        #self.delete()

        if os.path.exists('data.csv'):
            os.remove('data.csv')
        with open('data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['xi', 'f(xi)'])

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

    def plot_result(self):
        with open("data.csv", 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
    
            # Пропускаємо заголовок
            next(csvreader)

            x_data =[] 
            y_data = []
        
        # Зчитуємо рядки та заповнюємо масиви
            for row in csvreader:
                x_data.append(float(row[0]))  # або int(row[0]) залежно від типу даних
                y_data.append(float(row[1]))  # або int(row[1]) залежно від типу даних

        print(x_data, y_data)

        # Define the function f(x) using SymPy syntax
        with open('config.json') as f:
            config = json.load(f)

        x = symbols('x')
        f_x = eval(config['f(x)'])

        x_plot = linspace(config['Rest'][0], config['Rest'][1], 1000)  # Adjust range as needed

        # Generate function values for the plot range
        y_plot = [f_x.subs('x', v) for v in x_plot]

        # Create the plot
        plt.plot(x_plot, y_plot, label='f(x)')

        plt.scatter(x_data, y_data, label='Data Points')

        # Connect data points with a line
        plt.plot(x_data, y_data, 'b-', label='Data Connection')

        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Graph of f(x) with Data Points')
        plt.legend()

        # Display the plot
        plt.show()

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
    
    isFinished = config["isFinished"]

    while not isFinished :
        with open('PMFL_'+method+'.txt', 'r') as f:
            file_lines = f.readlines()
        file_lines_stripped = [line.strip() for line in file_lines]

        if len(file_lines_stripped) > len(master.video_frame.video_file_list):                                      ### Checking ???
            master.info_frame.insert("Updating!!!")
            master.video_frame.update_video_list()
            master.video_frame.activate()

        with open('config.json') as f:
            config = json.load(f)

        isFinished = config["isFinished"]

        time.sleep(2)

    master.info_frame.insert("Finished!!!")
    master.animation_frame.isanimated = False
    master.animation_frame.anim_b.configure(text="Animated")

def test():
    test = GINM()
    test.mainloop()
    ###close program
    test.info_frame.insert("end")

test()

