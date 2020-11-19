import sqlite3 as sql
import os
import Logger as log


class User:

    idteleg = "none"
    course = "none"
    direction = "none"
    role = "user"
    namebook = "none"
    filename = "none"
    path = "none"
    course = "none"
    direction = "none"
    books = []
    clients = None
    database = None

    def __init__(self, id):
        self.idteleg = str(id)
        self.clients = Clients()
        self.database = Database()
        if(self.clients.IsInBase(id)):
            data = self.clients.FindByid(self.idteleg)
            self.course = data[0][0]
            self.direction = data[0][1]
            self.role = data[0][2]

    def Direction(self, direction):
        self.direction = direction
    
    def Course(self, course):
        self.course = course  

    def ReturnAllBooks(self):
        user = self.clients.FindByid(self.idteleg)
        self.books = self.database.OpenBooks(user[0][0],user[0][1])
        return self.books

    def ReturnBook(self, idbook):
        return self.books[idbook]
    
    def SaveClient(self):
        if(not self.clients.IsInBase(self.idteleg)):
            self.clients.AppendToTable(self.idteleg)
        self.clients.ApdateCourse(self.idteleg,self.course)
        self.clients.ApdateDirection(self.idteleg,self.direction)
        self.clients.ApdateRole(self.idteleg,self.role)

    def IsInBase(self, id):
        return self.clients.IsInBase(id)
        
    def IsAdmin(self):
        return (self.role == "admin")

    def CreateBook(self, filename, path):
        self.filename = filename
        self.path = path

    def AppendNamebook(self, namebook):
        self.namebook = namebook
    
    def AppendCourse(self, course):
        self.course = course

    def AppendCourse(self, direction):
        self.direction = direction

    def SaveBook(self):
        if(self.IsAdmin()):
            if(not self.database.IsInBase(self.filename)):
                self.database.AppendToTable(self.namebook,self.path,self.filename,self.course,self.direction)
            else:
                self.database.UpdateCourse(self.course)
                self.database.UpdateDirection(self.direction)
            return True
        else:
            return False

    def ChangeRole(self,idteleg, role):
        if(self.IsAdmin()):
            self.clients.ApdateRole(idteleg,role)
            return True
        else:
            return False

    def DeleteBook(self, idbook):
        if(self.IsAdmin()):
            self.database.DeleteFromTable(idbook)
            return True
        else:
            return False

class Clients:
    
    connection = None 

    def __init__(self):
        try:
            if(not os.path.exists('databases\\users.db')):
                self.connection = sql.connect('databases\\users.db')
                cur = self.connection.cursor()
                cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, idtel STRING, course STRING, direction STRING, role STRING);')
                self.connection.commit()
            else:
                self.connection = sql.connect('databases\\users.db')
        except Exception as ex:
            log.WriteLog(ex,'users.db')

    def IsInBase(self, id):
        try:
            cur = self.connection.cursor()
            cur.execute('SELECT course, direction FROM users WHERE idtel = ?;',(str(id).lower(),))
            data = cur.fetchall()
            if(len(data)>0):
                return(True)
            else:
                return(False)
        except Exception as ex:
            log.WriteLog(ex, id)
            return(False)

    def FindByid(self, id):
        try:
            cur = self.connection.cursor()
            cur.execute('SELECT course, direction, role FROM users WHERE idtel = ?;',(str(id).lower(),))
            data = cur.fetchall()
            return(data)
        except Exception as ex:
            log.WriteLog(ex, id)
            return([])

    def AppendToTable(self, id):
        try:
            cur = self.connection.cursor()
            cur.execute('INSERT INTO users (idtel) VALUES ( ? );',(str(id).lower(),))
            self.connection.commit()
            return(True)
        except Exception as ex:
            log.WriteLog(ex,id)
            return(False)

    def ApdateCourse(self, id,newcourse):
        try:
            cur = self.connection.cursor()
            cur.execute('UPDATE users SET course = ? WHERE idtel = ?;',(newcourse.lower(),str(id).lower()))
            self.connection.commit()
            return(True)
        except Exception as ex:
            log.WriteLog(ex,str(id)+":"+newcourse)
            return(False)

    def ApdateDirection(self, id, newdirection):
        try:
            cur = self.connection.cursor()
            cur.execute('UPDATE users SET direction = ? WHERE idtel = ?;',(newdirection.lower(),str(id).lower()))
            self.connection.commit()
            return(True)
        except Exception as ex:
            log.WriteLog(ex,str(id)+":"+newdirection)
            return(False)

    def ApdateRole(self, id, role):
        try:
            cur = self.connection.cursor()
            cur.execute('UPDATE users SET role = ? WHERE idtel = ?;',(role.lower(),str(id).lower()))
            self.connection.commit()
            return(True)
        except Exception as ex:
            log.WriteLog(ex,str(id)+":"+role)
            return(False)

    def DeleteFromTable(self, id):
        try:
            cur = self.connection.cursor()
            cur.execute('DELETE FROM users WHERE idtel = ?;',(str(id).lower(),))
            self.connection.commit()
            return(True)
        except Exception as ex:
            log.WriteLog(ex,id)
            return(False)
        
        
