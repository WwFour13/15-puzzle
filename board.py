"""
Sizing & Layout Alignment
• width: Defines the horizontal size. Note: Represented in character widths for text labels, but screen units (pixels) for image labels.
• height: Defines the vertical size. Note: Represented in lines of text for text labels, but screen units (pixels) for image labels.

"""



import random
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from move import Move
from coloring import interpolate

class Board:

    TKKINTER_LOW_COLOR = "#f0f0f0"
    TKKINTER_HIGH_COLOR = "#df9809"

    PADX = 1
    PADY = 1
    BORDER_WIDTH = 1

    def __init__(self, cols, rows, start_from_end=False):

        assert cols > 0 and rows > 0, "rows and cols must be positive"
        assert isinstance(cols, int) and isinstance(rows, int), "rows and cols must be integers"

        self.__cols = cols
        self.__rows = rows
        self.__total_length = cols * rows

        self.__board = None

        self.__current_openning = None

        self.__available_moves = {
            "up": None,
            "down": None,
            "left": None,
            "right": None
        }

        self.__set_random_board_values(cols, rows, start_from_end)
        self.__find_opening()
        self.__update_available_moves()

    def __find_opening(self):
        for row in range(self.__rows):
            for col in range(self.__cols):
                if self.__board[row][col] == 0:
                    self.__current_openning = (row, col)
                    break
        assert self.__current_openning is not None, "Couldn't find the current_opening"

    def __set_random_board_values(self, cols, rows, start_from_end):
        flat_board = [i+1 for i in range(self.__cols * self.__rows - 1)]+[0]

        if start_from_end:
            end = flat_board[cols*(rows-2):]
            random.shuffle(end)
            flat_board = flat_board[:cols*(rows-2)]+end
        else:
            random.shuffle(flat_board)
            
        self.__board = [flat_board[i:i+cols] for i in range(0, self.__total_length, cols)]

    def __update_available_moves(self):
        row, col = self.__current_openning
        self.__available_moves["down"] = Move((row, col), (row - 1, col)) if row > 0 else None
        self.__available_moves["up"] = Move((row, col), (row + 1, col)) if row < self.__rows - 1 else None
        self.__available_moves["right"] = Move((row, col), (row, col - 1)) if col > 0 else None
        self.__available_moves["left"] = Move((row, col), (row, col + 1)) if col < self.__cols - 1 else None 

    def shuffle_board(self):
        self.__init__(self.__cols, self.__rows, start_from_end=False)
        self.print_to_tkinter(self.__root_save, self.__width_save, self.__hight_save)

    def play_end(self):
        self.__init__(self.__cols, self.__rows, start_from_end=True)
        self.print_to_tkinter(self.__root_save, self.__width_save, self.__hight_save)

    def get_current_openning(self):
        return self.__current_openning

    def get_available_moves(self):
        ret = []
        for _, move in self.__available_moves.items():
            if move is not None:
                ret.append(move)
        return ret

    def get_total_pixel_width(self):
        return self.__width_save

    def get_total_pixel_height(self):
        return self.__hight_save

    """
the cells change size based off text length (2 dugut vs 1 digit. make board method __get_image(text, color, width, height)
makes the image so that tk.Label takes image not text
    """

    def __create_image(self, value, color, width, height):
        text = str(value) if value != 0 else ""
        width = max(1, int(width))
        height = max(1, int(height))
        img = Image.new("RGB", (width, height), color=color)
        if text and str(text) != "0":
            draw = ImageDraw.Draw(img)
            font_size = max(8, int(min(width, height) * 0.4))
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except Exception:
                try:
                    font = ImageFont.load_default(size=font_size)
                except TypeError:
                    font = ImageFont.load_default()
            draw.text((width / 2, height / 2), str(text), fill="black", anchor="mm", font=font)
        return ImageTk.PhotoImage(img)

    def make_move(self, move: Move):
        from_row, from_col = move.from_
        to_row, to_col = move.to

        if self.__board[from_row][from_col] != 0:
            raise ValueError("Cannot move a tile that is not in the current opening")
        if not (0 <= to_row <self.__rows and 0 <= to_col <self.__cols):
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

    def print_to_tkinter(self, root, board_width, board_hight):

        # Store the root window and screen dimensions for later use in rendering the board.
        self.__root_save = root
        self.__width_save = board_width
        self.__hight_save = board_hight

        cell_width = board_width // self.__cols
        cell_height = board_hight // self.__rows

        if not hasattr(self, "__images") or self.__images is None:
            self.__images = {i: self.__create_image(
                i, 
                interpolate(self.TKKINTER_LOW_COLOR, 
                            self.TKKINTER_HIGH_COLOR, 
                            self.__total_length, 
                            i), 
                cell_width, 
                cell_height) 
                for i in range(0, self.__total_length)
            }

        grid_frame = tk.Frame(root)
        grid_frame.place(relx=0, rely=0)

        self.__cell_images = []
        for r in range(self.__rows):
            for c in range(self.__cols):
                value = self.__board[r][c]
                img = self.__images[value]
                self.__cell_images.append(img)
                cell = tk.Label(grid_frame,
                                image=img,
                                borderwidth=0, 
                                relief="solid")
                cell.grid(row=r, column=c)


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