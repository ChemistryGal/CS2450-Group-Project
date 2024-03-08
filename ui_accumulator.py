import os
import tkinter as tk
from tkinter import ttk, filedialog
from UVsimulator import UVSimulator

LARGEFONT = ("Verdana", 20)
SMALLFONT = ("Verdana", 10)

class tkinterApp(tk.Tk):
    def __init__(self, UVSim:UVSimulator, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("UVsim")
        self.minsize(width=750, height=300)
        self.maxsize(width=1500, height=600)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.UVsim = UVSim
        self.frames = {}
        self.file_path = None
        self.input_command = None

        for F in (StartPage, AccumulatorView, InputPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_input(self):
        frame = self.frames[InputPage]
        frame.tkraise()

    def output_trigger(self, output_msg: str):
        frame = self.frames[AccumulatorView]
        AccumulatorView.update_output(frame, output_msg=output_msg)
        frame.tkraise()


class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Input side
        self.input_label = ttk.Label(self, text="Waiting for User input - Enter a Signed four digit code", font=LARGEFONT)
        self.input_label.grid(row=0, column=0, padx=10, pady=10)

        # Entry widget for input
        self.input_entry = ttk.Entry(self)
        self.input_entry.grid(row=1, column=0, padx=10, pady=10)

        selectFileBTN = ttk.Button(self, text="submit", command=lambda: self.send_input(controller))
        selectFileBTN.grid(row=2, column=0, padx=10, pady=30)

    def send_input(self, controller:tkinterApp) -> str:
        # TODO add vaildation checking for input 
        input = self.input_entry.get()
        controller.show_frame(AccumulatorView)
        controller.UVsim.resume_execution(input)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        label = ttk.Label(self, text="Welcome to UVSim!", font=LARGEFONT, justify='center')
        label.grid(row=0, column=0, padx=10, pady=10)

        selectFileBTN = ttk.Button(self, text="Choose a file", command=lambda: self.load_file(controller))
        selectFileBTN.grid(row=1, column=0, padx=10, pady=30)

    def load_file(self, controller: tkinterApp):
        file_path = filedialog.askopenfilename(title="Select a file")

        if file_path:
            controller.file_path = file_path
            controller.frames[AccumulatorView].update_input(controller)
            controller.show_frame(AccumulatorView)

class AccumulatorView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Input side
        self.input_label = ttk.Label(self, text="Input", font=LARGEFONT)
        self.input_label.grid(row=0, column=0, padx=10, pady=10)

        # Entry widget for input
        self.input_entry = ttk.Entry(self)
        self.input_entry.grid(row=1, column=0, padx=10, pady=10)

        # Button to run the loaded file
        run_button = ttk.Button(self, text="Run File", command=lambda: self.run_file(controller))
        run_button.grid(row=2, column=0, padx=10, pady=10)

        # Load new file button
        # ld_file = ttk.Button(self, text="Load New File", command=lambda: controller.frames[StartPage].load_file(controller))
        # ld_file.grid(row=3, column=0, padx=10, pady=10)

        # Output side
        self.output_label = ttk.Label(self, text="Output", font=LARGEFONT, justify="right")
        self.output_label.grid(row=0, column=1, padx=10, pady=10)

        # Label for displaying output text
        self.output_text = ttk.Label(self, text="", font=("Helvetica", 16))
        self.output_text.grid(row=1, column=1, padx=50, pady=50)

        #Horizontal Line dividing
        

        # Bind the <Return> key event to the run_file function
        self.input_entry.bind("<Return>", lambda event: self.run_file(controller, event))

    def run_file(self, controller: tkinterApp, event=None):
        # Placeholder function to notify the user
        result = controller.UVsim.load_program(controller.file_path)
        controller.UVsim.run_program(read_callback=controller.get_input, write_callback=controller.output_trigger)
        # write_var = controller.UVsim.shared_output
        # if write_var is not None:
        #     index = 1
        #     for out in write_var:
        #         self.output_write = ttk.Label(self, text=out, font=('Helvetica',14,'bold'), foreground ="blue")
        #         self.output_write.grid(row=index, column=1, padx=10, pady=10)
        #         index+=1
        #controller.UVsim.run_program()
        if result == 1:
            controller.show_frame(StartPage)

    def get_input(self, controller):
        # Get the value from the input entry
        return self.input_entry.get()

    def update_input(self, controller):
        file = os.path.basename(controller.file_path)
        self.input_label.config(text=file, font=('Helvetica',14,'bold'), justify="center", foreground ="Green")

    def update_output(self, output_msg):
        current_text = self.output_text.cget("text")
        self.output_text.config(text= current_text + "\n" + output_msg)


    # def update_data(self, controller):    
    #     # Update the labels with new data
    #     self.input_label.config(text=controller.file_path)
    #     self.output_label.config(text=controller.file_path)

