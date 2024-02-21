# DB class connection
import sqlite3

class Connection:

    def __init__(self):
        self.conn = self.connection()
        

    def connection(self):
        try:
            connection = sqlite3.connect('db_project.db')
            return connection
        except sqlite3.Error as error:
            # Handle errors from interface of the application
            return error
    
    def query_sets(self,query):
        try:
            cursor = self.conn.cursor()
            result = cursor.execute(query).fetchall()
            return result
        except Exception as error:
            # Handle errors
            return error
    
    def insert_item(self,data_sets):
        try:
            query = 'INSERT INTO products (name,price) VALUES (?,?)'
            cursor = self.conn.cursor()
            cursor.execute(query,data_sets)
            self.conn.commit()
            return True
        except sqlite3.Error as error:
            return error
            
    def delete_item(self,name):
        query = 'DELETE FROM products WHERE name = ?'
        try:
            cursor = self.conn.cursor()
            cursor.execute(query,(name,))
            self.conn.commit()
        except sqlite3.Error as error:
            return error

    def edit_item(self,new_name,name,new_price,price):

        query = 'UPDATE products SET name =?, price = ? WHERE name = ? and price = ? '
        parameters = (new_name,new_price,name,price)
        cursor = self.conn.cursor()
        cursor.execute(query,parameters)
        self.conn.commit()

        
if __name__ == '__main__':
    test = Connection()
    #result = test.insert_data(['tablet_gx14',100])
    #print(result)