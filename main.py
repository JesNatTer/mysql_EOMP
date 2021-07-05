from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
import mysql.connector
from tkinter.ttk import Combobox

root = Tk()
root.geometry("400x400")
root.config(bg='#BCFF33')
root.resizable(0, 0)
titlefont = Font(family='Helvetica', size=25)

mydb = mysql.connector.connect(user='lifechoices', password='@Lifechoices1234', host='127.0.0.1',
                                   database='LCSignIn',
                                   auth_plugin='mysql_native_password')
mycursor = mydb.cursor()


class Login:
    def __init__(self, master):
        self.title = Label(master, text='Welcome to Life Choices', font=titlefont, bg='#BCFF33')
        self.title.place(x=15, y=20)
        self.namelbl = Label(master, text='Enter username', bg='#BCFF33')
        self.namelbl.place(x=135, y=90)
        self.nameent = Entry(master)
        self.nameent.place(x=135, y=120)
        self.passlbl = Label(master, text='Enter password', bg='#BCFF33')
        self.passlbl.place(x=135, y=140)
        self.passent = Entry(master)
        self.passent.place(x=135, y=170)

        def Signin():
            mycursor.execute("SELECT Password FROM users WHERE Name='" + self.nameent.get() + "'")
            records = mycursor.fetchall()
            if records == []:
                messagebox.showerror("Invalid Credentials", "User does not exist.")
                self.nameent.delete(0, END)
                self.passent.delete(0, END)
            else:
                if self.passent.get() == records[0][0]:
                    messagebox.showinfo("Login Successful", "Enter to the next screen.")
                    root.destroy()
                    import thesquare
                else:
                    messagebox.showerror("Login Unsuccessful", "Username and password do not correspond")
                    self.nameent.delete(0, END)
                    self.passent.delete(0, END)

        self.signinbtn = Button(master, text='Sign In', width=15, command=Signin)
        self.signinbtn.place(x=140, y=220)
        self.registerlbl = Label(master, text='If you do not have an account, please register:', bg='#BCFF33')
        self.registerlbl.place(x=75, y=310)

        def Register():
            window = Toplevel()
            window.geometry('300x400')
            window.resizable(0, 0)

            idlabel = Label(window, text='ID Number')
            idlabel.place(x=20, y=20)
            namelabel = Label(window, text='Name')
            namelabel.place(x=20, y=40)
            surnamelabel = Label(window, text='Surname')
            surnamelabel.place(x=20, y=60)
            phonelabel = Label(window, text='Contact No.')
            phonelabel.place(x=20, y=80)
            passwordlabel = Label(window, text='Password')
            passwordlabel.place(x=20, y=100)

            roleset = StringVar(window)
            roleset.set("A")
            rolecombolist = ['STUDENT', 'LECTURER', 'GUEST']
            roleselector = Combobox(window, textvariable=roleset)
            roleselector['values'] = rolecombolist
            roleselector['state'] = 'readonly'
            roleselector.place(x=20, y=130)

        self.registerbtn = Button(master, text='Register', width=15, command=Register)
        self.registerbtn.place(x=140, y=340)


login = Login(root)
root.mainloop()
