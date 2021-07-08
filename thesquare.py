from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

biglist = [(123, 456, 789), (123, 456, 789), (123, 456, 789), (123, 456, 789)]

root = Tk()
root.geometry('400x400')

def testfunc():
    print(int(tv.selection()[0]) + 1)

def testfunc2():
    if tv.selection() == ():
        print('none')
    else:
        print(tv.selection())


tv = Treeview(root)
tv['columns'] = ('number1', 'number2', 'number3')
tv.column('#0', width=0, stretch=NO)
tv.column('number1', anchor=CENTER, width=80)
tv.column('number2', anchor=CENTER, width=80)
tv.column('number3', anchor=CENTER, width=80)

tv.heading('#0', text='', anchor=CENTER)
tv.heading('number1', text='n1', anchor=CENTER)
tv.heading('number2', text='n2', anchor=CENTER)
tv.heading('number3', text='n3', anchor=CENTER)

tv.insert(parent='', index=0, iid=0, text='', values=biglist[0])
tv.insert(parent='', index=1, iid=1, text='', values=biglist[1])
tv.insert(parent='', index=2, iid=2, text='', values=biglist[2])
tv.insert(parent='', index=3, iid=3, text='', values=biglist[3])

xx = Button(root, text='test', command=testfunc2)
xx.pack()

tv.pack()

root.mainloop()
