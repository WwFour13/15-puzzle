import tkinter as tk
from board import Board

WIDTH=4
HEIGHT=4

board = Board(WIDTH, HEIGHT)

def play_in_console():

    while True:
        board.print_to_console()
        print("Current opening:", board.get_current_openning())
        print("Available moves:", [f"({m.from_}, {m.to})" for m in board.get_available_moves()])
        move = input("Enter your move (up, down, left, right): ").strip().lower()
        if move == "up":
            board.up()
        elif move == "down":
            board.down()
        elif move == "left":
            board.left()
        elif move == "right":
            board.right()
        else:
            print("Invalid move. Please enter up, down, left, or right.")

def play_in_tkinter():
    # 1. Create the main application window
    root = tk.Tk()
    root.title("My First GUI")

    SCREEN_HEIGHT = 480
    SCREEN_WIDTH = (SCREEN_HEIGHT * 16) // 9
    root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

    def handle_keypress(event):
        key = event.keysym
        if key == "Up":
            board.up()
        elif key == "Down":
            board.down()
        elif key == "Left":
            board.left()
        elif key == "Right":
            board.right()
        if key == "w":
            board.up()
        elif key == "s":
            board.down()
        elif key == "a":
            board.left()
        elif key == "d":
            board.right()
        board.print_to_tkinter(root, screen_width=SCREEN_WIDTH, screen_hight=SCREEN_HEIGHT)
    
    root.bind("<Key>", handle_keypress)
    root.focus_set()

    board.print_to_tkinter(root, screen_width=SCREEN_WIDTH, screen_hight=SCREEN_HEIGHT)

    root.mainloop()


if __name__ == "__main__":
    play_in_tkinter()
