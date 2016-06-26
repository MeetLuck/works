from Tkinter import *
import ttk
root = Tk()
tree = ttk.Treeview(root)

#----------- style--------------
style = ttk.Style(root)
style.configure('Treeview', rowheight=20, background='yellow',relief='flat', borderwith=4)

#---------- columns #0, 1, 2, 3, ... -----------------------
tree['columns'] = ('one','two')
tree.column('one', width=100)
tree.column('two', width=100)

#---------- columns heading #0, 1, 2, 3, ... ---------------
tree.heading('#0', text='column #0')
tree.heading('one', text = 'column one')
tree.heading('two', text = 'column two')

#------------- insert at root -----------------------------
### row 0 -> Line1      1A      1B     ###
tree.insert('', 0, text='Line 1', values = ('1A','1B'),tags='T' )
### row 1 -> Dir2                      ###
id2 = tree.insert('',1,'dir2', text = 'Dir2', tags='T')
### id2 -> sub dir2      2A      2B    ###
tree.insert(id2, 'end', text='sub dir2 ', values = ('2A','2B') )
## alternatively
### row2 ->  dir3
### dir3 ->  sub dir3      3A    3B   ###
tree.insert('',2,'dir3',text='dir3')
#tree.insert('',3,'dir3', text='dir3')
tree.insert('dir3',3,text='sub dir3', values =('3A','3B') )

#-------------- tree.tag_configure ---------------------------
tree.tag_configure('T',font='Arial 10')
tree.pack()
root.mainloop()
