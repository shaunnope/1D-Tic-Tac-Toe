from copy import deepcopy

import tkinter as tk
import tkinter.messagebox
from functools import partial
import sys

class Game(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.window = tk.Tk()
        self.window.title('1D Tic Tac Toe')
        self.window.geometry('500x300+500+100')
        pass

# (cross: _ wins, circle: _ wins)
# (no. of wins == 3) == winner
class Cube:
    def __init__(self, root = None, num_boards = 6):
        self.root = root
        self.turn_num = 0
        self.wins = {1: 0 , 2: 0} # 1: circle, 2: cross

        self.corner = (200,80)
        self.side = 60

        self.boards = []
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

    def display_cube(self):
        for board in self.boards:
            board.display_board()

    # update the attributes of the cube after each move
    def update_cube(self):
        # how many boards are filled
        num_filled=0
        for key in self.wins.keys():
            self.wins[key] = sum([board.wins[key] for board in self.boards])
        
        for board in self.boards:
            if board.filled==True:
                num_filled+=1
        if num_filled==6:
            winner = "It's a tie!"
            if self.wins[1] != self.wins[2]:
                winner = 'O'*(self.wins[1] > self.wins[2]) + 'X'*(self.wins[2] > self.wins[1]) + ' wins!'
            message = f"Score\n O:   {self.wins[1]}  X:   {self.wins[2]}"
            is_restart = tkinter.messagebox.askyesno(title='Game Over', message= winner+'\n\n'+message + '\nRestart?')
            if is_restart:
                self.root.destroy()
                start()


    def turn_cube(self, board, move):
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
        #check whether the board wins or not
        self.board_win=False
        #check whether all the cells are filled
        self.filled=False
        self.step=0
        self.buttons = [[None, None, None], [None, None, None], [None, None, None]]
        self.display_board()

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
        is_valid = (x < 3 and y < 3) &(~self.board_win)
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
        # get current turn number from global scope
        turn_num = self.parent.turn_num
        i,j = coords

        # Check if we have valid coordinates
        is_valid = self.coordinates_valid(coords)

        # If valid coordinates, update the board
        if (is_valid):
            self.step+=1
            self.board[i][j] = 2 - (turn_num%2)
            self.buttons[i][j]['text'] = 'O'*(self.board[i][j] == 1) + 'X'*(self.board[i][j] == 2)
            self.parent.turn_num += 1
            self.checkwin(coords)
            self.checkfilled()
            self.count_wins()
            self.parent.update_cube()
        else:
            tkinter.messagebox.showinfo(title='Invalid cell',message='Please choose a valid cell')

    def checkfilled(self):
        if self.step==9:
            self.filled=True

    
    def checkwin(self,coords):
        # print(1)
        x=coords[0]
        y=coords[1]
        win=0
        if self.buttons[x%3][y]['text']==self.buttons[(x+1)%3][y]['text']==self.buttons[(x+2)%3][y]['text']:
            self.board_win=True
            self.filled=True
        elif self.buttons[x][y%3]['text']==self.buttons[x][(y+1)%3]['text']==self.buttons[x][(y+2)%3]['text']:
            self.board_win=True
            self.filled = True
        if x%2==0 and y%2==0:
            if self.buttons[x][y]['text']==self.buttons[1][1]['text']==self.buttons[2-x][2-y]['text']:
                self.board_win = True
                self.filled = True
        if self.board_win==True:
            if self.buttons[x][y]['text']=='O':
                win=1
                self.board_win = True
                self.filled = True
            else:
                win=2
                self.board_win = True
                self.filled = True
            #circle wins highlight the board with blue color, X wins highlight the board with red color
            if win==1:
                color='#00ffff'
            elif win==2:
                color='#ff8080'
            for x in range(3):
                for y in range(3):
                    self.buttons[x][y]['bg'] = color
            self.wins[win]+=1

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
    game = Cube(root,1)
    #game.display_cube()
    root.mainloop()

start()