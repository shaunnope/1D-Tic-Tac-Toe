from copy import deepcopy

import tkinter as tk
import tkinter.messagebox
from functools import partial

class Game(tk.Frame):
    def __init__(self, num_boards = 6, master=None):
        super().__init__(master)
        self.master = master

        self.num_boards = num_boards
        
        #self.window = tk.Tk()
        self.restart()
    
    def restart(self):
        #self.window.destroy()
        self.window = tk.Tk()
        self.window.title('1D Tic Tac Toe')
        self.window.geometry('500x300+500+100')

        self.cube = Cube(self, self.num_boards)

        self.window.mainloop()

        
# (cross: _ wins, circle: _ wins)
class Cube:
    def __init__(self, root = None, num_boards = 6):
        self.root = root

        # display parameters
        self.corner = (200,80)
        self.side = 60
        self.font = ('Bauhaus 93 Regular',20)

        # score tracking
        self.turn_num = 0
        self.wins = {1: 0 , 2: 0} # 1: circle, 2: cross
        self.init_scoreboard()

        self.boards = []
        self.init_cube(num_boards)
        
        self.display_cube()
    
    def init_cube(self, num_boards):
        if num_boards == 6:
            # init cube projection of boards
            x,y = self.corner
            w = self.side*3
            corners = [(x+w,y), (x,y+w), (x+w,y+w), (x+2*w,y+w), (x+3*w,y+w), (x+w,y+2*w)]
            for i in range(num_boards):
                self.boards.append(Board(self, self.root, corners[i]))
        else:
            # if not default number of boards, display boards as a row
            for i in range(num_boards):
                corner = (self.corner[0] + i*self.side*3, self.corner[1])
                self.boards.append(Board(self, self.root, corner))

    def init_scoreboard(self):
        self.label=tk.Label(text=f"O wins: {self.wins[1]}\nX wins: {self.wins[2]}",bg='#00ffff',
                            font=self.font)
        self.label.place(x=800,y=80)

    def update_scoreboard(self):
        self.label['text'] = f"O wins: {self.wins[1]}\nX wins: {self.wins[2]}"

    def display_cube(self):
        for board in self.boards:
            board.display_board()

    # update the attributes of the cube after each move
    def update_cube(self):
        # store previous wins
        old_wins = deepcopy(self.wins)
        # count current wins
        for key in self.wins.keys():
            self.wins[key] = sum([board.wins[key] for board in self.boards])
        
        # if all cells are filled, end the game
        if self.turn_num >= len(self.boards)*9:
            winner = "It's a tie!"
            if self.wins[1] != self.wins[2]: 
                winner = 'O'*(self.wins[1] > self.wins[2]) + 'X'*(self.wins[2] > self.wins[1]) + ' wins!'
            message = f"Score\n O:   {self.wins[1]}  X:   {self.wins[2]}"
            is_restart = tkinter.messagebox.askyesno(title='Game Over', 
                                                    message= winner+'\n\n'+message + '\nRestart?')
            if is_restart:
                self.root.destroy()
                #self.root.restart()
                start()
            else:
                tkinter.messagebox.showinfo(title='Good Game!',message='Thanks for playing!')
                self.root.destroy()
        # else, check if total num of wins for a player increases
        elif self.wins[1] > old_wins[1] or self.wins[2] > old_wins[2]:
            # check who is turning cube
            turner = (self.wins[1] > old_wins[1]) + (self.wins[2] > old_wins[2])
            priority = 2 - ((self.turn_num-1)%2)
            # prompt to turn cube
            self.turn_cube()
            pass
    def turn_cube(self):
        # display turn buttons over current board
        # prompt turn
        pass

class Board(Cube):
    # init empty board and board score
    def __init__(self, parent=None, root=None, corner = (380,80)):
        if parent is None:
            super().__init__(root)
        self.parent = parent
        self.root = root
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.wins = {1: 0, 2: 0} # 1: circle, 2: cross
        self.side = 60
        self.corner = corner

        self.buttons = [[None, None, None], [None, None, None], [None, None, None]]

    # displays the board of buttons
    def display_board(self):
        x,y = self.corner
        for i in range(3):
            for j in range(3):
                symb = 'O'*(self.board[i][j] == 1) + 'X'*(self.board[i][j] == 2)
                self.buttons[i][j] = tk.Button(self.root, text = symb, command=partial(self.update_board,(i,j)))
                self.buttons[i][j].place(x= x + i * self.side, y= y + j * self.side, width=self.side, height=self.side)

    # returns True if coords provided is empty cell
    # False otherwise
    def coordinates_valid(self, coords = (0,0)):
        x, y = coords

        # Check if coordinates are within range
        is_valid = (x < 3 and y < 3)
        # Check if cell is empty
        if (is_valid):
            is_valid = (self.board[x][y] == 0)

        # If coordinates are invalid, let the user know
        if (not is_valid):
            error_message = f"Coordinates for given action are invalid! You passed {coords}."
            print(error_message)

        # Return the boolean is_valid
        return is_valid

    # attempt to update board with given move
    # if valid move, update board and inc turn_num
    # if invalid, display error window
    def update_board(self, coords = (0,0)):
        # get current turn number from parent
        turn_num = self.parent.turn_num
        i,j = coords

        # Check if we have valid coordinates
        is_valid = self.coordinates_valid(coords)

        # If valid coordinates, update the board
        if (is_valid):
            self.board[i][j] = 2 - (turn_num%2)
            self.buttons[i][j]['text'] = 'O'*(self.board[i][j] == 1) + 'X'*(self.board[i][j] == 2)
            
            old_wins = deepcopy(self.wins)
            self.count_wins()
            if self.wins != old_wins:
                self.parent.turn_cube()
            
            self.parent.turn_num += 1
            self.parent.update_cube()
        else:
            tkinter.messagebox.showinfo(title='Invalid cell',message='Please choose a valid cell')

    # count the number of wins on the board
    def count_wins(self):
        wins = {1: 0, 2: 0} # 1: circle, 2: cross
        # Check rows and cols
        for i in range(3):
            row = self.board[i][0] * self.board[i][1] * self.board[i][2]
            col = self.board[0][i] * self.board[1][i] * self.board[2][i]
            if row in (1,8):
                wins[int(row**(1/3))] += 1
            if col in (1,8):
                wins[int(col**(1/3))] += 1

        # Check diagonals
        diag1 = self.board[0][0] * self.board[1][1] * self.board[2][2]
        diag2 = self.board[0][2] * self.board[1][1] * self.board[2][0]
        if diag1 in (1,8):
            wins[int(diag1**(1/3))] += 1
        if diag2 in (1,8):
            wins[int(diag2**(1/3))] += 1

        self.wins = wins
        return wins

def start():
    root = tk.Tk()
    root.title('1D Tic Tac Toe')
    root.geometry('1600x800+-10+0')
    game = Cube(root)
    root.mainloop()

start()
#game = Game(1)
#a = Cube(None, 1)