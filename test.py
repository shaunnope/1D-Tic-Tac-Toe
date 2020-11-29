import tkinter as tk
from functools import partial

root = tk.Tk()
root.title('1d')
root.geometry('500x300+500+100')

buttonlist = {}

def play(i):
    print('Hello' + str(i))
    buttonlist[i]['text'] = 'o'

for i in range(2):
    buttonlist[i] = tk.Button(root, command= partial(play,i) )
    buttonlist[i].place(x=100 + i*60 , y=80, width=60, height=60)




root.mainloop()

# root = tk.Tk()
# root.title('1d')
# root.geometry('500x300+500+100')


# def play():
#     # change button state
#     # update game
#     pass


# a = Application(master=root)
# a.draw_board()
# root.mainloop()