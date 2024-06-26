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
4. You will select a file by clicking the "Load" button
5. You can make edits to your file using the "Edit File" button. You can make your chanes then click the "Submit Changes" button.

   NOTE:

   - All input values must have "+" before the chosen value
   - The application continues to support old four-digit word files but does not allow mixing of four and six-digit words within a single file.
   - The application will convert any four-digit word files to six-digit words before reading them into memory.
   - The application now supports data files containing up to 250 lines.

6. You can also save the new updated file with the "Save File" button.
7. You can then execute your file by clicking the run file.
8. If your file needs to take input the program will stop and a window will prompt you to enter your input. Click ok then enter your input into
   the box above the resume execution button. Once you out in your input click resume execution.
9. The output will then display inthe box labeled output.
10. You can then Load a new file with the "Load" button and continue to execute.
11. You can also run multiple tabs at once with "Add Tab" button.

## Addtional Functionalities

There is an options menu in the top left that will allow you to change the background color and the box colors. You can also exit the app through the options
menu. Below is a video showing how everything works!

You can also use the command or control keys to copy and paste items to the editor. If you would like to copy multiple values just hold down the control or command key and select each of the values you'd like to copy. The same works for deleting values.

## Video

[<img src="https://i9.ytimg.com/vi/CktHo5eETc4/mq1.jpg?sqp=CLjD6LAG&rs=AOn4CLDr35kYmbdD7w8IBKmx72RI0TK2eA&retry=2" width="50%">](https://youtu.be/CktHo5eETc4 "Test Video")

## Example Input File

Here's a small example of what your input file should look like. Ensure that your file includes a halt instruction (4300).

```assembly
+010007
+010008
+020007
+020008
+021009
+011009
+043000
+000000
+000000
+000000
```
