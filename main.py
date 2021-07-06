from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
import mysql.connector
from tkinter.ttk import Combobox
from datetime import datetime

root = Tk()
root.geometry("400x400")
root.config(bg='#BCFF33')
root.resizable(0, 0)
titlefont = Font(family='Helvetica', size=25)

mydb = mysql.connector.connect(user='lifechoices', password='@Lifechoices1234', host='127.0.0.1',
                                   database='LCSignIn',
                                   auth_plugin='mysql_native_password')

mycursor = mydb.cursor()
current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
                    root.withdraw()
                    self.signedinscreen()
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
            identry = Entry(window)
            identry.place(x=130, y=20)
            namelabel = Label(window, text='Name')
            namelabel.place(x=20, y=40)
            nameentry = Entry(window)
            nameentry.place(x=130, y=40)
            surnamelabel = Label(window, text='Surname')
            surnamelabel.place(x=20, y=60)
            surnameentry = Entry(window)
            surnameentry.place(x=130, y=60)
            phonelabel = Label(window, text='Contact No.')
            phonelabel.place(x=20, y=80)
            phoneentry = Entry(window)
            phoneentry.place(x=130, y=80)
            passwordlabel = Label(window, text='Password')
            passwordlabel.place(x=20, y=100)
            passentry = Entry(window)
            passentry.place(x=130, y=100)
            kinlbl = Label(window, text='Next of Kin details:')
            kinlbl.place(x=20, y=190)
            kinnamelbl = Label(window, text='Name')
            kinnamelbl.place(x=20, y=220)
            kinnameentry = Entry(window)
            kinnameentry.place(x=130, y=220)
            kin_nolbl = Label(window, text='Phone Number')
            kin_nolbl.place(x=20, y=240)
            kin_noentry = Entry(window)
            kin_noentry.place(x=130, y=240)

            rolelbl = Label(window, text='Registering As:')
            rolelbl.place(x=20, y=130)
            roleset = StringVar(window)
            roleset.set("A")
            rolecombolist = ['STUDENT', 'LECTURER', 'GUEST']
            roleselector = Combobox(window, textvariable=roleset)
            roleselector['values'] = rolecombolist
            roleselector['state'] = 'readonly'
            roleselector.place(x=130, y=130)

            def SignUp():
                sql1 = "INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s)"
                val1 = (identry.get(), nameentry.get(), surnameentry.get(), phoneentry.get(), passentry.get(), roleset.get())
                sql2 = "INSERT INTO next_of_kin (ID, Name, Phone_number) VALUES (%s, %s, %s)"
                val2 = (identry.get(), kinnameentry.get(), kin_noentry.get())
                mycursor.execute(sql1, val1)
                mycursor.execute(sql2, val2)
                mydb.commit()
                messagebox.showinfo("Successful", "Your account is registered. You may now sign in.")
                window.destroy()

            registeruserbtn = Button(window, text='Sign Up', command=SignUp)
            registeruserbtn.place(x=20, y=300)

        self.registerbtn = Button(master, text='Register', width=15, command=Register)
        self.registerbtn.place(x=140, y=340)

        def AdminSignIn(event=None):
            master.withdraw()
            ascreen = Toplevel()
            ascreen.geometry('350x450')
            ascreen.resizable(0, 0)
            acanvas = Canvas(ascreen, width=500, height=600, highlightbackground='#aaa')
            acanvas.place(x=-10, y=-10)
            aimg = PhotoImage(file="./images/jean-philippe-delberghe-75xPHEQBmvA-unsplash.png")
            aimg = aimg.subsample(4)
            acanvas.create_image(230, 290, image=aimg)
            aframe = Frame(ascreen, width=300, height=200, bg='#999')
            aframe.place(x=25, y=150)
            ascreen.mainloop()

        master.bind('<Control-a>', AdminSignIn)

        master.mainloop()

    def signedinscreen(self):
        mycursor.execute("SELECT Name, Surname, Role FROM users WHERE Name='" + self.nameent.get() + "'")
        data = mycursor.fetchall()
        sscreen = Toplevel()
        sscreen.geometry('400x500')
        scanvas = Canvas(sscreen, width=500, height=600, highlightbackground='yellow')
        scanvas.place(x=-10, y=-10)
        simg = PhotoImage(file="./images/ben-neale-sQQf8Ao3dpk-unsplash (1).png")
        simg = simg.subsample(4)
        scanvas.create_image(230, 290, image=simg)

        signedinlbl = Label(sscreen, text='Signed In', font=titlefont, bg='#aaa')
        signedinlbl.place(x=130, y=20)
        frame = Frame(sscreen, width=300, height=200, bg='#aaa')
        frame.place(x=50, y=250)

        rolelbl = Label(frame, text='Role: ' + data[0][2], bg='#aaa')
        rolelbl.place(x=20, y=20)
        timelbl = Label(frame, text='Time of Sign In: ' + str(datetime.now()), bg='#aaa')
        timelbl.place(x=20, y=60)


        sscreen.mainloop()


login = Login(root)