class Database:

    connection = None

    def __init__(self):
        try:
            if(not os.path.exists('databases\\DataAboutFiles.db')):
                self.connection = sql.connect('databases\\DataAboutFiles.db')
                cur = self.connection.cursor()
                cur.execute('CREATE TABLE DataAboutFiles (id INTEGER PRIMARY KEY AUTOINCREMENT, namebook STRING, path STRING, filename STRING, course STRING, direction STRING);')
                self.connection.commit()   
            else:
                self.connection = sql.connect('databases\\DataAboutFiles.db')
        except Exception as ex:
            log.WriteLog(ex,'DataAboutFiles.db')
        
    def AppendToTable(self, namebook, filepath, filename, course, direction):
        try:
            cur = self.connection.cursor()
            cur.execute('INSERT INTO DataAboutFiles ( namebook, path, filename, course, direction ) VALUES ( ?, ?, ?, ?, ?);',(namebook.lower(),filepath.lower(),filename.lower(),course.lower(),direction.lower()))
            self.connection.commit()
            return(True)
        except Exception as ex:
            log.WriteLog(ex,namebook+":"+filepath+":"+course+":"+direction)
            return(False)

    def DeleteFromTable(self, id):
        try:
            book = self.ReturnBook(id)
            if(len(book)>0):
                os.remove(book[0][2])
                cur = self.connection.cursor()
                cur.execute('DELETE FROM DataAboutFiles WHERE id = ?;',(str(id).lower(),))
                self.connection.commit()
            return(True)
        except Exception as ex:
            log.WriteLog(ex,id)
            return(False)

    def IsInBase(self,filename):
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT id, namebook, path, FROM DataAboutFiles WHERE  filename = ?;",(filename.lower(),))
            data = cur.fetchall()
            if(len(data)>0):
                return (True)
            else:
                return (False)
        except Exception as ex:
            log.WriteLog(ex,filename)
            return(False)

    def ReturnBook(self,id):
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT id, namebook, path, filename, course, direction FROM DataAboutFiles WHERE  id = ?;",(str(id).lower(),))
            data = cur.fetchall()
            return (data)
        except Exception as ex:
            log.WriteLog(ex,id)
            return([])

    def OpenBooks(self, course, direction):
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT id, namebook, path, filename FROM DataAboutFiles WHERE  course = ? AND direction = ?;",(course.lower(),direction.lower()))
            data = cur.fetchall()
            return (data)
        except Exception as ex:
            log.WriteLog(ex,course+":"+direction)
            return([])

    def UpdateCourse(self, id, newcourse):
        try:
            cur = self.connection.cursor()
            cur.execute('UPDATE DataAboutFiles SET course = ? WHERE id = ?;',(newcourse.lower(),str(id).lower()))
            self.connection.commit()
            return(True)
        except Exception as ex:
            log.WriteLog(ex, newcourse)
            return(False)

    def UpdateDirection(self, id, newdirection):
        try:
            cur = self.connection.cursor()
            cur.execute("UPDATE DataAboutFiles SET direction = ? WHERE id = ?;",(newdirection.lower(),str(id).lower()))
            self.connection.commit()
            return(True)
        except Exception as ex:
            log.WriteLog(ex,newdirection)
            return(False)