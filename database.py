import sqlite3

class DataBase:
    def __init__(self):
        self.data = "music_meta.sqlite"
        self.connection = sqlite3.connect(self.data)
        self.cursor = self.connection.cursor()
        
        '''
        drop_table_query = "DROP TABLE IF EXISTS songs"
        self.cursor.execute(drop_table_query)
        self.connection.commit()
        '''

        create_table_query = "CREATE TABLE IF NOT EXISTS songs(\
                                nid INTEGER, Name TEXT,\
                                Lyrics TEXT, Author TEXT)"
        self.cursor.execute(create_table_query)
        self.connection.commit()
        
    def addItem(self, item):
        self.cursor.execute("INSERT INTO songs VALUES (?, ?, ?, ?)", item)
        self.connection.commit()
        
    def searchItem(self, item, form):
        query = f"SELECT * FROM songs WHERE {item} = '{form}';"
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        return row
        
    def getLength(self):
        query = "SELECT * FROM songs"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return len(result)
        
    def abort(self):
        self.cursor.close()
        self.connection.close()
        
#print(DataBase().searchItem("Name", "Name"))