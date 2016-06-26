from Tkinter import *
import ttk
import sqlite3

def execute_db_query(query,paremeters ):
    with sqlite3.connect('phonebook.db') as conn:
        cursor = conn.cursor()
        if paremeters: #print 'with param'
            query_result = cursor.execute(query, paremeters)
        else:# print 'no param'
            query_result = cursor.execute(query)
        conn.commit()
#       cursor.close()
    return query_result

class PhoneBook:
    def __init__(self, parent):
        photo = PhotoImage( file = 'icons/phonebookicon.gif')
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=0)

        fr = LabelFrame(parent, text='Create New Record')
        fr.grid(row=0,column=1, padx=8, pady=8, sticky='ew')
        
        Label(fr, text='Name:').grid(row=1, column=1, sticky=W, pady=2)
        self.name = StringVar()
        self.namefield = Entry(fr, textvariable = self.name)
        self.namefield.grid(row=1, column=2, sticky=W, padx=5, pady=2)

        Label(fr, text='Contact Number:').grid(row=2, column=1, sticky=W, pady=2)
        self.number = IntVar()
        self.numberfield = Entry(fr, textvariable= self.number)
        self.numberfield.grid(row=2, column=2, sticky=W, padx=5, pady=2)
        ttk.Button(fr, text='Add Record', command=self.create_record).grid(row=3,column=2,
                sticky=W, padx=5, pady=2)

        showbtn = ttk.Button(text='Show Records', command=self.view_records)
        showbtn.grid(row=3,column=0, sticky=W)

        self.msg = Label(text='', fg='red')
        self.msg.grid(row=3,column=1,sticky=W)
        
        #--------------- Treeview -----------------------
        self.tree = ttk.Treeview(height=5, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Name', anchor=W)
        self.tree.heading(2, text='Phone Number', anchor=W)

        #---------------- delete button ------------------
        delbtn = ttk.Button(text='Delete Selected', command = self.delete_record)
        delbtn.grid(row=5, column=0, sticky=W)

        #---------------- update button ------------------
        updatebtn = ttk.Button(text='Modify Selected', command = self.open_modify_window)
        updatebtn.grid(row=5,column=1,sticky=W)

        query = '''CREATE TABLE IF NOT EXISTS contacts(
        contactid INTEGER PRIMARY KEY AUTOINCREMENT,
        name STRING NOT NULL,
        contactnumber INTEGER NOT NULL
        ) '''
        execute_db_query(query,None )

    def create_record(self):
        name = self.namefield.get()
        number = self.numberfield.get()
        if name =='':
            self.msg['text'] = 'Please Enter name'
            return
        if number =='':
            self.msg['text'] = 'Please Enter Number'
            return

        query = 'INSERT INTO contacts VALUES(NULL,?,?)'
        parameters =  (name, number)
        execute_db_query(query, parameters)

        self.namefield.delete(0,END)
        self.numberfield.delete(0,END)
        self.msg['text'] = 'Phone Record of %s added' % name
        self.view_records()
    def view_records(self):
        x = self.tree.get_children()
        for item in x:
            print item
            self.tree.delete(item)
        query = 'select * from contacts'
        list = execute_db_query(query,None)
        for row in list:
            print row
            self.tree.insert('', 0, text=row[1], values=row[2] )

    def delete_record(self):
        self.msg['text'] = ''
        query = "DELETE FROM contacts WHERE name = ?"
        name =  self.tree.item(self.tree.selection() )['text']
        execute_db_query(query,(name,) )
        self.msg['text'] = 'Phone Record fo %s Deleted' % name
        self.view_records()

    def open_modify_window(self):
        try:
            self.msg['text'] = ''
            name = self.tree.item(self.tree.selection())['text']
            oldphone = self.tree.item(self.tree.selection())['values'][0]

            self.tl = Tk()
            Label(self.tl, text = 'Name: ').grid(row=0, column=1,sticky=W)
            ne = Entry(self.tl)
            ne.grid(row=0, column=2, sticky=W)
            ne.insert(0, name)
            ne.config(state='readonly')

            Label(self.tl, text='Old Phone Number:').grid(row=1, column=1, sticky=W)
            ope = Entry(self.tl)
            ope.grid(row=1, column=2, sticky=W)
            ope.insert(0, str(oldphone) )
            ope.config(state='readonly')

            Label(self.tl, text='New Phone Number:').grid(row=2, column=1, sticky=W)
            newph = StringVar()
            newphe = Entry(self.tl, textvariable= newph)
            newphe.grid(row=2, column=2, sticky=W)

            updatebtn = Button(self.tl, text='Update Record', 
                    command = lambda:self.update_record(newphe.get(), oldphone, name) )
            updatebtn.grid(row=3, column=2, sticky=W)
            self.tl.mainloop()
        except IndexError as e:
            self.msg['text'] = 'Please Select Item to Modify'

    def update_record(self, newphone, oldphone, name):
        query = "UPDATE contacts SET contactnumber = ? WHERE contactnumber = ? AND name = ?"
        parameter = (newphone, oldphone, name)
        execute_db_query(query, parameter)
        self.tl.destroy()
        self.msg['text'] = 'Phone Number of %s modified' % name
        self.view_records()

root = Tk()
app = PhoneBook(root)
root.mainloop()






