import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import asksaveasfilename
from UVsimulator import UVSimulator
from tkinter import messagebox, colorchooser
import sys


LARGEFONT = ("Verdana", 20)
SMALLFONT = ("Verdana", 10)

DEFAULTBACKGROUND = "#4c721d"
CUSTOMCOLOR = "gray"

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("UVsim")
        self.config(bg=DEFAULTBACKGROUND)
        self.minsize(1000, 500)

        # Button to add new tabs
        self.add_tab_button = ttk.Button(self, text="Add Tab", command=self.add_tab)
        self.add_tab_button.pack(side='left', padx=10, pady=10)

        # Notebook that will hold tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', pady=20, padx=10)

        # Add window size label
        self.label = tk.Label(self, text="Window size: 500x500")
        self.label.pack(side="bottom", padx=0, pady=3)
        
        # Bind the resize event
        self.bind("<Configure>", lambda event: self.on_resize(event))

        # Add an Initial Tab to Start with
        self.add_tab()

        # Menu bar setup
        my_menu = tk.Menu(self)
        self.config(menu=my_menu)
        option_menu = tk.Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Options", menu=option_menu)
        option_menu.add_command(label="Change Primary Color", command= lambda :self.change_primary_color())
        option_menu.add_command(label="Change Secondary Color", command= lambda :self.change_secondary_color())
        option_menu.add_command(label="New File", command= lambda :self.new_file())
        option_menu.add_separator()
        option_menu.add_command(label="Exit App", command=self.quit)

    def on_resize(self, event):
        # Display the current size of the window in the label
        self.label.config(text=f"Window size: {self.winfo_width()}x{self.winfo_height()}")
        # Adjust layout or other elements based on the size
        if self.winfo_width() < 400 or self.winfo_height() < 200:
            self.label.config(bg='red', fg='white')
        else:
            self.label.config(bg='black', fg='white')

    def add_tab(self):
        # Create a new TabsPage frame (assumed to be defined elsewhere)
        frame = TabsPage(self.notebook)
        frame.config(bg=DEFAULTBACKGROUND)
        self.notebook.add(frame, text="New Tab")
        TabsPage.observers.append(frame)

    def change_primary_color(self):
        primary_color = colorchooser.askcolor()[1]
        global DEFAULTBACKGROUND
        DEFAULTBACKGROUND = primary_color
        if primary_color:
            self.config(bg=DEFAULTBACKGROUND)
            TabsPage.change_background_color()

    def change_secondary_color(self):
        secondary_color = colorchooser.askcolor()[1]
        global CUSTOMCOLOR
        CUSTOMCOLOR = secondary_color
        if secondary_color:
            self.config(bg=DEFAULTBACKGROUND)
            TabsPage.change_background_color()

