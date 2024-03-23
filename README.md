# uvSim: Virtual Machine for Interpreting BasicML

## Introduction

Hello and welcome to uvSim! uvSim is a virtual machine designed for interpreting BasicML. Our app contains a options Menu in the top left, and 
in this menu you can customer the colors used in this application. You can also select a new file as well, and you can also exit the app and through
this menu as well.

## Getting Started

To run this program, follow these simple steps:

1. Open a terminal.
2. Type the following command:

    ```bash
    python main.py
    ```

3. The system will open a GUI
4. You will select a file
5. Upon selecting a file you will see a screen that has a button to run the file. Click on "Run File".
6. There will be a spot for input and when you type it in you can clcik resume execution to submit the input.
7. There is also a button to run another file if you choose or you can close the application.

## Example Input File

Here's a small example of what your input file should look like. Ensure that your file includes a halt instruction (4300).

```assembly
+1007
+1008
+2007
+2008
+2109
+1109
+4300
+0000
+0000
+0000
```

