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
        self.minsize(width=750, height=400)
        self.maxsize(width=1500, height=600)
        
        # parent container for file frame and io frame
        main_frame = tk.Frame(self, width=650, height=400, bg='grey')
        main_frame.grid(row=0, column=0, padx=10, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # variables for operations
        self.frames = {}
        self.UVsim = UVSim
        self.file_path = None

        for F in (StartPage, AccumulatorView):
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_input(self):
        # Callback funtion for read
        # frame = self.frames[InputPage]
        # frame.tkraise()
        pass 

    def output_trigger(self, output_msg: str):
        # Callback function for output
        # frame = self.frames[AccumulatorView]
        # AccumulatorView.update_output(frame, output_msg=output_msg)
        # frame.tkraise()
        pass

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

class AccumulatorView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Label for IO side of accumulatorView "Input/Output"
        self.IO_label = ttk.Label(self, text="UVsimulator Group E", font=LARGEFONT)
        self.IO_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # left side of accumulator view is for file loading and reading in the file.
        file_frame = tk.Frame(self, width=650, height=400, bg='grey')
        file_frame.grid(row=0, column=0, padx=10, pady=5)

        # Right side of the accumulator view is for IO operations while executing the code.
        io_frame = tk.Frame(self, width=650, height=400, bg='grey')
        io_frame.grid(row=0, column=1, padx=10, pady=5)

        # Label for IO side of accumulatorView "Input/Output"
        self.IO_label = ttk.Label(io_frame, text="Input/Output", font=LARGEFONT)
        self.IO_label.grid(row=0, column=0, padx=10, pady=10)

        # Entry widget for input
        self.input_entry = ttk.Entry(io_frame)
        self.input_entry.grid(row=1, column=0, padx=10, pady=10)

        # Button to run the loaded file
        run_button = ttk.Button(file_frame, text="Run File", command=lambda: self.run_file(controller))
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


# from tkinter import *
# from PIL import Image, ImageTk

# root = Tk()  # create root window
# root.title("Basic GUI Layout")  # title of the GUI window
# root.minsize(500, 400)  # specify the max size the window can expand to
# root.maxsize(900, 600)  # specify the max size the window can expand to
# root.config(bg="skyblue")  # specify background color

# root.columnconfigure([0, 1], weight=1, minsize=75)
# root.rowconfigure(0, weight=1, minsize=50)

# # Create left and right frames
# left_frame = Frame(root, width=200, height=400, bg='grey')
# left_frame.grid(row=0, column=0, padx=10, pady=5)

# right_frame = Frame(root, width=650, height=400, bg='grey')
# right_frame.grid(row=0, column=1, padx=10, pady=5)

# # Create frames and labels in left_frame
# Label(left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

# # load image to be "edited"
# image = Image.open('image.jpg')
# python_image = ImageTk.PhotoImage(image)
# # original_image = image.subsample(3,3)  # resize image using subsample
# # Label(left_frame, image=original_image).grid(row=1, column=0, padx=5, pady=5)
# # Display image in right_frame
# Label(right_frame, image=python_image).grid(row=0,column=0, padx=5, pady=5)

# # Create tool bar frame
# tool_bar = Frame(left_frame, width=180, height=185)
# tool_bar.grid(row=2, column=0, padx=5, pady=5)

# # Example labels that serve as placeholders for other widgets
# Label(tool_bar, text="Tools", relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
# Label(tool_bar, text="Filters", relief=RAISED).grid(row=0, column=1, padx=5, pady=3, ipadx=10)

# root.mainloop()