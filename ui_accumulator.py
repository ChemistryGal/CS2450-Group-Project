import os
import tkinter as tk
from tkinter import ttk, filedialog
from UVsimulator import UVSimulator
from tkinter import messagebox

LARGEFONT = ("Verdana", 20)
SMALLFONT = ("Verdana", 10)

UVUBACKGROUND = "green"
DEFAULTBACKGROUND = "gray"

class tkinterApp(tk.Tk):
    def __init__(self, UVSim:UVSimulator, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("UVsim")
        self.config(bg="gray")
        self.minsize(500, 500)

        # Create a frame that will expand to fill the window
        main_frame = tk.Frame(self, bg='grey')
        main_frame.pack(expand=True, fill='both')

        # Set up grid weights for responsive resizing
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Variables for operations
        self.frames = {}
        self.UVsim = UVSim
        self.file_path = None
        self.file_contents : list = []

        for F in (StartPage, AccumulatorView):
            frame = F(main_frame, self)
            frame.config(bg=DEFAULTBACKGROUND)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_input(self):
        # Callback function for read
        print("read callback executing inside Tkinterapp")
        frame = self.frames[AccumulatorView]
        frame.send_btn.config(state="normal")
        messagebox.showinfo("Waiting for Input", "Please provide input.")
        frame.tkraise()

    def output_trigger(self, output_msg: str):
        # Callback function for output
        frame = self.frames[AccumulatorView]
        AccumulatorView.update_output(frame, self, output_msg=output_msg)
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Set up grid weights for responsive resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = ttk.Label(self, text="Welcome to UVSim!", font=LARGEFONT, justify='center')
        label.grid(row=0, column=0, padx=10, pady=10)

        selectFileBTN = ttk.Button(self, text="Choose a file", command=lambda: self.load_file(controller))
        selectFileBTN.grid(row=1, column=0, padx=10, pady=30)

    def load_file(self, controller: tkinterApp):
        file_path = filedialog.askopenfilename(title="Select a file")

        if file_path:
            controller.file_path = file_path
            controller.frames[AccumulatorView].update_input(controller)
            result = controller.UVsim.read_file(controller.file_path)
            controller.file_contents = result

            controller.frames[AccumulatorView].update_table(controller)


            controller.show_frame(AccumulatorView)

class AccumulatorView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Set up grid weights for responsive resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure([0,1], weight=1)

        # Label for IO side of accumulatorView "Input/Output"
        self.IO_label = ttk.Label(self, text="UVsimulator Group E", font=LARGEFONT)
        self.IO_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Frames for file loading and IO operations
        file_frame = tk.Frame(self, bg='grey', bd=2, relief='ridge')
        file_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        file_frame.config(bg="gray8")

        io_frame = tk.Frame(self, bg='grey', bd=2, relief='ridge')
        io_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        io_frame.config(bg="gray8")

        # Set up grid weights for responsive resizing within frames
        file_frame.grid_rowconfigure(0, weight=1)
        file_frame.grid_columnconfigure(0, weight=1)

        io_frame.grid_rowconfigure(0, weight=1)
        io_frame.grid_columnconfigure(0, weight=1)

        input_frame = tk.Frame(io_frame, bg='grey', bd=2, relief='ridge')
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        input_frame.config(bg="gray")
        # Set up grid weights for responsive resizing
        input_frame.grid_rowconfigure(0, weight=1)
        input_frame.grid_columnconfigure(0, weight=1)

        output_frame = tk.Frame(io_frame, bg='grey', bd=2, relief='ridge')
        output_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        output_frame.config(bg="gray")
        # Set up grid weights for responsive resizing
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        # Labels for file loading section
        self.file_frame_label = ttk.Label(file_frame, text="File Manager", font=LARGEFONT)
        self.file_frame_label.grid(row=0, column=0, padx=10, pady=10, sticky="new")

        # Label to display selected file name
        self.file_name_label = ttk.Label(file_frame, text="No File selected", font=SMALLFONT, justify="center")
        self.file_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        # Table frame for file editing
        self.table_frame = tk.Frame(file_frame, bg='grey')
        self.table_frame.grid(row=2, column=0)
       # Treeview widget for displaying and editing data
        self.tree = ttk.Treeview(self.table_frame, columns=('Content'), show='headings')
        self.tree.heading('Content', text='Content')
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.tree.bind("<Button-1>", self.on_double_click)

        # Button to select and run the loaded file
        self.run_button = ttk.Button(file_frame, text="Run File", command=lambda: self.run_file(controller))
        self.run_button.grid(row=3, column=0, padx=10, pady=10, sticky="new")

        # Labels and widgets for IO operations section
        self.IO_label = ttk.Label(input_frame, text="Input", font=LARGEFONT, background="gray")
        self.IO_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.send_btn= ttk.Button(input_frame, text="Resume Execution", command=lambda: self.send_input(controller))
        self.send_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.send_btn.config(state="disabled")

        self.output_label = ttk.Label(output_frame, text="Output", font=LARGEFONT, justify="center")
        self.output_label.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.output_text = ttk.Label(output_frame, text="", font=SMALLFONT, wraplength=500)
        self.output_text.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # Bind the <Return> key event to the run_file function
        self.input_entry.bind("<Return>", lambda event: self.run_file(controller, event))
    

    # def load_file(self, controller: tkinterApp ):
    #     result = controller.UVsim.read_file(controller.file_path)

    def run_file(self, controller: tkinterApp, event=None):
        self.output_text.config(text="")
        self.get_table_data(controller=controller)
        result = controller.UVsim.load_program(controller.file_contents)
        controller.UVsim.run_program(read_callback=controller.get_input, write_callback=controller.output_trigger)

        if result == 1:
            controller.show_frame(StartPage)

    def get_table_data(self, controller):
        result = self.table_frame.winfo_children()
        valueLyst = []
        for i in result:
            valueLyst.append(i)
        print(valueLyst)

    def get_input(self, controller):
        return self.input_entry.get()

    def update_input(self, controller):
        file = os.path.basename(controller.file_path)
        self.file_name_label.config(text=file, font=('Helvetica',14,'bold'), justify="center")

    def update_output(self, controller, output_msg ):
        current_text = self.output_text.cget("text")
        self.output_text.config(text= current_text + "\n" + output_msg)
        controller.UVsim.resume_execution()

    def send_input(self, controller:tkinterApp):
        input = self.input_entry.get()
        self.send_btn.config(state="disabled")
        controller.UVsim.resume_execution(input)

    def on_double_click(self, event):
        try:
            item = self.tree.selection()[0]
            column = self.tree.identify_column(event.x)

            # Check if column exists
            if column:
                column = int(str(column).replace('#', ''))
                row = self.tree.item(item, 'values')

                # Create an Entry widget for editing
                entry = tk.Entry(self.tree, validate='key')
                entry.insert(0, row[0])
                entry.bind('<Return>', lambda _: self.update_data(item, column))

                # Place the Entry widget in the Treeview widget
                self.tree.focus_set()
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.set(item, column, '')
                self.tree.bind('<Return>', lambda _: self.update_data(item, column))
                self.tree.bind('<Escape>', lambda _: self.update_data(item, column))
                self.tree.bind('<FocusOut>', lambda _: self.update_data(item, column))
                self.tree.focus(item, column=column)
                self.tree.window_create(item, window=entry)
                entry.focus_set()
                self.entry = entry  # Store the Entry widget to use later
        except IndexError:
            print("No item was selected.")


    def update_table(self, controller):
        # Clear existing data from the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load data from the controller
        data = controller.file_contents
        for i, item in enumerate(data):
            self.tree.insert('', 'end', values=(item,))

    def update_data(self, item, column):
        new_value = self.entry.get()
        self.tree.item(item, values=(new_value,))
        self.entry.destroy()