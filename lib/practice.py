from . import CONN, CURSOR

## Movie class ##
class Movie:
    def __init__(self, title:str, year:int, id:int=None):
        self.id = id
        self.title = title
        self.year = year

    def __repr__(self):
        return f'Movie(id={self.id}, title={self.title}, year={self.year})'


    # --- SQL CLASS METHODS --- #

    @classmethod
    def create_table(cls):
        sql = '''CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            name TEXT
        )'''

        CURSOR.execute(sql) #Executes the sql statement
        CONN.commit() #makes that change to the db file
        
        # creates the table if it doesn't exist

    @classmethod
    def get_all(cls):
        sql = """SELECT * FROM movies"""

        rows = CURSOR.execute(sql).fetchall()
        movie_list = []
        for row_tuple in rows:
            movie = Movie(id={row_tuple[0]}, title=row_tuple[1], year=row_tuple[2])
            movie_list.append(movie)
        return movie_list
        
        # creates a new instance for each row in the db

    @classmethod
    def get_by_id(cls, id:int):
        sql = """SELECT * FROM movies WHERE id = ?"""

        row_tuple = CURSOR.execute(sql, [id]).fetchone()
        print(row_tuple)

        return Movie(id=row_tuple[0], title=row_tuple[1])
        
        # finds by id and if found instantiates a new instance


    # --- SQL INSTANCE METHODS --- #

    def create(self):
        sql = """INSERT INTO movies (name, year) VALUES (?, ?)"""
        CURSOR.execute(sql, [self.title, self.year]) ##executes the sql 
        CONN.commit()#Adds to db

        #need to give id in instance
        last_row_sql = """SELECT * FROM movies ORDER BY id DESC LIMIT 1"""
        self.id = CURSOR.execute(last_row_sql).fetchone()[0]

        return self
        
        # creates in the db and updates instance with the new id


    def update(self):
        sql = """UPDATE movies 
        SET name = ? 
        WHERE id = ?"""
        CURSOR.execute(sql, [self.title, self.id])
        CONN.commit()
        
        return self
        # updates the row based on current attributes 


    def save(self):
        if self.id:
            self.update()
        else:
            self.create()
        pass
        # creates if it doesn't exist
        # updates if it does exist

    
    def destroy(self):
        sql = """DELETE FROM movies WHERE id = ?"""

        CURSOR.execute(sql, [self.id])
        CONN.commit()
        
        self.id = None
        # deletes the instance from the db and removes the id