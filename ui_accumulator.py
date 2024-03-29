import os
import tkinter as tk
from tkinter import ttk, filedialog
from UVsimulator import UVSimulator
from tkinter import messagebox, colorchooser
import sys


LARGEFONT = ("Verdana", 20)
SMALLFONT = ("Verdana", 10)

DEFAULTBACKGROUND = "#4c721d"
CUSTOMCOLOR = "#FFFFFF"

class tkinterApp(tk.Tk):
    def __init__(self, UVSim:UVSimulator, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("UVsim")
        self.config(bg=DEFAULTBACKGROUND)
        self.minsize(1000, 500)

        # Create a frame that will expand to fill the window
        main_frame = tk.Frame(self, bg='grey')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

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

        def primaryColor():
            primary_color = colorchooser.askcolor()[1]
            global DEFAULTBACKGROUND
            DEFAULTBACKGROUND = primary_color
            if primary_color:
                for F in (StartPage, AccumulatorView):
                    frame = F(main_frame, self)
                    frame.config(bg=DEFAULTBACKGROUND)
                    self.frames[F] = frame
                    frame.grid(row=0, column=0, sticky="nsew")
                self.show_frame(StartPage)

        def secondaryColor():
            secondary_color = colorchooser.askcolor()[1]
            global CUSTOMCOLOR
            CUSTOMCOLOR = secondary_color
            if secondary_color:
                print(secondary_color)
                for F in (StartPage, AccumulatorView):
                    frame = F(main_frame, self)
                    frame.config(bg=DEFAULTBACKGROUND)
                    self.frames[F] = frame
                    frame.grid(row=0, column=0, sticky="nsew")
                self.show_frame(StartPage)

        def newFile():
            self.show_frame(StartPage)

        my_menu = tk.Menu(self)
        self.config(menu = my_menu)

        option_menu = tk.Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Options", menu=option_menu)
        option_menu.add_command(label="Change Primary Color", command=primaryColor)
        option_menu.add_command(label="Change Secondary Color", command=secondaryColor)
        option_menu.add_command(label="New File", command=newFile)
        option_menu.add_separator()
        option_menu.add_command(label="Exit App", command=self.quit)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_input(self):
        # Callback function for read
        print("read callback executing inside Tkinterapp")
        frame = self.frames[AccumulatorView]
        frame.send_btn.config(state="normal")
        messagebox.showinfo("Waiting for Input", "Click \"Ok\" and enter a valid BasicML word")
        frame.tkraise()

    def output_trigger(self, output_msg: str):
        # Callback function for output
        frame = self.frames[AccumulatorView]
        AccumulatorView.update_output(frame, self, output_msg=output_msg)
        frame.tkraise()

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select a file")

        if file_path:
            self.file_path = file_path
            self.frames[AccumulatorView].update_input(self)
            result = self.UVsim.read_file(self.file_path)
            self.file_contents = result

            self.frames[AccumulatorView].update_table(self)

            self.show_frame(AccumulatorView)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Set up grid weights for responsive resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = ttk.Label(self, text="Welcome to UVSim!", font=LARGEFONT, justify='center')
        label.grid(row=0, column=0, padx=10, pady=10)

        selectFileBTN = ttk.Button(self, text="Choose a file", command=lambda: controller.load_file())
        selectFileBTN.grid(row=1, column=0, padx=10, pady=30)

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
        file_frame = tk.Frame(self, bg=CUSTOMCOLOR, bd=2, relief='ridge')
        file_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        file_frame.config(bg=CUSTOMCOLOR)

        io_frame = tk.Frame(self, bg=CUSTOMCOLOR, bd=2, relief='ridge')
        io_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        io_frame.config(bg=CUSTOMCOLOR)

        # Set up grid weights for responsive resizing within frames
        file_frame.grid_rowconfigure(0, weight=1)
        file_frame.grid_columnconfigure(0, weight=1)

        io_frame.grid_rowconfigure(0, weight=1)
        io_frame.grid_columnconfigure(0, weight=1)

        input_frame = tk.Frame(io_frame, bg=CUSTOMCOLOR, bd=2, relief='ridge')
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        input_frame.config(bg="gray")
        # Set up grid weights for responsive resizing
        input_frame.grid_rowconfigure(0, weight=1)
        input_frame.grid_columnconfigure(0, weight=1)

        output_frame = tk.Frame(io_frame, bg=CUSTOMCOLOR, bd=2, relief='ridge')
        output_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        output_frame.config(bg="gray")
        # Set up grid weights for responsive resizing
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        # File manager inner frame on the left side
        self.left_inner_frame = tk.Frame(file_frame, bg=CUSTOMCOLOR)
        self.left_inner_frame.grid(row=2, column=0, padx=10, pady=10)
        self.left_inner_frame.config(bg="gray")
        self.left_inner_frame.grid_rowconfigure(0, weight=1)
        self.left_inner_frame.grid_columnconfigure(0, weight=1)

        # Table frame for file editing
        self.table_frame = tk.Frame(self.left_inner_frame, bg=CUSTOMCOLOR)
        self.table_frame.grid(row=2, column=0)
        self.table_frame.config(bg="gray")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

       # Treeview widget for displaying and editing data
        self.tree = ttk.Treeview(self.table_frame, columns=('Data'), show='headings')
        self.tree.heading('Data', text='BasicML')
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tree.bind("<<TreeviewSelect>>", lambda event: self.item_select(event=event, controller=controller))
        if sys.platform == 'darwin':  # macOS
            self.tree.bind("<Command-v>", lambda event: self.paste_text(event=event) )
        else:  # Windows and other platforms
            self.tree.bind("<Control-v>", lambda event: self.paste_text(event=event))

        if sys.platform == 'darwin':  # macOS
            self.tree.bind("<Command-c>", lambda event: self.copy_selection(event=event, controller=controller) )
        else:  # Windows and other platforms
            self.tree.bind("<control-c>", lambda event: self.copy_selection(event=event, controller=controller) )

        self.tree.bind("<Delete>", lambda event: self.item_delete(event=event, controller=controller))

        # Labels for file loading section
        self.file_frame_label = ttk.Label(self.left_inner_frame, text="File Editor/Manager", font=LARGEFONT)
        self.file_frame_label.grid(row=0, column=0, padx=10, pady=10, sticky="new")

        # Label to display selected file name
        self.file_name_label = ttk.Label(self.left_inner_frame, text="No File selected", font=SMALLFONT, justify="center")
        self.file_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        # Editor entry widget
        self.editor_entry = tk.Text(self.table_frame)
        self.editor_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Button to select and run the loaded file
        self.run_button = ttk.Button(self.left_inner_frame, text="Run File", command=lambda: self.run_file(controller))
        self.run_button.grid(row=3, column=0, padx=10, pady=10, sticky="new")

        # Button to select and run the loaded file
        self.new_file_btn = ttk.Button(self.left_inner_frame, text="Load New", command=lambda: controller.load_file())
        self.new_file_btn.grid(row=3, column=1, padx=10, pady=10, sticky="new")

        # Button to submit changed value
        self.editor_btn = ttk.Button(self.left_inner_frame, text="Submit Changes", command=lambda: controller.load_file())
        self.editor_btn.grid(row=4, column=0, padx=10, pady=10, sticky="new")

        # Labels and widgets for IO operations section
        self.IO_label = ttk.Label(input_frame, text="Input", font=LARGEFONT, background="gray")
        self.IO_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.send_btn= ttk.Button(input_frame, text="Resume Execution", command=lambda: self.send_input(controller))
        self.send_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.send_btn.config(state="disabled")

        self.output_label = ttk.Label(output_frame, text="Output", font=LARGEFONT, justify="center")
        self.output_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.output_text = ttk.Label(output_frame, text="", font=SMALLFONT, wraplength=500)
        self.output_text.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Bind the <Return> key event to the run_file function
        self.input_entry.bind("<Return>", lambda event: self.send_input(controller, event))
    
    def edit_text(self, event):
        value = self.editor_entry.get()
        # selected_item = 
        

    def paste_text(event):
        widget = event.widget
        text = widget.clipboard_get()
        widget.insert(tk.INSERT, text)

    def item_delete(self, event, controller:tkinterApp):
        print(controller.file_contents)

        print("delete")
        for i, item in enumerate(self.tree.selection()):
            # controller.file_contents
            self.tree.delete(item)
        
        print(controller.file_contents)

    def item_select(self, event, controller:tkinterApp):
        print(self.tree)
        for i in self.tree.selection():
            print(self.tree.item(i)["values"])

    def copy_selection(self, event, controller):
        self.tree.clipboard_clear()
        selection = self.tree.selection()
        column = self.tree.identify_column(event.x)
        column_no = int(column.replace("#", "")) - 1
        print("copy ")
        for each in selection:
            try:
                value = self.tree.item(each)["values"][column_no]
                if value != 0:
                    if value > 0:
                        self.tree.clipboard_append('+' + str(value))
                    else:
                        self.tree.clipboard_append('-' + str(value))
                else:
                    self.tree.clipboard_append("+0000")
            except:
                pass
            # print(each)
        print(self.tree.clipboard_get())


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
        self.output_text.config(text= output_msg)
        controller.UVsim.resume_execution()

    def send_input(self, controller:tkinterApp):
        input = self.input_entry.get()
        self.send_btn.config(state="disabled")
        controller.UVsim.resume_execution(input)

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
