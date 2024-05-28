
        super().__init__(master, **kwargs)
        self.master = master

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.video_panel = ctk.CTkFrame(self)
        self.video_panel.grid(row=0, column=0, padx=(5,5), pady=(5,5), sticky="swe")

        self.video = ctk.CTkLabel(self.video_panel, text = None, width=width, height=height)
        self.video.grid(row=0, column=0, padx=(20,20), pady=(10,10), sticky="swe")

        self.load_logo()

        self.control_panel = ctk.CTkFrame(self)
        self.control_panel.grid(row=1, column=0, padx=10, pady=10, sticky="swe")

        func_var = ctk.StringVar(value="Play mode")
        self.playmode_o = ctk.CTkOptionMenu(self.control_panel, values=["Full", "Steps"], command=self.play_mode, variable=func_var)
        self.playmode_o.grid(row=1, column=3, padx=20, pady=20, sticky="se")

        self.button_text = "Play"
        self.play_pause_b = ctk.CTkButton(self.control_panel, text=self.button_text, command=self.play_pause)
        self.play_pause_b.grid(row=1, column=1, padx=20, pady=20, sticky="s")

        self.stepF_b = ctk.CTkButton(self.control_panel, text="Step forward", command=self.stepF, state = 'disabled')
        self.stepF_b.grid(row=1, column=2, padx=20, pady=20, sticky="s")

        self.stepB_b = ctk.CTkButton(self.control_panel, text="Step backward", command=self.stepB, state = 'disabled')
        self.stepB_b.grid(row=1, column=0, padx=20, pady=20, sticky="sw")

        self.default()
