from tkinter import *
import ttkbootstrap as ttb
from ttkbootstrap.dialogs import Messagebox as messagebox
from ttkbootstrap.toast import ToastNotification
import sqlite3
from datetime import date
import time
import csv

#setting up database
db=sqlite3.connect('data.db')

# Window stuff
root = ttb.Window(themename='cosmo')
#root.iconbitmap('images/LBSHSLMS.ico')
root.title('LBSHS LMS')
root.geometry('1150x630+100+30')
root.resizable(False, False)

#instantiating a window object
class main:
    #login logic
    def login(self):
        self.user_entry = self.username_entry.get()
        self.pass_entry = self.password_entry.get()
        global cursor
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE if not exists adm (
                Username text,
                Password text
            )""")
        # cursor.execute("INSERT INTO adm VALUES('1234','1234')")
        # cursor.execute("INSERT INTO adm VALUES('masteradmin','m@$+erp@$$w0rd')")
        cursor.execute("SELECT * FROM adm WHERE Username=(?) and Password=(?)", (self.user_entry, self.pass_entry))
        db.commit()
        self.log_check = cursor.fetchone()
        if self.log_check!=None:
            login_toast = ToastNotification(title='LBSHS LMS', message=f'{self.user_entry} has just logged in.', duration=5000, alert=True)
            login_toast.show_toast()
            self.MS()
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)
        else:
            messagebox.show_error('Username or Password is incorrect!', 'LBSHS LMS')
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)

    def MS(self):
            # CREATE books table
            cursor.execute('''CREATE TABLE if not exists books(
                book_name text,
                author text,
                book_category text,
                ascension INTEGER 'primary' KEY,
                book_status text
            )''')
            #create issues table
            cursor.execute('''CREATE TABLE if not exists issues(
                ascension INTEGER 'primary' KEY,
                book_name text,
                issued_to text,
                class text,
                date_issued text,
                return_date text,
                FOREIGN KEY (ascension) REFERENCES books (ascension)
            )''')
            cursor.execute('''CREATE TABLE if not exists damaged(
                ascension INTEGER 'primary' KEY,
                book_name text,
                issued_to text,
                class text,
                date_issued text,
                return_date text
            )''')
            
            #CREATING THE MS
            self.under_fm=Frame(root,height=630,width=1100,bg='#fff')
            self.under_fm.place(x=0,y=0)

            self.title_label = ttb.Label(self.under_fm, text='DASHBOARD', font=('monospace', 30,'bold'), bootstyle='primary')
            self.title_label.place(x=30, y=5)
            
            self.search_button=Button(self.under_fm, text=' Search Books',font=('monospace',15,'bold'),width=220, relief='flat',
                          height=0, cursor='hand2', command=self.search_page)
            self.search_button.place(x=850, y=7)
            self.search_image = PhotoImage(file='images/search24.png')
            self.search_button.config(image=self.search_image, compound=LEFT)
            self.small_search_image = self.search_image.subsample(1,1)
            self.search_button.config(image=self.small_search_image)

            # DATE ON DASHBOARD
            self.today=date.today()
            self.date=Label(self.under_fm,text='DATE : ',font=('monospace', 10, 'bold'))
            self.date.place(x=955,y=78)
            self.dat2 = Label(self.under_fm, text=self.today, font=('monospace', 10, 'bold'))
            self.dat2.place(x=1015, y=78)

            #------------------------Clock---------------------------

            def clock():
                 h = str(time.strftime("%H"))
                 m = str(time.strftime("%M"))
                 s = str(time.strftime("%S"))

                 if int(h) >=12 and int(m) >= 0:
                       self.lb7_hr.config(text="PM")

                 self.lb1_hr.config(text=h)
                 self.book_author_hr.config(text=m)
                 self.book_status_hr.config(text=s)

                 self.lb1_hr.after(200, clock)
    
            self.lb1_hr = Label(self.under_fm, text='12', font=('monospace', 17, 'bold'))
            self.lb1_hr.place(x=850, y=105, width=60, height=30)

            self.book_author_hr = Label(self.under_fm, text='05', font=('monospace', 17, 'bold'))
            self.book_author_hr.place(x=910, y=105, width=60, height=30)

            self.book_status_hr = Label(self.under_fm, text='37', font=('monospace', 17, 'bold'))
            self.book_status_hr.place(x=970, y=105, width=60, height=30)

            self.lb7_hr = Label(self.under_fm, text='AM', font=('monospace', 17, 'bold'))
            self.lb7_hr.place(x=1040, y=105, width=60, height=30)

            clock()

            # ADD Books BUTTON
            self.add_button=Button(self.under_fm, text='  Add Books',font=('monospace',15,'bold'),width=180,
                          height=0, cursor='hand2',relief='flat',command=self.addbook)
            self.add_button.place(x=40,y=100)
            self.logo_addbook= PhotoImage(file='images/bt1.png')
            self.add_button.config(image=self.logo_addbook, compound=LEFT)
            self.small_logo_addbook = self.logo_addbook.subsample(1,1)
            self.add_button.config(image=self.small_logo_addbook)

            # ISSUE BUTTON
            self.issue_button=Button(self.under_fm, text='  Issue Books',font=('monospace',15,'bold'),width=180,relief='flat',
                          height=0, cursor='hand2', command=self.issuebook)
            self.issue_button.place(x=265,y=100)
            self.logo_issuebook = PhotoImage(file='images/bt2.png')
            self.issue_button.config(image=self.logo_issuebook, compound=LEFT)
            self.small_logo_issuebook = self.logo_issuebook.subsample(1,1)
            self.issue_button.config(image=self.small_logo_issuebook)

            # EDIt BUTTON
            self.edit_button=Button(self.under_fm, text='  Edit Books',font=('monospace',15,'bold'),width=180,relief='flat',
                          height=0, cursor='hand2', command=self.editbooks)
            self.edit_button.place(x=40,y=180)
            self.logo_editbook = PhotoImage(file='images/bt3.png')
            self.edit_button.config(image=self.logo_editbook, compound=LEFT)
            self.small_logo_editbook = self.logo_editbook.subsample(1,1)
            self.edit_button.config(image=self.small_logo_editbook)

            # REturn button
            self.return_button=Button(self.under_fm, text=' Return Books ',font=('monospace',15,'bold'),width=180,relief='flat',
                          height=0, cursor='hand2', command=self.returnbooks)
            self.return_button.place(x=265,y=180)
            self.logo_returnbook = PhotoImage(file='images/bt4.png')
            self.return_button.config(image=self.logo_returnbook, compound=LEFT)
            self.small_logo_returnbook = self.logo_returnbook.subsample(1,1)
            self.return_button.config(image=self.small_logo_returnbook)

            # Delete Button
            self.delete_button=Button(self.under_fm, text=' Delete Books',font=('monospace',15,'bold'),width=180,relief='flat',
                          height=0, cursor='hand2',command=self.deletebooks)
            self.delete_button.place(x=40,y=260)
            self.logo_deletebook = PhotoImage(file='images/bt5.png')
            self.delete_button.config(image=self.logo_deletebook, compound=LEFT)
            self.small_logo_deletebook = self.logo_deletebook.subsample(1,1)
            self.delete_button.config(image=self.small_logo_deletebook)

            # Show all books button
            self.show_books_button=Button(self.under_fm, text=' Show Books',font=('monospace',15,'bold'),width=180, relief='flat',
                          height=0, cursor='hand2', command=self.showbooks)
            self.show_books_button.place(x=265,y=260)
            self.logo_show_book = PhotoImage(file='images/bt6.png')
            self.show_books_button.config(image=self.logo_show_book, compound=LEFT)
            self.small_logo_show_book = self.logo_show_book.subsample(1,1)
            self.show_books_button.config(image=self.small_logo_show_book)

            self.show_issue_but=Button(self.under_fm, text='  Show Issued',font=('monospace',15,'bold'),width=180,relief='flat',
                        height=0, cursor='hand2', command=self.showissuedbooks)
            self.show_issue_but.place(x=40,y=340)
            self.logo_show_issue = PhotoImage(file='images/bt7.png')
            self.show_issue_but.config(image=self.logo_show_issue, compound=LEFT)
            self.small_logo_show_issue = self.logo_show_issue.subsample(1,1)
            self.show_issue_but.config(image=self.small_logo_show_issue)

            #  LOGIN
            self.logout_button=Button(self.under_fm, text='  Log Out',font=('monospace',15,'bold'),width=180,relief='flat',
                        height=0, cursor='hand2', command=self.login_back)
            self.logout_button.place(x=265,y=340)
            self.logo_logout = PhotoImage(file='images/bt8.png')
            self.logout_button.config(image=self.logo_logout, compound=LEFT)
            self.small_logo_logout = self.logo_logout.subsample(1,1)
            self.logout_button.config(image=self.small_logo_logout)

            self.logo_canvas = Canvas(self.under_fm, width=400, height=300)
            self.logo_canvas.place(x=900, y=180)
            self.logo_picture = PhotoImage(file='images/logo.png')
            self.logo_canvas.create_image(0,0, image=self.logo_picture, anchor=NW)

            self.analyse_button = Button(self.under_fm, text='  Analytics',font=('monospace',15,'bold'),width=180,relief='flat',
                        height=0, cursor='hand2',command=self.analysebooks)
            self.analyse_button.place(x=265,y=490)
            self.analyse_logo = PhotoImage(file='images/bt9.png')
            self.analyse_button.config(image=self.analyse_logo, compound=LEFT)
            self.small_logo_analyse= self.analyse_logo.subsample(1,1)
            self.analyse_button.config(image=self.small_logo_analyse)


            self.damaged_button = Button(self.under_fm, text='  Damaged',font=('monospace',15,'bold'),width=180,relief='flat',
                        height=0, cursor='hand2',command=self.damages)
            self.damaged_button.place(x=145,y=410)
            self.damaged_logo = PhotoImage(file='images/bt11.png')
            self.damaged_button.config(image=self.damaged_logo, compound=LEFT)
            self.small_logo_damaged= self.damaged_logo.subsample(1,1)
            self.damaged_button.config(image=self.small_logo_damaged)

            self.info_button = Button(self.under_fm, text='  Info',font=('monospace',15,'bold'),width=180,relief='flat',
                        height=0, cursor='hand2',command=self.infomation)
            self.info_button.place(x=40,y=490)
            self.info_logo = PhotoImage(file='images/bt10.png')
            self.info_button.config(image=self.info_logo, compound=LEFT)
            self.small_logo_info= self.info_logo.subsample(1,1)
            self.info_button.config(image=self.small_logo_info)

    def infomation(self):
        messagebox.show_info("""This is the Labone SHS Library Management System. Made by Salay Abdul Muhaimin Kanton. Copyright © 2023 | Labone SHS Createch.""", 'LBSHS LMS')

    def search_page(self):
        class search_page_item(main):
            def lookup(self):
                global selected
                self.selected = self.category_search_entry.get()
                conn = sqlite3.connect('data.db')
                cursor = conn.cursor()

                self.searched = self.search_entry.get()
                global column
                if self.selected == "Choose a Category...":
                    messagebox.show_warning('Please select a category to search from', 'LBSHS LMS')
                elif self.selected == 'Ascension Number':
                    self.column = 'ascension'
                elif self.selected == 'Book Title':
                    self.column = 'book_name'
                elif self.selected == 'Author':
                    self.column = 'book_category'
                elif self.selected == 'Book Class Number':
                    self.column = 'book_status'
                elif self.selected == 'Book Category':
                    self.column = 'author'
                else:
                    messagebox.show_error('Please select a valid category to search from', 'LBSHS LMS')
                cursor.execute(f"SELECT * FROM books WHERE {self.column} LIKE '%{self.searched}%'")

                global records
                records = cursor.fetchall()

                if not records:
                    records = messagebox.show_info('No such record is on the database', 'LBSHS LMS')
                else:
                    global count
                    count = 0
                    for record in records:
                        if count % 2 == 0:
                            self.search_books_tree_show.insert(parent='', index='end', iid=count, text='', values=(record[3], record[0], record[2], record[1], record[4]), tags=('evenrow',))
                        else:
                            self.search_books_tree_show.insert(parent='', index='end', iid=count, text='', values=(record[3], record[0], record[2], record[1], record[4]), tags=('oddrow',))
                        count += 1

                    self.search_entry.delete(0,END)
                    self.category_search_entry.delete(0,END)

            def search(self):
                self.search_book_frame = Frame(root, width=1100, height=1100)
                self.search_book_frame.place(x=0, y=0)

                self.backbt = ttb.Button(self.search_book_frame, bootstyle='secondary toolbutton outline', command=self.MS, cursor="hand2")
                self.backbt.place(x=0, y=0)
                self.log = PhotoImage(file='images/back.png')
                self.backbt.config(image=self.log, compound=LEFT)
                self.small_log = self.log.subsample(1, 1)
                self.backbt.config(image=self.small_log)
                
                self.search_books_label=ttb.Label(self.search_book_frame, text='SEARCH BOOKS',font=('monospace', 30,'bold'), bootstyle='primary')
                self.search_books_label.place(x=470,y=6)

                categories = ['Choose a Category...', 'Ascension Number', 'Book Title', 'Author', 'Book Class Number', 'Book Category']
                self.category_search_entry=ttb.Combobox(self.search_book_frame,width=23,font=('monospace',10,'bold'), values=categories, text='Choose a Category to Search from...')
                self.category_search_entry.current(0)
                self.category_search_entry.place(x=600,y=90)

                self.search_books_tree_show = ttb.Treeview(self.search_book_frame)
                #defining columns storing names in a tuple
                self.search_books_tree_show['columns'] = ('Ascension No', 'Book Title', 'Author', 'Category', 'Book Class Number')

                #Formatting columns 
                self.search_books_tree_show.column('#0', width=0, stretch=NO)
                self.search_books_tree_show.column('Ascension No', anchor=CENTER, minwidth=35, width=80)
                self.search_books_tree_show.column('Book Title', width=200, anchor=W, minwidth=180)
                self.search_books_tree_show.column('Author', width=180, anchor=W, minwidth=150)
                self.search_books_tree_show.column('Category', width=150, anchor=W, minwidth=120)
                self.search_books_tree_show.column('Book Class Number', width=150, anchor=W, minwidth=120)

                #column headings
                self.search_books_tree_show.heading('#0', text="", anchor=W)
                self.search_books_tree_show.heading('Ascension No', text="Ascension No", anchor=CENTER)
                self.search_books_tree_show.heading('Book Title', text="Book Title", anchor=W)
                self.search_books_tree_show.heading('Author', text="Author",anchor=W)
                self.search_books_tree_show.heading('Category', text="Category", anchor=W)
                self.search_books_tree_show.heading('Book Class Number', text="Book Class Number", anchor=W)

                self.search_books_tree_show.tag_configure('evenrow', background='lightblue')
                self.search_books_tree_show.tag_configure('oddrow', background='white')

                self.search_books_tree_show.place(x=175, y=150, height=406)

                self.search_entry=Entry(self.search_book_frame, width=19, font=('monospace',12,'bold'))
                self.search_entry.place(x=340,y=90)
                self.search_image = PhotoImage(file = 'images/search24.png')
                self.search_button = Button(self.search_book_frame, text='', image=self.search_image, cursor='hand2', font=('monospace',15,'bold'),width=35,relief='flat',
                            height=0, command=self.lookup)
                self.search_button.place(x=520, y=90)

        object = search_page_item()
        object.search()

    def export_as_excel(self, records):
        try:    
            with open('ALL BOOKS.csv', 'w') as csvfile:
                w = csv.writer(csvfile, dialect='excel')
                w.writerow(['Book Title', 'Book Category', 'Author', 'Ascension Number', 'Book Class Number'])
                for record in records:
                        w.writerow(record)
        except(PermissionError):
            messagebox.show_warning(""" Please close ALL BOOKS.csv file """, 'LBSHS LMS')
        messagebox.show_info(""" ALL BOOKS.csv has been saved.""", 'LBSHS LMS')

    def analysebooks(self):
        class analytics(main):
            def analyse(self):
                self.analyse_book_frame = Frame(root, width=1100, height=630)
                self.analyse_book_frame.place(x=0, y=0)

                self.backbt = ttb.Button(self.analyse_book_frame, bootstyle='secondary toolbutton outline', command=self.MS, cursor="hand2")
                self.backbt.place(x=0, y=0)
                self.log = PhotoImage(file='images/back.png')
                self.backbt.config(image=self.log, compound=LEFT)
                self.small_log = self.log.subsample(1, 1)
                self.backbt.config(image=self.small_log)

                self.analyse_books_label=ttb.Label(self.analyse_book_frame,text='DATA ANALYTICS',font=('monospace', 30,'bold'), bootstyle='primary')
                self.analyse_books_label.place(x=445,y=6)

                cursor.execute("SELECT * FROM books")
                records = cursor.fetchall()

                for index, x in enumerate(records):
                    num = 0
                    for y in x:
                        num +=1
                self.export_button=Button(self.analyse_book_frame, text=' Export All Books to Excel',font=('monospace',15,'bold'),width=335, relief='flat',
                          height=0, cursor='hand2', command=lambda:self.export_as_excel(records))
                self.export_button.place(x=425, y=100)
                self.export_image = PhotoImage(file='images/excel.png')
                self.export_button.config(image=self.export_image, compound=LEFT)
                self.small_export_image = self.export_image.subsample(1,1)
                self.export_button.config(image=self.small_export_image)

                self.all_books_count = len(records)
                self.book_number_label = ttb.Label(self.analyse_book_frame, text=f'Total number of Books: {self.all_books_count} books', font=('monospace', 18,'bold'), bootstyle='primary')
                self.book_number_label.place(x=50, y=180)

                cursor.execute('SELECT * FROM issues')
                issue_records = cursor.fetchall()
                self.all_issued_books_count = len(issue_records)
                self.book_number_label = ttb.Label(self.analyse_book_frame, text=f'Total number of Issues: {self.all_issued_books_count} issues', font=('monospace', 18,'bold'), bootstyle='primary')
                self.book_number_label.place(x=710, y=180)

                self.not_issued = self.all_books_count - self.all_issued_books_count
                self.pie_canvas = ttb.Canvas(root, width=305, height=305)
                self.pie_canvas.place(x=400, y=205)

                values = [self.all_issued_books_count, self.not_issued]
                colours = ['red', '#4280E3']

                # Define the coordinates for the bounding box of the pie chart
                x1 = 100
                y1 = 100
                x2 = 300
                y2 = 300
                # Calculate the total value of the sectors
                total = sum(values)

                # Draw each sector of the pie chart
                start_angle = 0
                for i in range(len(values)):
                    # Calculate the angle for this sector
                    angle = values[i] / total * 360
                    # Draw the sector
                    self.pie_canvas.create_arc(x1, y1, x2, y2, start=start_angle, extent=angle, fill=colours[i])
                    # Update the start angle for the next sector
                    start_angle += angle

                legend_canvas_1 = ttb.Canvas(root, width=40, height=40)
                legend_canvas_1.create_polygon(20,20,0,20,0,40,20,40, fill='red')
                legend_canvas_1.place(x=50, y=470)
                legend_canvas_2 = ttb.Canvas(root, width=40, height=40)
                legend_canvas_2.create_polygon(20,20,0,20,0,40,20,40, fill='#4280E3')
                legend_canvas_2.place(x=50, y=515)

                legend_label_1 = ttb.Label(text='Issued books', bootstyle='primary', font=('monospace 10 bold'))
                legend_label_1.place(x=72, y=490)

                legend_label_2 = ttb.Label(text='Available books', bootstyle='primary', font=('monospace 10 bold'))
                legend_label_2.place(x=72, y=535)

        object = analytics()
        object.analyse()

    def addbook(self):
        class book(main):
            def create_book(self):
                self.add_book_frame =  Frame(root, width=1100, height=1100)
                self.add_book_frame.place(x=0, y=0)

                self.backbt = ttb.Button(self.add_book_frame, bootstyle='secondary toolbutton outline', command=self.MS, cursor="hand2")
                self.backbt.place(x=0, y=0)
                self.log = PhotoImage(file='images/back.png')
                self.backbt.config(image=self.log, compound=LEFT)
                self.small_log = self.log.subsample(1, 1)
                self.backbt.config(image=self.small_log)

                self.add_books_label=ttb.Label(self.add_book_frame,text='ADD BOOKS',font=('monospace', 30,'bold'), bootstyle='primary')
                self.add_books_label.place(x=480,y=6)

                #---------------------------Label---------------------------------
                self.pass_label = Label(self.add_book_frame, text='Book Name', font=('monospace',12,'bold'))
                self.pass_label.place(x=375, y=135)
                self.book_author = Label(self.add_book_frame, text='Author', font=('monospace',12,'bold'))
                self.book_author.place(x=375, y=195)
                self.category_book= Label(self.add_book_frame, text='Category', font=('monospace',12,'bold'))
                self.category_book.place(x=375, y=259)
                self.ascension_no= Label(self.add_book_frame, text='Ascension No', font=('monospace',12,'bold'))
                self.ascension_no.place(x=375, y=319)
                self.book_class = Label(self.add_book_frame, text='Book Class No', font=('monospace',12,'bold'))
                self.book_class.place(x=375, y=379)

                 #-------------------------------Entry-------------------------------------
                self.book_name_entry=Entry(self.add_book_frame,width=25,font=('monospace',12,'bold'))
                self.book_name_entry.place(x=550,y=135)
                self.book_author_entry=Entry(self.add_book_frame,width=25,font=('monospace',12,'bold'))
                self.book_author_entry.place(x=550,y=195)
                categories = ['000-099 - General Works, Computer Science & Information', '100-199 - Philosophy & Psychology', '200-299 - Religion', '300-399 - Social Science', '400-499 - Language', '500-599 - Science', '600-699 - Technology', '700-799 - Arts & Recreation', '800-899 - Literature', '900-999 - History & Geography', 'Fiction']
                self.category_book_entry=ttb.Combobox(self.add_book_frame,width=23,font=('monospace',12,'bold'), values=categories)
                self.category_book_entry.place(x=550,y=255)
                self.ascension_no_entry = Entry(self.add_book_frame, width=25, font=('monospace', 12, 'bold'))
                self.ascension_no_entry.place(x=550,y=315)
                self.book_class_entry=Entry(self.add_book_frame,width=25,font=('monospace',12,'bold'))
                self.book_class_entry.place(x=550,y=375)

                self.submit_bt=Button(self.add_book_frame,text='Submit',width=30,font=('monospace',16,'bold'), cursor='hand2',command=self.submit_book)
                self.submit_bt.place(x=400,y=475)
                self.submit_bt.bind('<Return>', self.submit_book)
            
            def submit_book(self):
                if self.ascension_no_entry.get() != "":
                    self.ttl=self.book_name_entry.get()
                    self.cat=self.category_book_entry.get()
                    self.aut=self.book_author_entry.get()
                    self.asc_no = self.ascension_no_entry.get()
                    self.stat=self.book_class_entry.get()
                    cursor=db.cursor()
                    cursor.execute("INSERT INTO books(book_name,book_category,author,ascension,book_status) values(?,?,?,?,?)", (self.ttl,self.aut,self.cat,self.asc_no,self.stat))
                    db.commit()
                    self.clear()
                else:
                    messagebox.show_warning('You need to enter the Ascension Number', 'LBSHS LMS')

            def clear(self):
                self.book_name_entry.delete(0,END)
                self.book_author_entry.delete(0,END)
                self.category_book_entry.delete(0,END)
                self.ascension_no_entry.delete(0,END)
                self.book_class_entry.delete(0,END)

        object = book()
        object.create_book()

    def issuebook(self):
        class issue(main):
            def create_issue(self):
                self.issue_book_frame = Frame(root, width=1100, height=1100)
                self.issue_book_frame.place(x=0, y=0)

                self.backbt = ttb.Button(self.issue_book_frame, command=self.MS, cursor="hand2", bootstyle='secondary toolbutton outline')
                self.backbt.place(x=0, y=0)
                self.log = PhotoImage(file='images/back.png')
                self.backbt.config(image=self.log, compound=LEFT)
                self.small_log = self.log.subsample(1, 1)
                self.backbt.config(image=self.small_log)

                self.issue_books_label=ttb.Label(self.issue_book_frame,text='ISSUE BOOKS',font=('monospace', 30,'bold'), bootstyle='primary')
                self.issue_books_label.place(x=480,y=6)

                 #---------------------------Label---------------------------------
                self.bookname = Label(self.issue_book_frame, text='Book Title', font=('monospace',12,'bold'))
                self.bookname.place(x=375, y=135)
                self.book_issuedto = Label(self.issue_book_frame, text='Issued To', font=('monospace',12,'bold'))
                self.book_issuedto.place(x=375, y=195)
                self.issuee_class= Label(self.issue_book_frame, text='Recipients Class', font=('monospace',12,'bold'))
                self.issuee_class.place(x=375, y=255)
                self.ascension_no= Label(self.issue_book_frame, text='Ascension No', font=('monospace',12,'bold'))
                self.ascension_no.place(x=375, y=319)
                self.date_issued = Label(self.issue_book_frame, text='Date Issued', font=('monospace',12,'bold'))
                self.date_issued.place(x=375, y=379)
                self.return_date = Label(self.issue_book_frame, text='Return Date', font=('monospace',12,'bold'))
                self.return_date.place(x=375, y=439)

                 #-------------------------------Entry-------------------------------------
                self.book_name_entry=Entry(self.issue_book_frame,width=25,font=('monospace',12,'bold'))
                self.book_name_entry.place(x=550,y=135)
                self.book_issuee_entry=Entry(self.issue_book_frame,width=25,font=('monospace',12,'bold'))
                self.book_issuee_entry.place(x=550,y=195)
                self.issuee_class_entry=Entry(self.issue_book_frame,width=25,font=('monospace',12,'bold'))
                self.issuee_class_entry.place(x=550,y=255)
                self.ascension_no_entry = Entry(self.issue_book_frame, width=25, font=('monospace', 12, 'bold'))
                self.ascension_no_entry.place(x=550,y=315)
                self.date_issued_entry=ttb.DateEntry(self.issue_book_frame,width=31)
                self.date_issued_entry.place(x=550,y=375)
                self.return_date_entry=ttb.DateEntry(self.issue_book_frame,width=31)
                self.return_date_entry.place(x=550,y=435)

                self.issuebt=Button(self.issue_book_frame,text='Submit',width=30,font=('monospace',16,'bold'), cursor='hand2',command=self.issue_book)
                self.issuebt.place(x=400,y=545)
                self.issuebt.bind('<Return>', self.issue_book)

            def issue_book(self):
                if self.ascension_no_entry.get() != "":
                    self.ttl=self.book_name_entry.get()
                    self.issuto=self.book_issuee_entry.get()
                    self.asc_no = self.ascension_no_entry.get()
                    self.cla=self.issuee_class_entry.get()
                    self.dateissu=self.date_issued_entry.entry.get()
                    self.retu=self.return_date_entry.entry.get()
                    cursor=db.cursor()
                    cursor.execute("INSERT INTO issues(ascension,book_name,issued_to,class,date_issued,return_date) values(?,?,?,?,?,?)", (self.asc_no,self.ttl,self.issuto,self.cla,self.dateissu,self.retu))
                    db.commit()
                    self.clear()
                else:
                    messagebox.show_warning('You need to enter the Ascension Number', 'LBSHS LMS')

            def clear(self):
                self.book_name_entry.delete(0,END)
                self.book_issuee_entry.delete(0,END)
                self.ascension_no_entry.delete(0,END)
                self.issuee_class_entry.delete(0,END)

        object = issue()
        object.create_issue()

    def editbooks(self):
        class editing(main):
            def edit(self):
                self.edit_books_frame = Frame(root, width=1100, height=1100)
                self.edit_books_frame.place(x=0, y=0)

                self.backbt = ttb.Button(self.edit_books_frame, bootstyle='secondary toolbutton outline', command=self.MS, cursor="hand2")
                self.backbt.place(x=0, y=0)
                self.log = PhotoImage(file='images/back.png')
                self.backbt.config(image=self.log, compound=LEFT)
                self.small_log = self.log.subsample(1, 1)
                self.backbt.config(image=self.small_log)

                self.edit_books_label=ttb.Label(self.edit_books_frame,text='UPDATE BOOKS',font=('monospace', 30,'bold'), bootstyle='primary')
                self.edit_books_label.place(x=420,y=6)

                def show_edit_db():
                    cursor.execute("SELECT * FROM books")
                    records = cursor.fetchall()
                    global count
                    count = 0
                    for record in records:
                        if count % 2 == 0:
                            self.all_books_tree.insert(parent='', index='end', iid=count, text='', values=(record[3], record[0], record[2], record[1], record[4]), tags=('evenrow',))
                        else:
                            self.all_books_tree.insert(parent='', index='end', iid=count, text='', values=(record[3], record[0], record[2], record[1], record[4]), tags=('oddrow',))
                        count += 1
                    db.commit()

                def update_book():
                    selected = self.all_books_tree.focus()

                    self.all_books_tree.item(selected, text="", values=(self.asc_entry.get(), self.title_entry.get(), self.auth_entry.get(), self.cat_entry.get(), self.stat_entry.get()))
                    if self.asc_entry.get() == "":
                        messagebox.show_warning('You cannot leave the Ascension Number field blank', 'LBSHS LMS')
                    else: pass
                    connect = sqlite3.connect('data.db')
                    cursor = connect.cursor()
                    
                    cursor.execute("""UPDATE books SET
                        book_name = :book_name,
                        author = :author,
                        book_category = :category,
                        ascension = :ascension,
                        book_status = :book_status

                        WHERE 1 = :num""",
                        {
                            'book_name' : self.title_entry.get(),
                            'author' : self.auth_entry.get(),
                            'category': self.cat_entry.get(),
                            'ascension' : self.asc_entry.get(),
                            'book_status' : self.stat_entry.get(),
                            'num' : 1
                        })
                    connect.commit()

                    self.title_entry.delete(0, END)
                    self.auth_entry.delete(0, END)
                    self.cat_entry.delete(0, END)
                    self.stat_entry.delete(0, END)
                    self.asc_entry.delete(0, END)

                def select_record(event):
                    self.title_entry.delete(0, END)
                    self.auth_entry.delete(0, END)
                    self.cat_entry.delete(0, END)
                    self.stat_entry.delete(0, END)
                    self.asc_entry.delete(0, END)

                    selected = self.all_books_tree.focus()
                    values = self.all_books_tree.item(selected, 'values')
                    try:    
                        self.title_entry.insert(0, values[1])
                        self.auth_entry.insert(0, values[2])
                        self.cat_entry.insert(0, values[3])
                        self.stat_entry.insert(0, values[4])
                        self.asc_entry.insert(0, values[0])
                    except:
                        pass

                self.all_books_tree = ttb.Treeview(root)

                #defining columns storing names in a tuple
                self.all_books_tree['columns'] = ('Ascension No', 'Book Title', 'Author', 'Category', 'Book Class Number')

                #Formatting columns 
                self.all_books_tree.column('#0', width=0, stretch=NO)
                self.all_books_tree.column('Ascension No', anchor=CENTER, minwidth=25, width=80)
                self.all_books_tree.column('Book Title', width=180, anchor=W, minwidth=145)
                self.all_books_tree.column('Author', width=120, anchor=W, minwidth=100)
                self.all_books_tree.column('Category', width=140, anchor=W, minwidth=100)
                self.all_books_tree.column('Book Class Number', width=140, anchor=W, minwidth=100)

                #column headings
                self.all_books_tree.heading('#0', text="", anchor=W)
                self.all_books_tree.heading('Ascension No', text="Ascension No", anchor=CENTER)
                self.all_books_tree.heading('Book Title', text="Book Title", anchor=W)
                self.all_books_tree.heading('Author', text="Author",anchor=W)
                self.all_books_tree.heading('Category', text="Category", anchor=W)
                self.all_books_tree.heading('Book Class Number', text="Book Class Number", anchor=W)

                self.all_books_tree.tag_configure('evenrow', background='lightblue')
                self.all_books_tree.tag_configure('oddrow', background='white')
              
                self.all_books_tree.place(x=265, y=95)
                self.all_books_tree.bind('<ButtonRelease-1>', select_record)

                self.editor_frame = Frame(self.edit_books_frame)
                self.editor_frame.place(x=260, y=360)

                self.title_label = Label(self.editor_frame, text='Book Title', font=('monospace',12,'bold'))
                self.title_label.grid(row=0, column=1, padx=10, pady=5)

                self.au_l = Label(self.editor_frame, text='Author', font=('monospace',12,'bold'))
                self.au_l.grid(row=0, column=2, padx=10, pady=5)

                self.cat_l = Label(self.editor_frame, text='Category', font=('monospace',12,'bold'))
                self.cat_l.grid(row=2, column=0, padx=10, pady=5)

                self.asc_no = Label(self.editor_frame, text='Ascension No', font=('monospace',12,'bold'))
                self.asc_no.grid(row=0, column=0, padx=10, pady=5)

                self.stat_l = Label(self.editor_frame, text='Book Class Number', font=('monospace',12,'bold'))
                self.stat_l.grid(row=2, column=2, padx=10, pady=5)

                # Entrys
                self.title_entry =Entry(self.editor_frame, font=('monospace',12,'bold'))
                self.title_entry.grid(row=1, column=1, padx=10, pady=5)

                self.auth_entry =Entry(self.editor_frame, font=('monospace',12,'bold'))
                self.auth_entry.grid(row=1, column=2, padx=10, pady=5)

                categories = ['000-099 - General Works, Computer Science & Information', '100-199 - Philosophy & Psychology', '200-299 - Religion', '300-399 - Social Science', '400-499 - Language', '500-599 - Science', '600-699 - Technology', '700-799 - Arts & Recreation', '800-899 - Literature', '900-999 - History & Geography', 'Fiction']
                self.cat_entry = ttb.Combobox(self.editor_frame, font=('monospace',12,'bold'), values=categories)
                self.cat_entry.grid(row=3, column=0, padx=10, pady=5)

                self.stat_entry =Entry(self.editor_frame, font=('monospace',12,'bold'))
                self.stat_entry.grid(row=3, column=2, padx=10, pady=5)
                
                self.asc_entry =Entry(self.editor_frame, font=('monospace',12,'bold'))
                self.asc_entry.grid(row=1, column=0, padx=10, pady=5)

                self.update_book_button = Button(root, text='Update',width=30,font=('monospace',16,'bold'), cursor='hand2',command=update_book)
                self.update_book_button.place(x=400, y=535)

                show_edit_db()
        object = editing()
        object.edit()

    def showbooks(self):
        class showtree(main):
            def show(self):
                self.show_books_frame = Frame(root, width=1100, height=1100)
                self.show_books_frame.place(x=0, y=0)

                self.backbt = ttb.Button(self.show_books_frame, bootstyle='secondary toolbutton outline', command=self.MS, cursor="hand2")
                self.backbt.place(x=0, y=0)
                self.log = PhotoImage(file='images/back.png')
                self.backbt.config(image=self.log, compound=LEFT)
                self.small_log = self.log.subsample(1, 1)
                self.backbt.config(image=self.small_log)

                self.show_books_label=ttb.Label(self.show_books_frame,text='ALL BOOKS : LIST',font=('monospace', 30,'bold'), bootstyle='primary')
                self.show_books_label.place(x=415,y=6)

                # DATA FROM DB
                def show_db():
                    cursor.execute("SELECT * FROM books")
                    records = cursor.fetchall()
                    global count
                    count = 0
                    for record in records:
                        if count % 2 == 0:
                            self.all_books_tree_show.insert(parent='', index='end', iid=count, text='', values=(record[3], record[0], record[2], record[1], record[4]), tags=('evenrow',))     
                        else:
                            self.all_books_tree_show.insert(parent='', index='end', iid=count, text='', values=(record[3], record[0], record[2], record[1], record[4]), tags=('oddrow',))
                        count += 1

                self.all_books_tree_show = ttb.Treeview(self.show_books_frame)
                #defining columns storing names in a tuple
                self.all_books_tree_show['columns'] = ('Ascension No', 'Book Title', 'Author', 'Category', 'Book Class No.')

                #Formatting columns 
                self.all_books_tree_show.column('#0', width=0, stretch=NO)
                self.all_books_tree_show.column('Ascension No', anchor=CENTER, minwidth=35, width=80)
                self.all_books_tree_show.column('Book Title', width=200, anchor=W, minwidth=180)
                self.all_books_tree_show.column('Author', width=180, anchor=W, minwidth=150)
                self.all_books_tree_show.column('Category', width=150, anchor=W, minwidth=120)
                self.all_books_tree_show.column('Book Class No.', width=150, anchor=W, minwidth=120)

                #column headings
                self.all_books_tree_show.heading('#0', text="", anchor=W)
                self.all_books_tree_show.heading('Ascension No', text="Ascension No", anchor=CENTER)
                self.all_books_tree_show.heading('Book Title', text="Book Title", anchor=W)
                self.all_books_tree_show.heading('Author', text="Author",anchor=W)
                self.all_books_tree_show.heading('Category', text="Category", anchor=W)
                self.all_books_tree_show.heading('Book Class No.', text="Book Class No.", anchor=W)

                self.all_books_tree_show.tag_configure('evenrow', background='lightblue')
                self.all_books_tree_show.tag_configure('oddrow', background='white')

                self.all_books_tree_show.place(x=185, y=120, height=430)
                show_db()
        object = showtree()
        object.show()

    def deletebooks(self):
        class deleting(main):
            def delete(self):
                self.delete_books_frame = Frame(root, width=1100, height=1100)
                self.delete_books_frame.place(x=0, y=0)

                self.backbt = ttb.Button(self.delete_books_frame, bootstyle='secondary toolbutton outline', command=self.MS, cursor="hand2")
                self.backbt.place(x=0, y=0)
                self.log = PhotoImage(file='images/back.png')
                self.backbt.config(image=self.log, compound=LEFT)
                self.small_log = self.log.subsample(1, 1)
                self.backbt.config(image=self.small_log)

                self.delete_books_label=ttb.Label(self.delete_books_frame,text='DELETE BOOKS',font=('monospace', 30,'bold'), bootstyle='primary')
                self.delete_books_label.place(x=390,y=6)
                def show_db_delete():
                    cursor.execute("SELECT * FROM books")
                    records = cursor.fetchall()
                    global count
                    count = 0
                    for record in records:
                        if count % 2 == 0:
                            self.all_books_tree_delete.insert(parent='', index='end', iid=count, text='', values=(record[3], record[0], record[2], record[1], record[4]), tags=('evenrow',))     
                        else:
                            self.all_books_tree_delete.insert(parent='', index='end', iid=count, text='', values=(record[3], record[0], record[2], record[1], record[4]), tags=('oddrow',))
                        count += 1

                def delete_record():
                    selected = self.all_books_tree_delete.focus()
                    stored_id = str(self.all_books_tree_delete.item(selected).get('values')[0])
                    x = self.all_books_tree_delete.selection()[0]
                    self.all_books_tree_delete.delete(x)
                    connect = sqlite3.connect('data.db')
                    cursor = connect.cursor()
                    cursor.execute("DELETE from books where oid=" + stored_id)                    
                    connect.commit()

                self.all_books_tree_delete = ttb.Treeview(root)

                #defining columns storing names in a tuple
                self.all_books_tree_delete['columns'] = ('Ascension No', 'Book Title', 'Author', 'Category',  'Book Class No.')

                #Formatting columns 
                self.all_books_tree_delete.column('#0', width=0, stretch=NO)
                self.all_books_tree_delete.column('Ascension No', anchor=CENTER, minwidth=25, width=80)
                self.all_books_tree_delete.column('Book Title', width=150, anchor=W, minwidth=120)
                self.all_books_tree_delete.column('Author', width=120, anchor=W, minwidth=100)
                self.all_books_tree_delete.column('Category', width=190, anchor=W, minwidth=180)
                self.all_books_tree_delete.column('Book Class No.', width=140, anchor=W, minwidth=100)

                #column headings
                self.all_books_tree_delete.heading('#0', text="", anchor=W)
                self.all_books_tree_delete.heading('Ascension No', text="Ascension No", anchor=CENTER)
                self.all_books_tree_delete.heading('Book Title', text="Book Title", anchor=W)
                self.all_books_tree_delete.heading('Author', text="Author",anchor=W)
                self.all_books_tree_delete.heading('Category', text="Category", anchor=W)
                self.all_books_tree_delete.heading('Book Class No.', text="Book Class No.", anchor=W)

                self.all_books_tree_delete.tag_configure('evenrow', background='lightblue')
                self.all_books_tree_delete.tag_configure('oddrow', background='white')
              
                self.all_books_tree_delete.place(x=215, y=120, height=340)

                self.delete_bt=Button(self.delete_books_frame,text='Delete',width=30,font=('monospace',16,'bold'), cursor='hand2',command=delete_record)
                self.delete_bt.place(x=400,y=515)
                self.delete_bt.bind('<Return>', delete_record)

                show_db_delete()
        object = deleting()
        object.delete()

    def damages(self):
        class damaging(main):
            def damaged(self):
                self.damaged_books_frame = Frame(root, width=1100, height=1100)
                self.damaged_books_frame.place(x=0, y=0)

                self.backbt = ttb.Button(self.damaged_books_frame, bootstyle='secondary toolbutton outline', command=self.MS, cursor="hand2")
                self.backbt.place(x=0, y=0)
                self.log = PhotoImage(file='images/back.png')
                self.backbt.config(image=self.log, compound=LEFT)
                self.small_log = self.log.subsample(1, 1)
                self.backbt.config(image=self.small_log)

                self.damaged_books_label=ttb.Label(self.damaged_books_frame,text='DAMAGED BOOKS',font=('monospace', 30,'bold'), bootstyle='primary')
                self.damaged_books_label.place(x=390,y=6)

                def show_db_return():
                    cursor.execute("SELECT * FROM damaged")
                    records = cursor.fetchall()
                    global count
                    count = 0
                    for record in records:
                        if count % 2 == 0:
                            self.all_books_tree_return.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))     
                        else:
                            self.all_books_tree_return.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))
                        count += 1

                self.all_books_tree_return = ttb.Treeview(root)

                #defining columns storing names in a tuple
                self.all_books_tree_return['columns'] = ('Ascension No', 'Book Title', 'Student\'s Name', 'Student\'s Class', 'Date Issued', 'Return Date')

                #Formatting columns 
                self.all_books_tree_return.column('#0', width=0, stretch=NO)
                self.all_books_tree_return.column('Ascension No', anchor=CENTER, minwidth=25, width=80)
                self.all_books_tree_return.column('Book Title', width=150, anchor=W, minwidth=120)
                self.all_books_tree_return.column('Student\'s Name', width=135, anchor=W, minwidth=130)
                self.all_books_tree_return.column('Student\'s Class', width=140, anchor=W, minwidth=100)
                self.all_books_tree_return.column('Date Issued', width=140, anchor=W, minwidth=100)
                self.all_books_tree_return.column('Return Date', width=140, anchor=W, minwidth=100)

                #column headings
                self.all_books_tree_return.heading('#0', text="", anchor=W)
                self.all_books_tree_return.heading('Ascension No', text="Ascension No", anchor=CENTER)
                self.all_books_tree_return.heading('Book Title', text="Book Title", anchor=W)
                self.all_books_tree_return.heading('Student\'s Name', text="Student\'s Name",anchor=W)
                self.all_books_tree_return.heading('Student\'s Class', text="Student\'s Class", anchor=W)
                self.all_books_tree_return.heading('Date Issued', text="Date Issued", anchor=W)
                self.all_books_tree_return.heading('Return Date', text="Return Date", anchor=W)

                self.all_books_tree_return.tag_configure('evenrow', background='lightblue')
                self.all_books_tree_return.tag_configure('oddrow', background='white')
              
                self.all_books_tree_return.place(x=200, y=120, height=340)

                def delete_record():
                    try:
                        selected = self.all_books_tree_delete.focus()
                        stored_id = str(self.all_books_tree_delete.item(selected).get('values')[0])
                        x = self.all_books_tree_delete.selection()[0]
                        self.all_books_tree_delete.delete(x)
                        connect = sqlite3.connect('data.db')
                        cursor = connect.cursor()
                        cursor.execute("DELETE from damaged where oid=" + stored_id)                    
                        connect.commit()
                    except (AttributeError):
                        messagebox.show_info('Please select a record to delete', 'LBSHS LMS')
                        

                self.delete_bt=Button(self.damaged_books_frame,text='Delete',width=30,font=('monospace',16,'bold'), cursor='hand2',command=delete_record)
                self.delete_bt.place(x=400,y=492)
                show_db_return()
        object = damaging()
        object.damaged()
        
    def returnbooks(self):
        class returning(main):
            def returned(self):
                self.return_books_frame = Frame(root, width=1100, height=1100)
                self.return_books_frame.place(x=0, y=0)

                self.backbt = ttb.Button(self.return_books_frame, bootstyle='secondary toolbutton outline', command=self.MS, cursor="hand2")
                self.backbt.place(x=0, y=0)
                self.log = PhotoImage(file='images/back.png')
                self.backbt.config(image=self.log, compound=LEFT)
                self.small_log = self.log.subsample(1, 1)
                self.backbt.config(image=self.small_log)

                self.return_books_label=ttb.Label(self.return_books_frame,text='RETURN BOOKS',font=('monospace', 30,'bold'), bootstyle='primary')
                self.return_books_label.place(x=400,y=6)
                def show_db_return():
                    cursor.execute("SELECT * FROM issues")
                    records = cursor.fetchall()
                    global count
                    count = 0
                    for record in records:
                        if count % 2 == 0:
                            self.all_books_tree_return.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))     
                        else:
                            self.all_books_tree_return.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))
                        count += 1

                def return_record():
                    selected = self.all_books_tree_return.focus()
                    stored_id = str(self.all_books_tree_return.item(selected).get('values')[0])
                    x = self.all_books_tree_return.selection()[0]
                    self.all_books_tree_return.delete(x)
                    connect = sqlite3.connect('data.db')
                    cursor = connect.cursor()
                    cursor.execute("DELETE from issues where oid=" + stored_id)                    
                    connect.commit()

                def damaged_books():
                    selected = self.all_books_tree_return.focus()
                    self.asc = self.all_books_tree_return.item(selected).get('values')[0]
                    self.name = self.all_books_tree_return.item(selected).get('values')[1]
                    self.issued = self.all_books_tree_return.item(selected).get('values')[2]
                    self.clas = self.all_books_tree_return.item(selected).get('values')[3]
                    self.date = self.all_books_tree_return.item(selected).get('values')[4]
                    self.returned = self.all_books_tree_return.item(selected).get('values')[5]

                    connect = sqlite3.connect('data.db')
                    cursor = connect.cursor()
                    cursor.execute("INSERT INTO damaged(ascension,book_name,issued_to,class,date_issued,return_date) values(?,?,?,?,?,?)", (self.asc,self.name,self.issued,self.clas,self.date,self.returned))
                    connect.commit()

                self.all_books_tree_return = ttb.Treeview(root)

                #defining columns storing names in a tuple
                self.all_books_tree_return['columns'] = ('Ascension No', 'Book Title', 'Student\'s Name', 'Student\'s Class', 'Date Issued', 'Return Date')

                #Formatting columns 
                self.all_books_tree_return.column('#0', width=0, stretch=NO)
                self.all_books_tree_return.column('Ascension No', anchor=CENTER, minwidth=25, width=80)
                self.all_books_tree_return.column('Book Title', width=150, anchor=W, minwidth=120)
                self.all_books_tree_return.column('Student\'s Name', width=135, anchor=W, minwidth=130)
                self.all_books_tree_return.column('Student\'s Class', width=140, anchor=W, minwidth=100)
                self.all_books_tree_return.column('Date Issued', width=140, anchor=W, minwidth=100)
                self.all_books_tree_return.column('Return Date', width=140, anchor=W, minwidth=100)

                #column headings
                self.all_books_tree_return.heading('#0', text="", anchor=W)
                self.all_books_tree_return.heading('Ascension No', text="Ascension No", anchor=CENTER)
                self.all_books_tree_return.heading('Book Title', text="Book Title", anchor=W)
                self.all_books_tree_return.heading('Student\'s Name', text="Student\'s Name",anchor=W)
                self.all_books_tree_return.heading('Student\'s Class', text="Student\'s Class", anchor=W)
                self.all_books_tree_return.heading('Date Issued', text="Date Issued", anchor=W)
                self.all_books_tree_return.heading('Return Date', text="Return Date", anchor=W)

                self.all_books_tree_return.tag_configure('evenrow', background='lightblue')
                self.all_books_tree_return.tag_configure('oddrow', background='white')
              
                self.all_books_tree_return.place(x=200, y=120, height=340)

                self.return_bt=Button(self.return_books_frame,text='Return',width=15,font=('monospace',16,'bold'), cursor='hand2',command=return_record)
                self.return_bt.place(x=350,y=515)
                self.return_bt.bind('<Return>', return_record)

                self.damaged_bt=Button(self.return_books_frame,text='Add to Damaged',width=15,font=('monospace',16,'bold'), cursor='hand2',command=damaged_books)
                self.damaged_bt.place(x=670,y=515)                

                show_db_return()
        object = returning()
        object.returned()

    def showissuedbooks(self):
        class showissues(main):
            def show_all_issues(self):
                self.show_issued_frame = Frame(root, width=1100, height=1100)
                self.show_issued_frame.place(x=0, y=0)

                self.backbt = ttb.Button(self.show_issued_frame, command=self.MS, cursor="hand2", bootstyle='secondary toolbutton outline')
                self.backbt.place(x=0, y=0)
                self.log = PhotoImage(file='images/back.png')
                self.backbt.config(image=self.log, compound=LEFT)
                self.small_log = self.log.subsample(1, 1)
                self.backbt.config(image=self.small_log)

                self.show_issued_label=ttb.Label(self.show_issued_frame,text='ISSUED BOOKS',font=('monospace', 30,'bold'), bootstyle='primary')
                self.show_issued_label.place(x=480,y=6)

                #Create a treeview to preview the queried database
                def show_issued_db():
                    cursor.execute("SELECT * FROM issues")
                    records = cursor.fetchall()
                    global count
                    count = 0
                    for record in records:
                        if count % 2 == 0:
                            self.issued_books_tree_show.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))     
                        else:
                            self.issued_books_tree_show.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))
                        count += 1

                self.issued_books_tree_show = ttb.Treeview(self.show_issued_frame)
                #defining columns storing names in a tuple
                self.issued_books_tree_show['columns'] = ('Ascension No', 'Book Title', 'Issued To', 'Class', 'Date Issued', 'Return Date')

                #Formatting columns 
                self.issued_books_tree_show.column('#0', width=0, stretch=NO)
                self.issued_books_tree_show.column('Ascension No', anchor=CENTER, minwidth=35, width=80)
                self.issued_books_tree_show.column('Book Title', width=200, anchor=W, minwidth=180)
                self.issued_books_tree_show.column('Issued To', width=180, anchor=W, minwidth=150)
                self.issued_books_tree_show.column('Class', width=150, anchor=W, minwidth=120)
                self.issued_books_tree_show.column('Date Issued', width=150, anchor=W, minwidth=120)
                self.issued_books_tree_show.column('Return Date', width=150, anchor=W, minwidth=120)

                #column headings
                self.issued_books_tree_show.heading('#0', text="", anchor=W)
                self.issued_books_tree_show.heading('Ascension No', text="Ascension No", anchor=CENTER)
                self.issued_books_tree_show.heading('Book Title', text="Book Title", anchor=W)
                self.issued_books_tree_show.heading('Issued To', text="Issued To",anchor=W)
                self.issued_books_tree_show.heading('Class', text="Class", anchor=W)
                self.issued_books_tree_show.heading('Date Issued', text="Date Issued", anchor=W)
                self.issued_books_tree_show.heading('Return Date', text="Return Date", anchor=W)

                self.issued_books_tree_show.tag_configure('evenrow', background='lightblue')
                self.issued_books_tree_show.tag_configure('oddrow', background='white')

                self.issued_books_tree_show.place(x=140, y=120, height=426)
                show_issued_db()
        object = showissues()
        object.show_all_issues()

    def account(self):
        class create_account(main):
            def sign_in(self):
                self.signin_page = Frame(root, width=1100, height=1100)
                self.signin_page.place(x=0, y=0)

                self.signin_frame_box=Frame(self.signin_page,height=350,width=420,bd=3,relief='ridge')
                self.signin_frame_box.place(x=425,y=180)

                self.backbt2 = ttb.Button(self.signin_page, command=self.login_back, cursor="hand2", bootstyle='secondary toolbutton outline')
                self.backbt2.place(x=0, y=0)
                self.log = PhotoImage(file='images/back.png')
                self.backbt2.config(image=self.log, compound=LEFT)
                self.small_log = self.log.subsample(1, 1)
                self.backbt2.config(image=self.small_log)

                self.sign_in_c = ttb.Label(self.signin_page, text='CREATE ACCOUNT', font=('monospace',24,'bold'), bootstyle='primary')
                self.sign_in_c.place(x=440,y=100)

                self.user_label=Label(self.signin_frame_box,text='Master Username',font=('monospace',12,'bold'))
                self.user_label.place(x=10,y=42)

                self.master_username_entry=Entry(self.signin_frame_box,width=22,font=('monospace',11,'bold'))
                self.master_username_entry.place(x=190,y=40)

                self.pass_label=Label(self.signin_frame_box,text='Master Password',font=('monospace',12,'bold'))
                self.pass_label.place(x=10,y=102)

                self.master_password_entry=Entry(self.signin_frame_box,width=22,show='•',font=('monospace',11,'bold'))
                self.master_password_entry.place(x=190,y=100)

                self.new_user_label=Label(self.signin_frame_box,text='New Username',font=('monospace',12,'bold'))
                self.new_user_label.place(x=10,y=162)

                self.new_username_entry=Entry(self.signin_frame_box,width=22,font=('monospace',11,'bold'))
                self.new_username_entry.place(x=190,y=170)

                self.new_pass_label=Label(self.signin_frame_box,text='New Password',font=('monospace',12,'bold'))
                self.new_pass_label.place(x=10,y=222)

                self.new_password_entry=Entry(self.signin_frame_box,width=22,show='•',font=('monospace',11,'bold'))
                self.new_password_entry.place(x=190,y=230)

                self.signin_button=Button(self.signin_frame_box,text=' SIGN IN',width=120,font=('monospace',14,'bold'),
                        command=self.signin_back, relief='flat', cursor='hand2')
                self.signin_button.place(x=145,y=290)
                self.logo = PhotoImage(file='images/user.png')
                self.signin_button.config(image=self.logo, compound=LEFT)
                self.small_logo = self.logo.subsample(1, 1)
                self.signin_button.config(image=self.small_logo)

        object = create_account()
        object.sign_in()

    def signin_back(self):
        self.mas_user_entry = self.master_username_entry.get()
        self.mas_pass_entry = self.master_password_entry.get()
        self.new_user_entry = self.new_username_entry.get()
        self.new_pass_entry = self.new_password_entry.get()

        global cursor
        cursor = db.cursor()
        cursor.execute("SELECT * FROM adm WHERE Username=(?) and Password=(?)", (self.mas_user_entry, self.mas_pass_entry))
        db.commit()
        self.log_check = cursor.fetchone()

        if self.log_check!=None:
            cursor.execute("INSERT INTO adm(Username,Password) values(?,?)", (self.new_user_entry,self.new_pass_entry))
            self.login_back()
            self.master_username_entry.delete(0, END)
            self.master_password_entry.delete(0, END)
            self.new_username_entry.delete(0, END)
            self.new_password_entry.delete(0, END)
        else:
            messagebox.show_error('Master Username or Master Password Enter is incorrect!', 'LBSHS LMS')
            self.master_username_entry.delete(0, END)
            self.master_password_entry.delete(0, END)
            self.new_username_entry.delete(0, END)
            self.new_password_entry.delete(0, END)

    def login_back(self): 
        #LOGIN Frontend
        self.login_frame=Frame(root,height=1100,width=1100)
        self.login_frame.place(x=0,y=0)

        self.login_frame_box=Frame(self.login_frame,height=260,width=360,bd=3,relief='ridge')
        self.login_frame_box.place(x=420,y=200)

        self.login_label = ttb.Label(self.login_frame, text='LOG IN', font=('monospace',24,'bold'), bootstyle='primary')
        self.login_label.place(x=440,y=150)

        self.user_label=Label(self.login_frame_box,text='Username:',font=('monospace',12,'bold'))
        self.user_label.place(x=20,y=42)

        self.username_entry=Entry(self.login_frame_box,width=22,font=('monospace',11,'bold'))
        self.username_entry.place(x=125,y=40)

        self.pass_label=Label(self.login_frame_box,text='Password:',font=('monospace',12,'bold'))
        self.pass_label.place(x=20,y=102)

        self.password_entry=Entry(self.login_frame_box,width=22,show='•',font=('monospace',11,'bold'))
        self.password_entry.place(x=125,y=100)

        self.login_button=Button(self.login_frame_box,text=' LOG IN',width=120,font=('monospace',14,'bold'),
                command=self.login, relief='flat', cursor='hand2')
        self.login_button.place(x=125,y=160)
        self.logo = PhotoImage(file='images/user.png')
        self.login_button.config(image=self.logo, compound=LEFT)
        self.small_logo = self.logo.subsample(1, 1)
        self.login_button.config(image=self.small_logo)
        self.login_button.bind('<Return>', self.login)

        self.create_account_bt = ttb.Button(self.login_frame_box, text='Create a new account', bootstyle="link primary", cursor='hand2', command=self.account)
        self.create_account_bt.place(x=115, y=205)
        
        root.mainloop()

if __name__ == "__main__":
    object = main()
    object.login_back()
db.close()