from tkinter import *
import mysql.connector as mysql

root=Tk()
root.geometry("300x300")

root.title("Atm system")
MyLabel=Label(root,text="welcome to Bank ATM system").pack()

cnx=mysql.connect(user='root',password='sql123',host='localhost')
u_name=""
pwd=""
if cnx.is_connected():
    print("Connected")
    cur=cnx.cursor()

    query1="create database project;"
    cur.execute(query1)

    x="use project;"
    cur.execute(x)   

    query2="create table bank(Name varchar(6),age int,gender varchar(6),password varchar(12),balance int Default 1000);"
    cur.execute(query2)

    def Register():
        Register_screen=Toplevel(root)
        Register_screen.title("Registration")

        l1=Label(Register_screen,text="enter the details below to register",font=('Çalibri',12))
        l1.grid(row=0,sticky=N)
        l2=Label(Register_screen,text="name",font=('Calibri',12))
        l2.grid(row=1,sticky=W)
        l3=Label(Register_screen,text="age",font=('Calibri',12))
        l3.grid(row=2,sticky=W)
        l4=Label(Register_screen,text="gender",font=('Calibri',12))
        l4.grid(row=3,sticky=W)
        l5=Label(Register_screen,text="password",font=('Calibri',12))
        l5.grid(row=4,sticky=W)
        global notif1
        notif1=Label(Register_screen,font=('Calibri',12))
        notif1.grid(row=7,sticky=N)

    
        global temp_name
        global temp_age
        global temp_gender
        global temp_password
        temp_name=StringVar()
        temp_age=StringVar()
        temp_gender=StringVar()
        temp_password=StringVar()

        e1=Entry(Register_screen,text=temp_name,width=20)
        e1.grid(row=1)
        e2=Entry(Register_screen,text=temp_age,width=20)
        e2.grid(row=2)
        e3=Entry(Register_screen,text=temp_gender,width=20)
        e3.grid(row=3)
        e4=Entry(Register_screen,text=temp_password,show="*",width=15)
        e4.grid(row=4)

        b1=Button(Register_screen,text="Register now",command=finish_reg,padx=30)
        b1.grid(row=6)

    def finish_reg():
        print("Done")
        name=temp_name.get()
        age=temp_age.get()
        gender=temp_gender.get()
        password=temp_password.get()
        

        if name=="" or age=="" or gender=="" or password=="":
            notif1.config(fg="red",text="all fields need to be filled")
            return
        chk=0
        x="use project;"
        cur.execute(x)
        query="select name from bank"
        cur.execute(query)
        data=cur.fetchall()
        print(data)
        for i in data:
            if name in i:
                notif1.config(fg="red",text="username already exists")
                chk+=1
        if chk==0:        
            x="use project;"
            cur.execute(x)
            query3="insert into bank values('{}',{},'{}','{}',default);".format(name,age,gender,password)
            cur.execute(query3)
            cnx.commit()
    
    def login():
        global login_screen
        login_screen=Toplevel(root)
        login_screen.title("login")
    
        l6=Label(login_screen,text="Enter the details below to login to your account",font=('Çalibri',12))
        l6.grid(row=0,sticky=N)
        l7=Label(login_screen,text="Username",font=('Calibri',12))
        l7.grid(row=2,sticky=W)
        l8=Label(login_screen,text="Password",font=('Calibri',12))
        l8.grid(row=3,sticky=W)
   
        global notif2
        notif2=Label(login_screen,font=('Calibri',12))
        notif2.grid(row=5,sticky=N)

        global temp_username
        global temp_password
    
    
        temp_username=StringVar()
        temp_password=StringVar()

        e5=Entry(login_screen,text=temp_username,width=30)
        e5.grid(row=2)
        e6=Entry(login_screen,text=temp_password,show="*",width=30)
        e6.grid(row=3)

        b2=Button(login_screen,text="login",command=finish_login,padx=30)
        b2.grid(row=4)

    def finish_login():
        global u_name
        u_name=temp_username.get()
        global pwd
        pwd=temp_password.get()
        query="select name,password from bank;"
        cur.execute(query)
        data=cur.fetchall()
        chk=0
        for i in data:
            name=i[0]
            passwd=i[1]

            if name==u_name and passwd==pwd:
                chk+=1
                break
        if chk==1:

                print("Your account has been found")
                login_screen.destroy()
                acct_dashboard=Toplevel(root)
                acct_dashboard.title("Account dashboard")

                Label(acct_dashboard,text="This is your account dashboard",font=('Calibri',12)).grid(row=0,sticky=N)
                Label(acct_dashboard,text="welcome",font=('Calibri',12)).grid(row=1,sticky=N)

                Button(acct_dashboard,text="Personal details",command=personal_details,padx=20).grid(row=3)
                Button(acct_dashboard,text="Deposit",command=deposit,padx=20).grid(row=4)
                Button(acct_dashboard,text="Withdraw",command=withdraw,padx=20).grid(row=5)
        else:
                 
                notif2.config(fg="red",text="Incorrect Details !")
                return
    
    def withdraw():
        global amt
        global withdraw_balance
        global withdraw_notif
        global with_screen
        amt=StringVar()
        with_screen=Toplevel(root)
        with_screen.title("Withdraw here")
        query="select * from bank where name='{}' and password='{}';".format(u_name,pwd)
        cur.execute(query)
        data=cur.fetchone()
        
        user_name=data[0]
        user_age=data[1]
        user_gender=data[2]
        balance=data[4]
        
        
        Label(with_screen,text="Withdraw here",font=('Calibri',12)).grid(row=0)
        withdraw_balance=Label(with_screen,text="withdraw balance :",font=('Calibri',12))
        withdraw_balance.grid(row=1)
        Label(with_screen,text="Amount :",font=('Calibri',12)).grid(row=2)
        withdraw_notif=Label(with_screen,font=('Calibri',12))
        withdraw_notif.grid(row=4)

        Entry(with_screen,text=amt,width=20).grid(row=2,column=1)
        
        Button(with_screen,text="View",command=view_with,padx=30).grid(row=1,column=1)
        Button(with_screen,text="Withdraw now",command=finish_withdraw,padx=30).grid(row=3)

    def finish_withdraw():

        global upd_balance
        query="select * from bank where name='{}' and password='{}';".format(u_name,pwd)
        cur.execute(query)
        data=cur.fetchone()
        
        user_name=data[0]
        user_age=data[1]
        user_gender=data[2]
        bal=amt.get()
        print(type(bal))
        bal=bal.strip()
        print(bal)
        
        balance=data[4]
        
        if float(bal)>float(balance):
            withdraw_notif.config(fg="red",text="Amount exceeding balance! Please enter a valid amount")
            return

        
        upd_balance=balance
        upd_balance=float(balance)-float(amt.get())
        if upd_balance<1000:
            withdraw_notif.config(fg="red",text="Balance less than default!")
        else:
            query5="update bank set balance={} where name='{}';".format(upd_balance,user_name)
            cur.execute(query5)
            cnx.commit()
            withdraw_balance=Label(with_screen,text="withdraw balance :",font=('Calibri',12))
            withdraw_balance.grid(row=1,sticky=W)
            withdraw_notif.config(fg="green",text="balance has been updated")

    def deposit():
        global amt
        global current_balance
        global deposit_notif
        global depo_screen
        amt=StringVar()
        depo_screen=Toplevel(root)
        depo_screen.title("Deposit")
        query="select * from bank where name='{}' and password='{}';".format(u_name,pwd)
        cur.execute(query)
        data=cur.fetchone()
        
        user_name=data[0]
        user_age=data[1]
        user_gender=data[2]
        balance=data[4]
    

        Label(depo_screen,text="Deposit here",font=('Calibri',12)).grid(row=0,sticky=N)
        current_balance=Label(depo_screen,text="user balance :",font=('Calibri',12))
        current_balance.grid(row=1,sticky=W)
        Label(depo_screen,text="Amount :",font=('Calibri',12)).grid(row=2,sticky=W)
        deposit_notif=Label(depo_screen,font=('Calibri',12))
        deposit_notif.grid(row=4)

        Entry(depo_screen,text=amt,width=20).grid(row=2,column=1)
        
        Button(depo_screen,text="View",command=view_dep,padx=30).grid(row=1,column=1)
        Button(depo_screen,text="Deposit now",command=finish_deposit,padx=30).grid(row=3)

    def finish_deposit():
        query="select * from bank where name='{}' and password='{}';".format(u_name,pwd)
        cur.execute(query)
        data=cur.fetchone()
        
        user_name=data[0]
        user_age=data[1]
        user_gender=data[2]

        if amt.get()=="":
            deposit_notif.config(fg="red",text="This field has to be entered")
            return

        if float(amt.get())<=0:
            deposit_notif.config(fg="red",text="The amount entered is invalid, Please enter a valid amount")
            return

        global upd_balance
        
        bal=data[4]
        upd_balance=bal
        upd_balance=float(bal)+float(amt.get())
        query6="update bank set balance={} where name='{}';".format(upd_balance,user_name)
        cur.execute(query6)
        cnx.commit()

        current_balance=Label(depo_screen,text="User balance : ",font=('Calibri',12))
        current_balance.grid(row=1,sticky=W)
        deposit_notif.config(fg="green",text="balance has been updated")

    def view_dep():
        query="select * from bank where name='{}' and password='{}';".format(u_name,pwd)
        cur.execute(query)
        data=cur.fetchone()
        
        user_name=data[0]
        user_age=data[1]
        user_gender=data[2]
        upd_balance=data[4]


        global bal_screen
        bal_screen=Toplevel(root)
        bal_screen.title("Balance")
        Label(bal_screen,text="Your balance is :"+str(upd_balance),font=('Calibri',12)).grid(row=0,sticky=N)

    def view_with():
        query="select * from bank where name='{}' and password='{}';".format(u_name,pwd)
        cur.execute(query)
        data=cur.fetchone()
        
        user_name=data[0]
        user_age=data[1]
        user_gender=data[2]
        upd_balance=data[4]

        global bal_screen
        bal_screen=Toplevel(root)
        bal_screen.title("Balance")
        Label(bal_screen,text="Your balance is :"+str(upd_balance),font=('Calibri',12)).grid(row=0,sticky=N)
        
    def personal_details():
    
        query="select * from bank where name='{}' and password='{}';".format(u_name,pwd)
        cur.execute(query)
        data=cur.fetchone()
        
        user_name=data[0]
        user_age=data[1]
        user_gender=data[2]

        user_screen=Toplevel(root)
        user_screen.title("My Account")

        Label(user_screen,text="User account",font=('Calibri',12)).grid(row=0,sticky=N)
        Label(user_screen,text="Here are the details of your account",font=('Calibri',12)).grid(row=1,sticky=N)
        Label(user_screen,text="Name :" + user_name,font=('Calibri',12)).grid(row=2,sticky=W)
        Label(user_screen,text="Age :" + str(user_age),font=('Calibri',12)).grid(row=3,sticky=W)
        Label(user_screen,text="Gender :"+user_gender,font=('Calibri',12)).grid(row=4,sticky=W)
        Label(user_screen,text="Balance : $" ,font=('Calibri',12)).grid(row=5,sticky=W)
        user_screen.mainloop()
    
    myButton=Button(root,text="Register",padx=20,command=Register)
    myButton.pack()

    myButton2=Button(root,text="Login",padx=20,command=login)
    myButton2.pack()

    root.mainloop()
