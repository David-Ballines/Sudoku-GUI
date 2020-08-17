# Sudoku-GUI

This is a playable Sudoku game using the pygame library to create a GUI. The backtracking algorithm is used to solve the puzzle.

## Getting Started

To start to play you can open the file through a Python IDE, you can also run the program through the console using the following command line inside the folder.
```bash
python Sudoku_gui.py
```

Onece game has started, you can click on the boxes, they will hilight, and press any number key to insert the number inside the box. If the number is correct it will be colored blue and when it is incorrect it will be red.

There are three buttons that help the user solve the given puzzle, hint, restart, and solve buttons. To use the hint button, select a box and then click the hint button. The button will reveal the correct answer to the sellected box. The restart button will clear all of the number placed. The solve button will instantly solve the selected puzzle.

You can change what puzzle you are doing by eiditing the BOARDS variable in the Python file.

### Prerequisites

Need the Python library, pygame. To download pygame go to the console and type the command
```bash
py -m pip install -U pygame --user
```
more information about pygame can be found following this website https://www.pygame.org/wiki/GettingStarted


### Installing

Download the Python file into the desired folder.