class TabsPage(tk.Frame):
    observers = []

    @classmethod
    def change_background_color(cls):
        for observer in cls.observers:
            observer.update_color()

    def __init__(self, parent):
        super().__init__(parent)  # Using super for clean inheritance
        self.notebook = parent
        # Create a frame that will expand to fill the window
        self.main_frame = tk.Frame(self, bg=DEFAULTBACKGROUND)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)


        if sys.platform == 'darwin':  # macOS
            self.bind("<Command-s>", lambda event: self.save_file(event=event) )
        else:  # Windows and other platforms
            self.bind("<Control-s>", lambda event: self.save_file(event=event) )
            
        # Set up grid weights for responsive resizing
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
    
        # Variables for operations
        self.frames = self.build_AccumulatorView(self.main_frame)
        self.UVsim = UVSimulator()
        self.full_file_path = None
        self.file_path = None
        self.file_contents = []

        # Raise the AccumulatorView
        self.show_frame(AccumulatorView)

    def update_color(self):
        """ Update the GUI with the new background color """
        self.config(bg=DEFAULTBACKGROUND)
        self.main_frame.config(bg=DEFAULTBACKGROUND)
        self.frames[AccumulatorView].update_primary_color()

    def on_resize(self, event):
        # Display the current size of the window in the label
        self.label.config(text=f"Window size: {self.winfo_width()}x{self.winfo_height()}")
        # Adjust layout or other elements based on the size
        if self.winfo_width() < 400 or self.winfo_height() < 200:
            self.label.config(bg='red', fg='white')
        else:
            self.label.config(bg='black', fg='white')

    def build_AccumulatorView(self, frame: tk.Frame ):
        frame = AccumulatorView(frame, self)  # Ensure these classes are designed to accept these arguments
        frame.config(bg=DEFAULTBACKGROUND)
        frame.grid(row=0, column=0, sticky="nsew")
        return {AccumulatorView:frame}

    # update this function to not exist if you remove it we will break a lot of code
    def show_frame(self, cont):
        frame = self.frames[AccumulatorView]
        frame.tkraise()

    def get_input(self):
        # Simplified callback function for read
        print("Read callback executing inside TabsPage")
        messagebox.showinfo("Waiting for Input", "Click \"Ok\" and enter a valid BasicML word")
        self.frames[AccumulatorView].send_btn.config(state="enabled")

    def output_trigger(self, output_msg: str):
        # Callback function for output
        frame = self.frames[AccumulatorView]
        frame.update_output(self, output_msg)
        frame.tkraise()

    def update_tab_title(self, new_title):
        # Method to update the tab title
        index = self.notebook.index(self)
        self.notebook.tab(index, text=new_title)

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            self.full_file_path = file_path
            file_name = file_path.split("/")[-1]
            self.update_tab_title(file_name)
            self.file_path = file_path
            result = self.UVsim.read_file(self.file_path)
            self.file_contents = result
            self.frames[AccumulatorView].update_input(self)
            self.frames[AccumulatorView].update_table(self)
            self.show_frame(AccumulatorView)

    #Define the function
    def save_file(self):
        if self.file_contents != []:
            file_path = asksaveasfilename(initialfile = 'Untitled.txt', defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
            print(file_path)
            if file_path:
                with open(file_path, "w") as file:
                    for i in self.file_contents:
                        file.write(i+"\n")
                    messagebox.showinfo("File successfully saved", message="File saved ")
        else:
            messagebox.showinfo("Missing File", "Load a file, edit, and then save")

class AccumulatorView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        # Set up grid weights for responsive resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure([0,1], weight=1)

        # Label for IO side of accumulatorView "Input/Output"
        self.IO_label = ttk.Label(self, text="UVsimulator Group E", font=LARGEFONT)
        self.IO_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Frames for file loading and IO operations
        self.file_frame = tk.Frame(self, bg=CUSTOMCOLOR, bd=2, relief='ridge')
        self.file_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.file_frame.config(bg=CUSTOMCOLOR)

        self.io_frame = tk.Frame(self, bg=CUSTOMCOLOR, bd=2, relief='ridge')
        self.io_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        self.io_frame.config(bg=CUSTOMCOLOR)

        # Set up grid weights for responsive resizing within frames
        self.file_frame.grid_rowconfigure(0, weight=1)
        self.file_frame.grid_columnconfigure(0, weight=1)

        self.io_frame.grid_rowconfigure(0, weight=1)
        self.io_frame.grid_columnconfigure(0, weight=1)

        self.input_frame = tk.Frame(self.io_frame, bg=CUSTOMCOLOR, bd=2, relief='ridge')
        self.input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.input_frame.config(bg="gray")
        # Set up grid weights for responsive resizing
        self.input_frame.grid_rowconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.output_frame = tk.Frame(self.io_frame, bg=CUSTOMCOLOR, bd=2, relief='ridge')
        self.output_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.output_frame.config(bg="gray")
        # Set up grid weights for responsive resizing
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        # File manager inner frame on the left side
        self.left_inner_frame = tk.Frame(self.file_frame, bg=CUSTOMCOLOR)
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
            self.tree.bind("<Control-c>", lambda event: self.copy_selection(event=event, controller=controller) )

        if sys.platform == "darwin":  # Darwin indicates macOS
            self.tree.bind("<BackSpace>", lambda event: self.item_delete(event=event, controller=controller))
        else:
            self.tree.bind("<Delete>", lambda event: self.item_delete(event=event, controller=controller))

        # Labels for file loading section
        self.file_frame_label = ttk.Label(self.left_inner_frame, text="File Editor/Manager", font=LARGEFONT)
        self.file_frame_label.grid(row=0, column=0, padx=10, pady=10, sticky="new")

        # Label to display selected file name
        self.file_name_label = ttk.Label(self.left_inner_frame, text="File Name: No File selected", font=SMALLFONT, justify="center")
        self.file_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        # Editor entry widget
        self.editor_entry = tk.Text(self.table_frame)
        self.editor_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Button for saving file
        self.save_file = ttk.Button(self.table_frame, text="Save File", command=lambda: controller.save_file())
        self.save_file.grid(row = 3, column=1, padx=10, pady=10, sticky="new", rowspan=2)

        # Button to select and run the loaded file
        self.run_button = ttk.Button(self.left_inner_frame, text="Run File", command=lambda: self.run_file(controller))
        self.run_button.grid(row=4, column=0, padx=10, pady=10, sticky="new")

        # Button to submit changed value
        self.editor_btn = ttk.Button(self.left_inner_frame, text="Submit Changes", command=lambda: self.updateTreeView(controller))
        self.editor_btn.grid(row=3, column=0, padx=10, pady=10, sticky="new")

        # Button to submit changed value
        self.editor_btn = ttk.Button(self.left_inner_frame, text="Edit File", command=lambda: self.edit_file())
        self.editor_btn.grid(row=3, column=1, padx=10, pady=10, sticky="new")

        # Button to select and run the loaded file
        self.new_file_btn = ttk.Button(self.left_inner_frame, text="Load", command=lambda: controller.load_file())
        self.new_file_btn.grid(row=4, column=1, padx=10, pady=10, sticky="new")

        # Labels and widgets for IO operations section
        self.IO_label = ttk.Label(self.input_frame, text="Input", font=LARGEFONT, background="gray")
        self.IO_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.input_entry = ttk.Entry(self.input_frame)
        self.input_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.send_btn= ttk.Button(self.input_frame, text="Resume Execution", command=lambda: self.send_input(controller))
        self.send_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.send_btn.config(state="disabled") 

        self.output_label = ttk.Label(self.output_frame, text="Output", font=LARGEFONT, justify="center")
        self.output_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.output_text = ttk.Label(self.output_frame, text="", font=SMALLFONT, wraplength=500)
        self.output_text.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Bind the <Return> key event to the run_file function
        self.input_entry.bind("<Return>", lambda event: self.send_input(controller, event))

    def update_primary_color(self):
        self.config(bg=DEFAULTBACKGROUND)
        print(DEFAULTBACKGROUND)
        self.input_frame.config(bg=CUSTOMCOLOR)
        self.output_frame.config(bg=CUSTOMCOLOR)
        self.left_inner_frame.config(bg=CUSTOMCOLOR)
        self.table_frame.config(bg=CUSTOMCOLOR)
        self.file_frame.config(bg=CUSTOMCOLOR)
        self.io_frame.config(bg=CUSTOMCOLOR)


    # def on_resize(self, event):
    #     # Display the current size of the window in the label
    #     label.config(text=f"Window size: {event.width}x{event.height}")
    #     # Adjust layout or other elements based on the size
    #     if event.width < 400 or event.height < 200:
    #         label.config(bg='red', fg='white')
    #     else:
    #         label.config(bg='green', fg='black')

    def updateTreeView(self, controller:tkinterApp):
        if self.fileContents(controller=controller) or self.editor_entry.get("1.0", tk.END).strip() != "":
            newValues = self.editor_entry.get("1.0", tk.END)
            response = messagebox.askyesno("Confirm Overwrite", "Are you sure you want to overwrite the file?")
            if response:
                print("User chose to overwrite the file.")
                # split values on new line char
                splitValues = newValues.split()
                controller.file_contents = splitValues
                self.update_table(controller)
                self.editor_entry.delete("1.0", tk.END)
            else:
                print("User canceled the overwrite.")
        else:
            messagebox.showinfo("File contents Empty", "Click the \"Load\" button to load a file OR enter custome BasicML.")

    def edit_file(self):
        tree_items = []
        for idx, item in enumerate(self.tree.get_children()):
            cleanItem = self.tree.item(item)["values"]
            # print(cleanItem)
            if cleanItem[0] == 0:
                tree_items.append("+0000")
            elif len(str(cleanItem[0])) < 4:
                length = len(str(cleanItem[0]))
                diff = 4 - length
                newWord =   "+" + (diff * "0") + str(cleanItem[0])
                tree_items.append(newWord)
            else:
                tree_items.append(f"+{cleanItem[0]}")
            tree_items.append("\n")

        tree_string = "".join(tree_items)
        self.editor_entry.insert(tk.END, tree_string)

        # self.editor_entry.config(text=tree_items)
        self.editor_entry.bind('<Escape>', lambda event: self.cancel_editing(event))
        # self.editor_entry.bind('<FocusOut>', lambda event: self.on_focus_out(event))  # Save changes on focus out

    def cancel_editing(self, event):
        self.editor_entry.delete("1.0", tk.END)

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
                        self.tree.clipboard_append('+' + str(value)+ "\n")
                    else:
                        self.tree.clipboard_append('-' + str(value)+ "\n")
                else:
                    self.tree.clipboard_append("+0000")
            except:
                pass
            # print(each)
        print(self.tree.clipboard_get())

    def run_file(self, controller: tkinterApp, event=None):
        if self.fileContents(controller=controller):
            self.output_text.config(text="")
            self.get_table_data(controller=controller)
            result = controller.UVsim.load_program(controller.file_contents)
            controller.UVsim.run_program(read_callback=controller.get_input, write_callback=controller.output_trigger)
        else:
            messagebox.showinfo("File contents Empty", "Click the \"Load\" button to load a file OR enter custome BasicML.")

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

    def send_input(self, controller:TabsPage):
        print("sending input")
        input = self.input_entry.get()
        print(f"input: {input}")
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

    def fileContents(self, controller) -> bool:
        # checks if the file contents is Empty
        if len(controller.file_contents) == 0:
            controller.file_path = None
            return False
        return True