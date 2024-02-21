# Product class
from tkinter import ttk
from tkinter import *
# Import the module connection
from db import Connection

class Product:

    def __init__(self,window):
        self.wind = window
        self.wind.title('Product Management')
        self.connect = Connection() # Inicia la conexion a la db

        # Container
        frame = LabelFrame(self.wind,text= "Register Product")
        frame.grid(row=0,column=0,columnspan=3,pady=20)
        
        # Name input
        Label(frame,text="Name: ").grid(row=1,column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1,column=1)

        # Price Input
        Label(frame,text="Price: ").grid(row=2,column=0)
        self.price = Entry(frame,)
        self.price.grid(row=2,column=1)

        # Button add product
        ttk.Button(frame,text='Save product', command=self.add_product).grid(row=3, column=1,sticky= W+E)
        
        # Output Messages
        self.message = Label(text='',fg='red')
        self.message.grid(column=0,row=3,columnspan=2,sticky=W+E)
        
        # Table
        self.tree = ttk.Treeview(height=10,columns=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0',text='Name',anchor=CENTER)
        self.tree.heading('#1',text='Price',anchor=CENTER)

        # Buttons
        ttk.Button(frame,text='DELETE',command=self.delete_product).grid(row=5,column=0,sticky=W+E)
        ttk.Button(frame,text='EDIT',command=self.edit_product).grid(row=5,column=1,sticky=W+E)

        # Filling the rows
        self.get_products()

    def get_products(self):
        # List all products in the table

        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        db_rows = self.connect.query_sets('SELECT * FROM products ORDER BY id DESC')
        for row in db_rows:
            self.tree.insert('',0,text=row[1],values = row[2])
    
    def add_product(self):
        if self.validation():
            # True
            result = self.connect.insert_item([self.name.get(),self.price.get()])
            self.message['text'] = "Succes Load" if result == True else result
            self.name.delete(0,END)
            self.price.delete(0,END)
            self.get_products()

        else: 
            # False
            self.message['text'] = 'Name Product or Price are empty'

    def edit_product(self):
        # edit product
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as error:
            self.message['text'] = 'Please select a record'
            return
        

        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_window = Toplevel()
        self.edit_window.title = 'Edit Product'

        # Old Name
        Label(self.edit_window,text='Old Name:').grid(row=0,column=1)
        Entry(self.edit_window,textvariable=StringVar(self.edit_window,value=name),state='readonly').grid(row=0,column=2)

        # New Name
        Label(self.edit_window,text='New Name').grid(row=1,column=1)
        new_name = Entry(self.edit_window)
        new_name.grid(row=1,column=2)

        #Old Price
        Label(self.edit_window,text='Old Price').grid(row=2,column=1)
        Entry(self.edit_window,textvariable=StringVar(self.edit_window,value=old_price),state='readonly').grid(row=2,column=2)

        # New Price
        Label(self.edit_window,text='New Price').grid(row=3,column=1)
        new_price = Entry(self.edit_window)
        new_price.grid(row=3,column=2)

        # Button save edit items
        Button(self.edit_window,text='Update Data',command= lambda: self.update_item(new_name.get(),name,new_price.get(),old_price)).grid(row=4,column=2,sticky=W)
    
    
    def update_item(self,new_name,name,new_price,price):
        self.connect.edit_item(new_name,name,new_price,price)
        self.edit_window.destroy()
        self.message['text'] = f'Record {name} update successfylly'
        self.get_products()
        pass

    def delete_product(self):
        # Delete product
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as error:
            self.message['text'] = 'Please select a record'
            return error

        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        self.connect.delete_item(name)
        self.message['text'] = f'Deleted { name } successfully '
        self.get_products()
        
    def validation(self):
        return True if len(self.name.get()) != 0 and len(self.price.get()) != 0 else False




# Testing class
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
    