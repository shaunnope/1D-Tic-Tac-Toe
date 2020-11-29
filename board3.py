from copy import deepcopy

import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
from functools import partial


# class Game(tk.Frame):
#     def __init__(self, num_boards=6, master=None):
#         super().__init__(master)
#         self.master = master
#
#         self.num_boards = num_boards
#
#         # self.window = tk.Tk()
#         self.restart()
#
#     def restart(self):
#         # self.window.destroy()
#         self.window = tk.Tk()
#         self.window.title('1D Tic Tac Toe')
#         self.window.geometry('500x300+500+100')
#
#         self.cube = Cube(self, self.num_boards)
#
#         self.window.mainloop()


# (cross: _ wins, circle: _ wins)
class Cube:
    def __init__(self, root=None, num_boards=6):
        self.root = root
        self.turn_num = 0
        self.wins = {1: 0, 2: 0}  # 1: circle, 2: cross

        self.corner = (250, 60)
        self.side = 60
        #recording the number of wins for 'O' and 'X'
        self.scoreboard()
        self.boards = []
        if num_boards == 6:
            # init cube projection of boards
            x, y = self.corner
            w = self.side * 3
            corners = [(x + w, y), (x, y + w), (x + w, y + w), (x + 2 * w, y + w), (x + 3 * w, y + w),
                       (x + w, y + 2 * w)]
            for i in range(num_boards):
                self.boards.append(Board(self, self.root, corners[i]))

        else:
            # if not default number of boards, display boards as a row
            for i in range(num_boards):
                corner = (self.corner[0] + i * self.side * 3, self.corner[1])
                self.boards.append(Board(self, self.root, corner))

        self.display_cube()

    def scoreboard(self):
        self.label=tk.Label(text='''O wins: {}\nX wins: {}'''.format(self.wins[1],self.wins[2]),bg='#00ffff',
                            font=('Bauhaus 93 Regular',20))
        self.label.place(x=800,y=80)

    def update_scoreboard(self):
        self.label['text'] = '''O wins: {}\nX wins: {}'''.format(self.wins[1], self.wins[2])

    def display_cube(self):
        for board in self.boards:
            board.display_board()

    # update the attributes of the cube after each move
    def update_cube(self):
        for index, board in enumerate(self.boards):
            if board.winturn==True:
                self.turn_cube(board,index)
                for board2 in self.boards:
                    board2.count_wins()
                board.winturn=False

        for key in self.wins.keys():
            self.wins[key] = sum([board.wins[key] for board in self.boards])

        if self.turn_num >= len(self.boards) * 9:
            winner = "It's a tie!"
            if self.wins[1] != self.wins[2]:
                winner = 'O' * (self.wins[1] > self.wins[2]) + 'X' * (self.wins[2] > self.wins[1]) + ' wins!'
            message = f"Score\n O:   {self.wins[1]}  X:   {self.wins[2]}"
            is_restart = tkinter.messagebox.askyesno(title='Game Over',
                                                     message=winner + '\n\n' + message + '\nRestart?')
            if is_restart:
                self.root.destroy()
                # self.root.restart()
                start()
            else:
                tkinter.messagebox.showinfo(title='Good Game!', message='Thanks for playing!')
                self.root.destroy()

    def turn_cube(self, board,index):
            board=board
            index=index
            for i in range(3):
                for j in range(3):
                    board.buttons[i][j]['bg'] = '#ff8080'
            rotate_row=tk.messagebox.askyesno(title='rotate row',message='do you want to rotate a row?')
            if rotate_row:
                row_num=tk.simpledialog.askinteger(title='row number',prompt='which row do you want to rotate?(0~2)',initialvalue=None,minvalue=0,maxvalue=2)
                if index==0:
                        l4=self.boards[1].buttons[row_num][::-1]
                        l1=[self.boards[0].buttons[i][row_num] for i in range(3)]
                        l3 = [self.boards[5].buttons[2-i][2-row_num] for i in range(3)]
                        l2 = self.boards[3].buttons[2-row_num]

                elif index == 1 or index==2 or index==3 or index==4:
                        l1 = [self.boards[1].buttons[i][row_num] for i in range(3)]
                        l2 = [self.boards[2].buttons[i][row_num] for i in range(3)]
                        l3 = [self.boards[3].buttons[i][row_num] for i in range(3)]
                        l4 = [self.boards[4].buttons[i][row_num] for i in range(3)]

                else:
                        l4 = self.boards[1].buttons[2-row_num][::-1]
                        l1 = [self.boards[0].buttons[2-i][2-row_num] for i in range(3)]
                        l3 = [self.boards[5].buttons[i][row_num] for i in range(3)]
                        l2 = self.boards[3].buttons[row_num]
                for i in l1:
                    i['bg'] = '#00ffff'
                for i in l2:
                    i['bg'] = '#00ffff'
                for i in l3:
                    i['bg'] = '#00ffff'
                for i in l4:
                    i['bg'] = '#00ffff'
                # print(l1,l2,l3,l4)
                rotate = tk.messagebox.askyesno(title='rotate?', message='sure to rotate?')
                if rotate:
                    l1_text=[]
                    for button in l1:
                        t=button['text']
                        l1_text.append(t)
                    for i in range(3):
                        l1[i]['text'] = l4[i]['text']
                        l4[i]['text']=l3[i]['text']
                        l3[i]['text']=l2[i]['text']
                        l2[i]['text']=l1_text[i]
                else:
                    for i in l1:
                        i['bg'] = 'SystemButtonFace'
                    for i in l2:
                        i['bg'] = 'SystemButtonFace'
                    for i in l3:
                        i['bg'] = 'SystemButtonFace'
                    for i in l4:
                        i['bg'] ='SystemButtonFace'
                    self.turn_cube(board, index)
                for i in l1:
                    i['background'] = 'SystemButtonFace'
                for i in l2:
                    i['background'] = 'SystemButtonFace'
                for i in l3:
                    i['background'] = 'SystemButtonFace'
                for i in l4:
                    i['background'] = 'SystemButtonFace'
                for i in range(3):
                    for j in range(3):
                        board.buttons[i][j]['bg'] = 'SystemButtonFace'


            else:
                rotate_column=tk.messagebox.askyesno(title='rotate column',message='do you want to rotate a column?')
                if rotate_column:
                    column_num = tk.simpledialog.askinteger(title='column number', prompt='which column do you want to rotate?(0~2)',
                                               initialvalue=None, minvalue=0, maxvalue=2)
                    if index == 1:
                        l4 = self.boards[1].buttons[column_num][::-1]
                        l1 = [self.boards[0].buttons[i][column_num] for i in range(3)]
                        l3 = [self.boards[5].buttons[2 - i][2-column_num] for i in range(3)]
                        l2 = self.boards[3].buttons[2-column_num]

                    elif index==3:
                        l4 = self.boards[1].buttons[2-column_num][::-1]
                        l1 = [self.boards[0].buttons[i][2-column_num] for i in range(3)]
                        l3 = [self.boards[5].buttons[2 - i][column_num] for i in range(3)]
                        l2 = self.boards[3].buttons[column_num]

                    elif index == 0 or index==2 or index==5:
                        l1 = self.boards[0].buttons[column_num]
                        l2 = self.boards[2].buttons[column_num]
                        l3 = self.boards[5].buttons[column_num]
                        l4 = self.boards[4].buttons[2-column_num]

                    elif index==4:
                        l1 = self.boards[0].buttons[2-column_num]
                        l2 = self.boards[2].buttons[2-column_num]
                        l3 = self.boards[4].buttons[column_num]
                        l4 = self.boards[5].buttons[2-column_num]

                    for i in l1:
                        i['bg'] = '#00ffff'
                    for i in l2:
                        i['bg'] = '#00ffff'
                    for i in l3:
                        i['bg'] = '#00ffff'
                    for i in l4:
                        i['bg'] = '#00ffff'
                    rotate=tk.messagebox.askyesno(title='rotate?', message='sure to rotate?')
                    if rotate:
                        l1_text = []
                        for button in l1:
                            t = button['text']
                            l1_text.append(t)
                        for i in range(3):
                            l1[i]['text'] = l4[i]['text']
                            l4[i]['text'] = l3[i]['text']
                            l3[i]['text'] = l2[i]['text']
                            l2[i]['text'] = l1_text[i]
                    else:
                        for i in l1:
                            i['bg'] = 'SystemButtonFace'
                        for i in l2:
                            i['bg'] = 'SystemButtonFace'
                        for i in l3:
                            i['bg'] = 'SystemButtonFace'
                        for i in l4:
                            i['bg'] = 'SystemButtonFace'
                        self.turn_cube(board,index)
                    for i in l1:
                        i['bg'] = 'SystemButtonFace'
                    for i in l2:
                        i['bg'] = 'SystemButtonFace'
                    for i in l3:
                        i['bg'] = 'SystemButtonFace'
                    for i in l4:
                        i['bg'] ='SystemButtonFace'
                    for i in range(3):
                        for j in range(3):
                            board.buttons[i][j]['bg'] = 'SystemButtonFace'

