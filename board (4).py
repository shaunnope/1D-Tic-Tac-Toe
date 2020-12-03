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
        self.font = ('Bauhaus 93 Regular',20)
        self.padding = 0.1
        self.corner = (1000,380)
        self.side = 15
        self.play_corner = (380,120)
        self.play_side = 100

        # score tracking
        self.turn_num = 0
        self.wins = {1: 0 , 2: 0} # 1: circle, 2: cross
        self.init_scoreboard()

        self.boards = []
        self.init_cube(num_boards)
        self.playfield = Board(self, self.root, self.play_corner, self.play_side)
        self.playfield.board = self.boards[2].board
        
        self.init_controls()
        
        self.display_cube()
        self.debug = tk.Button(self.root, text = 'Debug', command=self.debug_func)
        self.debug.place(x= 20, y= 20, width=50, height=20)

    def debug_func(self):
        self.toggle_controls()

    def init_scoreboard(self):
        self.label=tk.Label(text=f"O wins: {self.wins[1]}\nX wins: {self.wins[2]}",bg='#00ffff',
                            font=self.font)
        self.label.place(x=800,y=80)
    def update_scoreboard(self):
        self.label['text'] = f"O wins: {self.wins[1]}\nX wins: {self.wins[2]}"
  
    def init_cube(self, num_boards):
        if num_boards == 6:
            # init cube projection of boards
            p = int(2*self.padding*self.side)
            x,y = self.corner
            w = self.side*3+p
            corners = [(x+w,y), (x,y+w), (x+w,y+w), (x+2*w,y+w), (x+3*w,y+w), (x+w,y+2*w)]
            for i in range(num_boards):
                self.boards.append(Board(self, self.root, corners[i], self.side))
        else:
            # if not default number of boards, display boards as a row
            for i in range(num_boards):
                corner = (self.corner[0] + i*self.side*3, self.corner[1])
                self.boards.append(Board(self, self.root, corner, self.side))

    def init_controls(self):
        # init list of control buttons [up(3), down(3,3), left(3), right(3,3)]
        self.controls = [[None,None,None],[None,None,None],[None,None,None],[None,None,None],[None,None,None],[None,None,None]]
        
        # Coordinates, details of buttons
        p = int(2.5*self.padding*self.play_side)
        x,y = self.play_corner
        w,h = self.play_side,self.play_side/3
        corners = [[(x+p,y-h-p),(x+p+w,y-h-p),(x+p+2*w,y-h-p)],
                    [(x+p,y+3*w+p),(x+p+w,y+3*w+p),(x+p+2*w,y+3*w+p)],
                    [(x+p,y+3*w+h+p),(x+p+w,y+3*w+h+p),(x+p+2*w,y+3*w+h+p)],
                    [(x-h-p,y+p),(x-h-p,y+p+w),(x-h-p,y+p+2*w)],
                    [(x+3*w+p,y+p),(x+3*w+p,y+p+w),(x+3*w+p,y+p+2*w)],
                    [(x+3*w+h+p,y+p),(x+3*w+h+p,y+p+w),(x+3*w+h+p,y+p+2*w)]]
        dim = [(w-2*p,h),(h,w-2*p)]
        symbs = ['^','v','w','<','>','>>']
        
        # init callback methods
        self.controls_commands = [partial(self.rotate_up,1),partial(self.rotate_up,-1),partial(self.rotate_up,2),partial(self.rotate_left,1),partial(self.rotate_left,-1),partial(self.rotate_left,2)]
        self.turn_commands = [
                                [partial(self.make_turn,1,0,True), partial(self.make_turn,1,1,True),partial(self.make_turn,1,2,True)],
                                [partial(self.make_turn,-1,0,True), partial(self.make_turn,-1,1,True),partial(self.make_turn,-1,2,True)],
                                [partial(self.make_turn,2,0,True), partial(self.make_turn,2,1,True),partial(self.make_turn,2,2,True)],
                                [partial(self.make_turn,1,0,False), partial(self.make_turn,1,1,False),partial(self.make_turn,1,2,False)],
                                [partial(self.make_turn,-1,0,False), partial(self.make_turn,-1,1,False),partial(self.make_turn,-1,2,False)],
                                [partial(self.make_turn,2,0,False), partial(self.make_turn,2,1,False),partial(self.make_turn,2,2,False)]
                                ]
        self.is_turning = False

        for i in range(6):
            for j in range(3):
                self.controls[i][j] = tk.Button(self.root, text = symbs[i], command =self.controls_commands[i])
                self.controls[i][j].place(x= corners[i][j][0], y= corners[i][j][1], width=dim[i>2][0], height=dim[i>2][1])

    # rotate cube up a given number of times
    def rotate_up(self, times = 1):
        times %= 4
        order = [0,2,5,4,0,2,5]
        order = order[times:times+4]
        order = [order[0], 1, order[1], 3, order[3], order[2]]
        
        self.boards[4].rotate()
        old_boards = [deepcopy(face.board) for face in self.boards]
        for i in range(len(self.boards)):
            self.boards[i].board = old_boards[order[i]]
            self.boards[i].count_wins()
        self.boards[4].rotate()
        self.boards[1].rotate(times)
        self.boards[3].rotate(-times)
        self.is_turning = False

    # rotate cube left a given number of times
    def rotate_left(self, times = 1):
        times %= 4
        order = [1,2,3,4,1,2,3]
        order = [0] + order[times:times+4] + [5]
        
        old_boards = [deepcopy(face.board) for face in self.boards]
        for i in range(len(self.boards)):
            self.boards[i].board = old_boards[order[i]]
            self.boards[i].count_wins()
        self.boards[0].rotate(-times)
        self.boards[5].rotate(times)
        self.is_turning=False

    # turn a row/ col based on index, centered on board 2
    def make_turn(self, times = 1, index = 1, is_col = True):
        times %= 4
        if is_col:
            order = [0,2,5,4,0,2,5]
            order = order[times:times+4]
            order = [order[0], 1, order[1], 3, order[3], order[2]]
            self.boards[4].rotate()
            col = [deepcopy(board.board[index]) for board in self.boards]
            col = [col[i] for i in order]
            for i in range(6):
                self.boards[i].board[index] = col[i]
                self.boards[i].count_wins()
            self.boards[4].rotate()
            if index == 0:
                self.boards[1].rotate(times)
            elif index == 2:
                self.boards[3].rotate(-times)

        else:
            order = [1,2,3,4,1,2,3]
            order = [0]+order[times:times+4]+[5]
            row = [[deepcopy(board.board[0][index]),deepcopy(board.board[1][index]),deepcopy(board.board[2][index])] for board in self.boards]
            row = [row[i] for i in order]
            for i in range(6):
                for j in range(3):
                    self.boards[i].board[j][index] = row[i][j]
                    self.boards[i].count_wins()
            if index == 0:
                self.boards[0].rotate(-times)
            elif index == 2:
                self.boards[5].rotate(times)
            
        self.update_cube_display()
        self.is_turning = False
        self.toggle_controls()


    def toggle_controls(self):
        print(1)
        if self.is_turning:
            for i in range(6):
                for j in range(3):
                    self.controls[i][j]['command'] = self.turn_commands[i][j]
                    self.controls[i][j]['bg'] = '#FF3012'
        else:
            for i in range(6):
                for j in range(3):
                    self.controls[i][j]['command'] = self.controls_commands[i]
                    self.controls[i][j]['bg'] = '#FFFFFF'


    # displays all the Board instances
    def display_cube(self):
        self.playfield.display_board()
        for board in self.boards:
            board.display_board()
    # updates display of boards
    def update_cube_display(self):
        self.playfield.board = self.boards[2].board
        self.playfield.update_board()
        for board in self.boards:
            board.update_board()
    
    def sync_boards(self):
        pass

    # update the attributes of the cube after each move
    def update_cube_state(self):
        self.update_cube_display()
        # store previous wins
        old_wins = deepcopy(self.wins)

        self.boards[2].wins=self.playfield.wins
        # count current wins
        for key in self.wins.keys():
            self.wins[key] = sum([board.wins[key] for board in self.boards])
        self.update_scoreboard()

        # check if total num of wins for a player increases
        if self.wins[1] > old_wins[1] or self.wins[2] > old_wins[2]:
            # check who is turning cube
            turner = (self.wins[1] > old_wins[1]) + (self.wins[2] > old_wins[2])
            priority = 2 - (self.turn_num%2)
            # prompt to turn cube
            self.turn_cube()

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
                #self.parent.restart()
                start()
            else:
                tkinter.messagebox.showinfo(title='Good Game!',message='Thanks for playing!')
                self.root.destroy()

    def turn_cube(self):
        # display turn buttons over current board
        # prompt turn
        
        pass

