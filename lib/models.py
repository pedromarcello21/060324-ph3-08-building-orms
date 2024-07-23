############## IMPORTS ##############

# the . stands for our __init__.py
from . import CONN, CURSOR


############## COURSE ##############

class Course:

    def __init__(self, name:str, id:int=None):
        self.name = name
        self.id = id

    def __repr__(self):
        return f"Course(id={self.id}, name={self.name})"

    # --- SQL CLASS METHODS --- #

    @classmethod
    def create_table(cls):
        sql='''CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name TEXT
        )'''

        CURSOR.execute(sql)
        CONN.commit()

    # creates a new instance for each row in the db
    @classmethod
    def get_all(cls):
        sql = '''SELECT * FROM courses'''

        rows = CURSOR.execute(sql).fetchall()

        courses_list = []
        for row_tuple in rows:
            course = Course(id=row_tuple[0], name=row_tuple[1])
            courses_list.append(course)

        return courses_list


    # finds by id and if found instantiates a new instance
    @classmethod
    def get_by_id(cls, id:int):
        sql = '''SELECT * FROM courses WHERE id = ?'''

        row_tuple = CURSOR.execute(sql, [id]).fetchone()

        return Course(id=row_tuple[0], name=row_tuple[1])


    # --- SQL INSTANCE METHODS --- #

    # creates in the db and updates instance with the new id
    def create(self):
        sql = '''INSERT INTO courses (name)
        VALUES (?)'''

        CURSOR.execute(sql, [self.name]) # add
        CONN.commit()

        # GET THE LAST DB ITEM AND GRAB ITS ID
        last_row_sql='''SELECT * FROM courses 
        ORDER BY id DESC LIMIT 1'''

        self.id = CURSOR.execute(last_row_sql).fetchone()[0]

        return self

    # updates the row based on current attributes 
    def update(self):
        sql = '''UPDATE courses
        SET name = ?
        WHERE id = ?'''

        CURSOR.execute(sql, [self.name, self.id])
        CONN.commit()

        return self

    # creates or updates depending on whether item exists in db
    def save(self):
        if self.id: # if I am in the db do this
            self.update()
        else: # if I am not in the db do this
            self.create()
        
    
    # deletes the instance from the db and removes the id
    def destroy(self):
        sql = '''DELETE FROM courses WHERE id = ?'''

        CURSOR.execute(sql, [self.id])
        CONN.commit()

        self.id = None


    # --- JOIN METHODS --- #

    # return a list of instances of each student
    def students(self):
        sql = '''SELECT * FROM students WHERE course_id = ?'''

        bunch_of_student_tuples = CURSOR.execute(sql, [self.id]).fetchall()

        students_list = []
        for row in bunch_of_student_tuples:
            student = Student(id=row[0], name=row[1], grade=row[2], course_id=row[3])
            students_list.append(student)

        return students_list


############## END COURSE ##############



############## STUDENT ##############

class Student:

    def __init__(self, name:str, grade:int, course_id:int, id:int=None):
        self.name = name
        self.grade = grade
        self.id = id
        self.course_id = course_id

    def __repr__(self):
        return f'Student(id={self.id}, name={self.name}, course_id={self.course_id})'
    

    # --- CLASS SQL METHODS --- #

    # make a table if it doesn't exist
    @classmethod
    def create_table(cls):
        pass
        # create table with proper columns if not exists


    # --- SQL METHODS --- #

    def create(self):
        pass
        # add to the database

    def update(self):
        pass
        # update based on current instance attributes

    # remove from the database
    def destroy(self):
        pass
        # destroy row in the db based on id


    # --- SQL CLASS METHODS --- #

    @classmethod
    def get_by_id(cls, id):
        pass
        # find and return instance based on id
        
    # BONUS #
    @classmethod
    def get_by_name(cls, name:str):
        pass
        # find and return instance based on name
    
    @classmethod
    def get_all(cls):
        pass
        # return all instances from the database


    # --- JOIN METHODS --- #

    def course(self):
        pass
        # get the course by course_id


############## END STUDENT ##############