class Board(Cube):
    # init empty board and board score
    def __init__(self, parent=None, root=None, corner=(380, 80)):
        if parent is None:
            super().__init__(root)
        self.parent = parent
        self.root = root
        self.wins = {1: 0, 2: 0}  # 1: circle, 2: cross
        self.side = 60
        self.corner = corner

        self.winturn=False

        self.buttons = [[None, None, None], [None, None, None], [None, None, None]]

    # displays the board of buttons
    def display_board(self):
        x, y = self.corner
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text='', command=partial(self.update_board, (i, j)))
                self.buttons[i][j].place(x=x + i * self.side, y=y + j * self.side, width=self.side, height=self.side)

    # returns True if coords provided is empty cell
    # False otherwise
    def coordinates_valid(self, coords=(0, 0)):
        x, y = coords

        # Check if coordinates are within range
        is_valid = (x < 3 and y < 3)
        # Check if cell is empty
        if (is_valid):
            is_valid = (self.buttons[x][y]['text'] == '')

        # If coordinates are invalid, let the user know
        if (not is_valid):
            error_message = f"Coordinates for given action are invalid! You passed {coords}."
            print(error_message)

        # Return the boolean is_valid
        return is_valid

    # attempt to update board with given move
    # if valid move, update board and inc turn_num
    # if invalid, display error window
    def update_board(self, coords=(0, 0)):
        # get current turn number from parent
        turn_num = self.parent.turn_num
        i, j = coords

        # Check if we have valid coordinates
        is_valid = self.coordinates_valid(coords)

        # If valid coordinates, update the board
        if (is_valid):
            self.buttons[i][j]['text'] = 'O' * (self.parent.turn_num%2==1) + 'X' * (self.parent.turn_num%2==0)
            self.parent.turn_num += 1
            self.count_wins()
            self.parent.update_cube()
            self.parent.update_scoreboard()

        else:
            tkinter.messagebox.showinfo(title='Invalid cell', message='Please choose a valid cell')


    # count the number of wins on the board
    def count_wins(self):
        wins = {1: 0, 2: 0}  # 1: circle, 2: cross
        previous_win=self.wins
        # Check rows and cols
        text_list = ['', 'O', 'X']
        index_list = [0, 1, 2]
        for i in range(3):
            for j in range(len(text_list)):
                if self.buttons[i][0]['text'] == text_list[j]:
                    a = index_list[j]
                if self.buttons[i][1]['text'] == text_list[j]:
                    b = index_list[j]
                if self.buttons[i][2]['text'] == text_list[j]:
                    c = index_list[j]
            row = a * b * c
            for j in range(len(text_list)):
                if self.buttons[0][i]['text'] == text_list[j]:
                    a = index_list[j]
                if self.buttons[1][i]['text'] == text_list[j]:
                    b = index_list[j]
                if self.buttons[2][i]['text'] == text_list[j]:
                    c = index_list[j]
            col = a * b * c
            if row in (1, 8):
                wins[int(row ** (1 / 3))] += 1
            if col in (1, 8):
                wins[int(col ** (1 / 3))] += 1

        # Check diagonals
        for j in range(len(text_list)):
            if self.buttons[0][0]['text'] == text_list[j]:
                a = index_list[j]
            if self.buttons[1][1]['text'] == text_list[j]:
                b = index_list[j]
            if self.buttons[2][2]['text'] == text_list[j]:
                c = index_list[j]
        diag1 = a * b * c
        for j in range(len(text_list)):
            if self.buttons[0][2]['text'] == text_list[j]:
                a = index_list[j]
            if self.buttons[1][1]['text'] == text_list[j]:
                b = index_list[j]
            if self.buttons[2][0]['text'] == text_list[j]:
                c = index_list[j]
        diag2 = a * b * c
        if diag1 in (1, 8):
            wins[int(diag1 ** (1 / 3))] += 1
        if diag2 in (1, 8):
            wins[int(diag2 ** (1 / 3))] += 1

        if wins[1] > previous_win[1] or wins[2] > previous_win[2]:
            self.winturn = True
        self.wins = wins

        return wins

class Cell:
    # instance of each board space
    def __init__(self, parent, side=60):
        self.parent = parent
        self.button = tk.Button()
        self.side = side
        pass


def start():
    root = tk.Tk()
    root.title('1D Tic Tac Toe')
    root.geometry('1600x800+-10+0')
    game = Cube(root)
    root.mainloop()


start()
# game = Game(1)
