import tkinter as tk
from tkinter import ttk, filedialog

LARGEFONT = ("Verdana", 20)

class tkinterApp(tk.Tk):
    def __init__(self, UVSim, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("UVsim")
        self.minsize(width=300, height=250)
        self.maxsize(width=1500, height=600)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.file_path = None
        self.input_command = None

        for F in (StartPage, AccumulatorView):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


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
            controller.frames[AccumulatorView].update_data(controller)
            controller.show_frame(AccumulatorView)

class AccumulatorView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.input_label = ttk.Label(self, text="Input", font=LARGEFONT)
        self.input_label.grid(row=0, column=0, padx=10, pady=10)

        # Entry widget for input
        self.input_entry = ttk.Entry(self)
        self.input_entry.grid(row=1, column=0, padx=10, pady=10)

        self.output_label = ttk.Label(self, text="Output", font=LARGEFONT)
        self.output_label.grid(row=2, column=0, padx=10, pady=10)

        # Label for displaying output text
        self.output_text = ttk.Label(self, text="", font=("Helvetica", 16))
        self.output_text.grid(row=3, column=0, padx=10, pady=10)

        # Button to run the loaded file
        run_button = ttk.Button(self, text="Run File", command=self.run_file)
        run_button.grid(row=4, column=0, padx=10, pady=10)
        
        # Button to run the loaded file
        ld_file = ttk.Button(self, text="Load New File", command= lambda: controller.frames[StartPage].load_file(controller))
        ld_file.grid(row=5, column=0, padx=10, pady=10)
        # Bind the <Return> key event to the run_file function
        # Bind the <Return> key event to the run_file function
        self.input_entry.bind("<Return>", lambda event: self.run_file(controller, self.get_input()))

    def run_file(self, controller, input_value, event=None):
        # Placeholder function to notify the user
        self.output_text.config(text=f"Waiting for input... Input Value: {input_value}")
        controller.input_command = input_value

        # You can add your file execution logic here using the controller.file_path
        # For example, you might want to read the content of the file and process it
        # You can update the output_text label accordingly
        
    def get_input(self):
        # Get the value from the input entry
        return self.input_entry.get()
    
    def update_data(self, controller):    
        # Update the labels with new data
        self.input_label.config(text=controller.file_path)
        self.output_label.config(text=controller.file_path)
        
# Driver Code - move and import these into the main function to run the application.
# app = tkinterApp()
# app.mainloop()
