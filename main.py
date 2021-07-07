from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
import mysql.connector
from tkinter.ttk import Combobox
from datetime import datetime
import rsaidnumber


root = Tk()
root.geometry("400x400")
root.title('Life Choices Online')
root.resizable(0, 0)
titlefont = Font(family='Helvetica', size=25)

mydb = mysql.connector.connect(user='lifechoices', password='@Lifechoices1234', host='127.0.0.1',
                                   database='LCSignIn',
                                   auth_plugin='mysql_native_password')

mycursor = mydb.cursor()
dcurrent = datetime.now().date().strftime("%Y-%m-%d")
tcurrent = datetime.now().time().strftime('%H:%M:%S')


class Login:
    def __init__(self, master):
        self.mcanvas = Canvas(master, width=500, height=600, highlightbackground='#aaa')
        self.mcanvas.place(x=-10, y=-10)
        self.mimg = PhotoImage(file="./images/andrew-ridley-jR4Zf-riEjI-unsplash.png")
        self.mimg = self.mimg.subsample(1)
        self.mcanvas.create_image(230, 250, image=self.mimg)
        self.title = Label(master, text='Welcome to Life Choices', font=titlefont, bg='#83E6DC')
        self.title.place(x=18, y=20)
        self.idlbl = Label(master, text='Enter ID', bg='#83E6DC')
        self.idlbl.place(x=135, y=90)
        self.ident = Entry(master)
        self.ident.place(x=135, y=120)
        self.passlbl = Label(master, text='Enter password', bg='#83E6DC')
        self.passlbl.place(x=135, y=150)
        self.passent = Entry(master)
        self.passent.place(x=135, y=180)

        def Signin():
            mycursor.execute("SELECT Password, Role FROM users WHERE ID='" + self.ident.get() + "'")
            records = mycursor.fetchall()
            if records == []:
                messagebox.showerror("Invalid Credentials", "User does not exist.")
                self.ident.delete(0, END)
                self.passent.delete(0, END)
            else:
                if self.passent.get() == records[0][0] and records[0][1] != 'ADMIN':
                    signinsql = 'INSERT INTO signin (ID, Sign_in_date, Sign_in_time) VALUES (%s, %s, %s)'
                    signinval = (self.ident.get(), dcurrent, tcurrent)
                    mycursor.execute(signinsql, signinval)
                    mydb.commit()
                    messagebox.showinfo("Login Successful", "Enter to the next screen.")
                    root.withdraw()
                    self.signedinscreen()
                elif self.passent.get() == records[0][0] and records[0][1] == 'ADMIN':
                    messagebox.showwarning('Use Admin Login', 'Admin users must log in through the Admin screen.')
                else:
                    messagebox.showerror("Login Unsuccessful", "Username and password do not correspond")
                    self.ident.delete(0, END)
                    self.passent.delete(0, END)

        self.signinbtn = Button(master, text='Sign In', width=15, command=Signin)
        self.signinbtn.place(x=140, y=220)
        self.registerlbl = Label(master, text='If you do not have an account, please register:', bg='#83E6DC')
        self.registerlbl.place(x=75, y=310)

        def Register():
            window = Toplevel()
            window.geometry('300x400')
            window.resizable(0, 0)
            window.config(bg='')

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
            roleset.set("Select your role")
            rolecombolist = ['STUDENT', 'LECTURER', 'GUEST']
            roleselector = Combobox(window, textvariable=roleset)
            roleselector['values'] = rolecombolist
            roleselector['state'] = 'readonly'
            roleselector.place(x=130, y=130)

            def SignUp():
                try:
                    phonevalid = int(phoneentry.get())
                    kphonevalid = int(kin_noentry.get())
                    if (identry.get() == '' or nameentry.get() == '' or surnameentry.get() == ''
                            or phoneentry.get() == '' or passentry.get() == '' or roleset.get() == 'Select your role'
                            or kinnameentry.get() == '' or kin_noentry.get() == ''):
                        messagebox.showerror('Entries Unfilled', 'Please fill out all entries before signing up.')
                    else:
                        if len(phoneentry.get()) != 10 and len(kin_noentry.get()) != 10:
                            messagebox.showerror('Invalid Contact Number',
                                                 'Length of contact number must be 10 digits.')
                        else:
                            idno = rsaidnumber.parse(identry.get())
                            if idno.valid is False:
                                messagebox.showerror('Invalid ID', 'Please enter a valid SA ID.')
                            else:
                                if str.isalpha(nameentry.get()) is False or str.isalpha(kinnameentry.get()) is False\
                                        or str.isalpha(surnameentry.get()) is False:
                                    messagebox.showerror('Invalid Name/Surname',
                                                         'Please enter only alphabetic characters for name')
                                else:
                                    sql1 = "INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s)"
                                    val1 = (identry.get(), nameentry.get(), surnameentry.get(), phoneentry.get(),
                                            passentry.get(), roleset.get())
                                    sql2 = "INSERT INTO next_of_kin (ID, Name, Phone_number) VALUES (%s, %s, %s)"
                                    val2 = (identry.get(), kinnameentry.get(), kin_noentry.get())
                                    mycursor.execute(sql1, val1)
                                    mycursor.execute(sql2, val2)
                                    mydb.commit()
                                    messagebox.showinfo("Successful", "Your account is registered. "
                                                                      "You may now sign in.")
                                    window.destroy()
                except ValueError:
                    messagebox.showerror('Invalid details', 'Phone number must be in digits only.')

            registeruserbtn = Button(window, text='Sign Up', command=SignUp)
            registeruserbtn.place(x=20, y=300)

        self.registerbtn = Button(master, text='Register', width=15, command=Register)
        self.registerbtn.place(x=140, y=340)

        def AdminSignIn(event=None):
            master.withdraw()
            ascreen = Toplevel()
            ascreen.geometry('400x500')
            ascreen.resizable(0, 0)
            acanvas = Canvas(ascreen, width=500, height=600, highlightbackground='#aaa')
            acanvas.place(x=-10, y=-10)
            aimg = PhotoImage(file="./images/jean-philippe-delberghe-75xPHEQBmvA-unsplash.png")
            aimg = aimg.subsample(4)
            acanvas.create_image(230, 290, image=aimg)
            signintitle = Label(ascreen, text='Admin Sign In', font=titlefont, bg="#999")
            signintitle.place(x=100, y=20)
            aframe = Frame(ascreen, width=300, height=200, bg='#999')
            aframe.place(x=50, y=200)
            aidlbl = Label(aframe, text='Your ID', bg='#999')
            aidlbl.place(x=20, y=20)
            aidentry = Entry(aframe)
            aidentry.place(x=140, y=20)
            apasslbl = Label(aframe, text='Your Password', bg='#999')
            apasslbl.place(x=20, y=60)
            apassentry = Entry(aframe)
            apassentry.place(x=140, y=60)

            def Asignin():
                mycursor.execute("SELECT Password, Role FROM users WHERE ID='" + aidentry.get() + "'")
                records = mycursor.fetchall()
                if records == []:
                    messagebox.showerror("Invalid Credentials", "User does not exist.")
                    aidentry.delete(0, END)
                    apassentry.delete(0, END)
                else:
                    if apassentry.get() == records[0][0] and records[0][1] == 'ADMIN':
                        signinsql = 'INSERT INTO signin (ID, Sign_in_date, Sign_in_time) VALUES (%s, %s, %s)'
                        signinval = (aidentry.get(), dcurrent, tcurrent)
                        mycursor.execute(signinsql, signinval)
                        mydb.commit()
                        messagebox.showinfo("Login Successful", "Enter to the next screen.")
                        ascreen.withdraw()
                        self.adminscreen()

                    elif apassentry.get() == records[0][0] and records[0][1] != 'ADMIN':
                        messagebox.showwarning('Unauthorized',
                                               'Only admin users may log in through the Admin screen.')
                    else:
                        messagebox.showerror("Login Unsuccessful", "Username and password do not correspond")
                        self.ident.delete(0, END)
                        self.passent.delete(0, END)

            asigninbtn = Button(aframe, text='Sign In', width=15, command=Asignin)
            asigninbtn.place(x=90, y=160)

            ascreen.mainloop()

        master.bind('<Control-a>', AdminSignIn)

        master.mainloop()

    def signedinscreen(self):
        mycursor.execute("SELECT Name, Surname, Role FROM users WHERE ID='" + self.ident.get() + "'")
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

        def signout():
            signoutsql = "INSERT INTO signin (Sign_out_date, Sign_out_time) VALUES (%s, %s) WHERE ID='" \
                         + self.ident.get() + "' AND Sign_in_date='" + dcurrent + "'"
            signoutval = (dcurrent, tcurrent)
            mycursor.execute(signoutsql, signoutval)
            mydb.commit()
            messagebox.showinfo('Sign Out successful', 'Enjoy the rest of your day!')
            sscreen.destroy()
            root.destroy()

        signoutbtn = Button(frame, text='Sign Out', command=signout)
        signoutbtn.place(x=130, y=100)

        sscreen.mainloop()

    def adminscreen(self):
        mycursor.execute("SELECT Name, Surname, Role FROM users WHERE ID='" + self.ident.get() + "'")
        data = mycursor.fetchall()
        asiscreen = Toplevel()
        asiscreen.geometry('600x600')
        asicanvas = Canvas(asiscreen, width=700, height=700, highlightbackground='yellow')
        asicanvas.place(x=-10, y=-10)
        asiimg = PhotoImage(file="./images/scott-webb-OxHPDs4WV8Y-unsplash (1).png")
        asiimg = asiimg.subsample(2)
        asicanvas.create_image(230, 290, image=asiimg)

        signedinlbl = Label(asiscreen, text='Signed In', font=titlefont, bg='#aaa')
        signedinlbl.place(x=130, y=20)
        frame = Frame(asiscreen, width=300, height=200, bg='#aaa')
        frame.place(x=50, y=250)

        def asignout():
            signoutsql = "INSERT INTO signin (Sign_out_date, Sign_out_time) VALUES (%s, %s) WHERE ID='" \
                         + self.ident.get() + "' AND Sign_in_date='" + dcurrent + "'"
            signoutval = (dcurrent, tcurrent)
            mycursor.execute(signoutsql, signoutval)
            mydb.commit()
            messagebox.showinfo('Sign Out successful', 'Enjoy the rest of your day!')
            asiscreen.destroy()
            root.destroy()

        signoutbtn = Button(frame, text='Sign Out', command=asignout)
        signoutbtn.place(x=130, y=100)

        asiscreen.mainloop()

    # def adminsigninscreen(self):
    #


login = Login(root)
