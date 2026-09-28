import random
import tkinter as tk
from move import Move
from coloring import interpolate

class Board:

    TKKINTER_LOW_COLOR = "#f0f0f0"
    TKKINTER_HIGH_COLOR = "#df9809"

    def __init__(self, width, hight, start_from_end=False):

        assert width > 0 and hight > 0, "Width and height must be positive"
        assert isinstance(width, int) and isinstance(hight, int), "Width and height must be integers"

        self.__width = width
        self.__hight = hight
        self.__total_length = width * hight

        self.__board = None

        self.__current_openning = None

        self.__available_moves = {
            "up": None,
            "down": None,
            "left": None,
            "right": None
        }

        self.__set_random_board_values(width, hight, start_from_end)
        self.__find_opening()
        self.__update_available_moves()

    def __find_opening(self):
        for row in range(self.__hight):
            for col in range(self.__width):
                if self.__board[row][col] == 0:
                    self.__current_openning = (row, col)
                    break
        assert self.__current_openning is not None, "Couldn't find the current_opening"

    def __set_random_board_values(self, width, hight, start_from_end):
        flat_board = [i+1 for i in range(self.__width * self.__hight - 1)]+[0]

        if start_from_end:
            end = flat_board[width*(hight-2):]
            random.shuffle(end)
            flat_board = flat_board[:width*(hight-2)]+end
        else:
            random.shuffle(flat_board)
            
        self.__board = [flat_board[i:i+width] for i in range(0, self.__total_length, width)]

    def __update_available_moves(self):
        row, col = self.__current_openning
        self.__available_moves["down"] = Move((row, col), (row - 1, col)) if row > 0 else None
        self.__available_moves["up"] = Move((row, col), (row + 1, col)) if row < self.__hight - 1 else None
        self.__available_moves["right"] = Move((row, col), (row, col - 1)) if col > 0 else None
        self.__available_moves["left"] = Move((row, col), (row, col + 1)) if col < self.__width - 1 else None 

    def shuffle_board(self):
        self.__init__(self.__width, self.__hight, start_from_end=False)
        self.print_to_tkinter(self.__root_save, self.__screen_width_save, self.__screen_hight_save)

    def play_end(self):
        self.__init__(self.__width, self.__hight, start_from_end=True)
        self.print_to_tkinter(self.__root_save, self.__screen_width_save, self.__screen_hight_save)

    def get_current_openning(self):
        return self.__current_openning

    def get_available_moves(self):
        ret = []
        for _, move in self.__available_moves.items():
            if move is not None:
                ret.append(move)
        return ret

    def make_move(self, move: Move):
        from_row, from_col = move.from_
        to_row, to_col = move.to

        if self.__board[from_row][from_col] != 0:
            raise ValueError("Cannot move a tile that is not in the current opening")
        if not (0 <= to_row <self.__hight and 0 <= to_col <self.__width):
            raise ValueError("Move is out of bounds") 

        self.__board[from_row][from_col] = self.__board[to_row][to_col]
        self.__board[to_row][to_col] = 0
        self.__current_openning = (to_row, to_col)
        self.__update_available_moves()

    def print_to_console(self):
        for row in self.__board:
            for tile in row:
                print(f"{tile:2}", end=" ")
            print()

    def print_to_tkinter(self, root, screen_width, screen_hight):

        # Store the root window and screen dimensions for later use in rendering the board.
        self.__root_save = root
        self.__screen_width_save = screen_width
        self.__screen_hight_save = screen_hight

        cell_width = screen_width // (30 * len(self.__board[0]))
        cell_height = screen_hight // (36 * len(self.__board))

        grid_frame = tk.Frame(root)
        grid_frame.place(relx=0, rely=0)
        
        for r in range(self.__hight):
            for c in range(self.__width):
                value = self.__board[r][c]
                cell = tk.Label(grid_frame,
                                text=value if value != 0 else "",
                                background=interpolate(self.TKKINTER_LOW_COLOR, 
                                                       self.TKKINTER_HIGH_COLOR, 
                                                       self.__total_length, 
                                                       value),
                                borderwidth=1, 
                                relief="solid", 
                                height=cell_height, 
                                width=cell_width)
                cell.grid(row=r, column=c, padx=1, pady=1)

        reset_button = tk.Button(root, text="Reset", command=self.shuffle_board)
        grid_frame.update_idletasks()
        reset_button.place(x=grid_frame.winfo_width(), rely=0.0)
        play_end_button = tk.Button(root, text="Play End", command=self.play_end)
        reset_button.update_idletasks()
        play_end_button.place(x=grid_frame.winfo_width(), y=reset_button.winfo_height())

    def down(self):
        if self.__available_moves["down"] is not None:
            self.make_move(self.__available_moves["down"])

    def up(self):
        if self.__available_moves["up"] is not None:
            self.make_move(self.__available_moves["up"])

    def left(self):
        if self.__available_moves["left"] is not None:
            self.make_move(self.__available_moves["left"])

    def right(self):
        if self.__available_moves["right"] is not None:
            self.make_move(self.__available_moves["right"])