from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import sys

class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.configure(background='light yellow')

        self.style = Style()
        self.style.configure('TButton', font=('Arial', 20))

        self.board = [[0 for _ in range(9)] for _ in range(9)]

        self.create_board()
        self.create_buttons()

    def create_board(self):
        self.entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                frame = Frame(self.root, borderwidth=1, relief="solid")
                frame.grid(row=i, column=j, padx=self.calculate_padx(j), pady=self.calculate_pady(i))
                entry = Entry(frame, width=2, font=('Arial', 30), justify='center')
                entry.pack()
                entry.bind("<KeyRelease>", self.validate_entry)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def calculate_padx(self, j):
        if j == 0:
            return (8, 0)
        elif (j + 1) % 3 == 0:
            return (0, 8)
        else:
            return (2, 2)

    def calculate_pady(self, i):
        if i == 0:
            return (8, 0)
        elif (i + 1) % 3 == 0:
            return (0, 8)
        else:
            return (2, 2)

    def create_buttons(self):
        self.create_button("Solve", self.solve_sudoku, 9)
        self.create_button("Reset", self.clear_entries, 10)

    def create_button(self, text, command, row):
        button = Button(self.root, text=text, command=command, width=10, style='TButton')
        button.grid(row=row, columnspan=9, pady=5)

    def validate_entry(self, event):
        widget = event.widget
        value = widget.get()
        if not value.isdigit() or not (1 <= int(value) <= 9):
            widget.delete(0, END)
            return

        row, col = None, None
        for i in range(9):
            for j in range(9):
                if self.entries[i][j] == widget:
                    row, col = i, j
                    break

        self.board[row][col] = int(value)
        if self.is_duplicate(row, col):
            messagebox.showwarning("Invalid Input", "This number is already present in the row, column, or 3x3 box. Please enter a different number.")
            widget.delete(0, END)
            self.board[row][col] = 0

    def is_duplicate(self, row, col):
        value = self.board[row][col]

        # Check row and column
        for i in range(9):
            if i != col and self.board[row][i] == value:
                return True
            if i != row and self.board[i][col] == value:
                return True

        # Check 3x3 box
        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_start_row, box_start_row + 3):
            for j in range(box_start_col, box_start_col + 3):
                if (i != row or j != col) and self.board[i][j] == value:
                    return True

        return False

    def solve_sudoku(self):
        self.read_entries()
        gameboard = Board(self.board)
        if gameboard.solver():
            self.update_board(gameboard.board)
        else:
            messagebox.showerror("Error", "The provided puzzle is unsolvable. The program will now exit.")
            self.root.quit()
            sys.exit()

    def read_entries(self):
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                self.board[i][j] = int(value) if value.isdigit() else 0

    def clear_entries(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, END)

    def update_board(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, END)
                self.entries[i][j].insert(0, str(board[i][j]))

class Board:
    def __init__(self, board):
        self.board = board

    def solver(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(num, row, col):
                self.board[row][col] = num
                if self.solver():
                    return True
                self.board[row][col] = 0
        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, num, row, col):
        # Check the row
        if num in self.board[row]:
            return False

        # Check the column
        if num in [self.board[i][col] for i in range(9)]:
            return False

        # Check the 3x3 box
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num:
                    return False
        return True

if __name__ == "__main__":
    root = Tk()
    SudokuSolverGUI(root)
    root.mainloop()
