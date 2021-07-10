from tkinter import *
from tkinter.ttk import *
import mysql.connector
from datetime import *

si_dcurrent = datetime.now().date().strftime('%Y-%m-%d')

mydb = mysql.connector.connect(user='lifechoices', password='@Lifechoices1234', host='127.0.0.1',
                                   database='LCSignIn',
                                   auth_plugin='mysql_native_password')

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM Signin WHERE Sign_in_date=curdate() AND Sign_out_date IS NULL")
record = mycursor.fetchall()

print(len(record))
