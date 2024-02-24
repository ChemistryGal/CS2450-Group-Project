# uvSim: Virtual Machine for Interpreting BasicML

## Introduction

Hello and welcome to uvSim! uvSim is a virtual machine designed for interpreting BasicML.

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

   NOTE: As a team we ran into issues with reading from our GUI application. This is one requirement that is taking longer than expected to deliver. The rest of the app depends on this input functionality. Since we didn't get this figured out in time we wanted to still have something working. The current version will allow you to run the file through the GUI but the input must be done through the command line. A prompt will appear in the console for input. We hope as our customer you will have patience with us as we resolve this issue.

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