class Board(Cube):
    # init empty board and board score
    def __init__(self, parent=None, root=None, corner = (380,80), side = 15):
        if parent is None:
            super().__init__(root)
        self.parent = parent
        self.root = root

        # get parameters
        self.side = side
        self.corner = corner

        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.wins = {1: 0, 2: 0} # 1: circle, 2: cross

        self.buttons = [[None, None, None], [None, None, None], [None, None, None]]

    # displays the board of buttons
    def display_board(self):
        x,y = self.corner
        for i in range(3):
            for j in range(3):
                symb = 'O'*(self.board[i][j] == 1) + 'X'*(self.board[i][j] == 2)
                self.buttons[i][j] = tk.Button(self.root, text = symb, command=partial(self.make_move,(i,j)))
                self.buttons[i][j].place(x= x + i * self.side, y= y + j * self.side, width=self.side, height=self.side)
    # updates the text for each button
    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = 'O'*(self.board[i][j] == 1) + 'X'*(self.board[i][j] == 2)

    # recusive method to rotate orientation of a face anticlockwise a given number of times
    def rotate(self, times = 2):
        times %= 4
        if times == 0:
            return self.board

        old_board = deepcopy(self.board)
        self.board[0][0] = old_board[2][0]
        self.board[0][1] = old_board[1][0]
        self.board[0][2] = old_board[0][0]
        self.board[1][0] = old_board[2][1]
        self.board[1][2] = old_board[0][1]
        self.board[2][0] = old_board[2][2]
        self.board[2][1] = old_board[1][2]
        self.board[2][2] = old_board[0][2]
        self.parent.update_cube_display()
        self.rotate(times-1)

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
    def make_move(self, coords = (0,0)):
        # get current turn number from parent
        turn_num = self.parent.turn_num
        i,j = coords

        # Check if we have valid coordinates
        # If valid coordinates, update the board
        is_valid = self.coordinates_valid(coords)
        if (is_valid):
            self.board[i][j] = 2 - (turn_num%2)
            self.buttons[i][j]['text'] = 'O'*(self.board[i][j] == 1) + 'X'*(self.board[i][j] == 2)

            self.is_turning = False
            self.count_wins()
            self.parent.update_cube_state()
            self.parent.toggle_controls()
            self.parent.turn_num += 1

        else:
            tkinter.messagebox.showinfo(title='Invalid cell',message='Please choose a valid cell')

    # count the number of wins on the board
    def count_wins(self):
        wins = {1: 0, 2: 0} # 1: circle, 2: cross
        previous_wins=self.wins
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
        print(wins)
        if previous_wins[1]<wins[1] or previous_wins[2]<wins[2]:
            self.parent.is_turning=True
            print(88)
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