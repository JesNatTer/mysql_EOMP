from tkinter import *

root = Tk()
root.geometry('300x300')
root.config(bg='black')

thesquare = Label(root, text='square', bg='black', fg='white')
thesquare.place(x=130, y=130)

root.mainloop()