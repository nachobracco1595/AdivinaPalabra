import sqlite3
import bcrypt

from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect('database/database.db')
        print("Conexion correcta database")
        return con
    except Error:
        print(Error)
    #finally:
    #    con.close()



def sql_tables(con):
    print('Generando tablas y preparando primer usuario!')    
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS jugadores(id integer PRIMARY KEY, nombre text, pswd text)")    
    cursorObj.execute("CREATE TABLE IF NOT EXISTS score(id integer PRIMARY KEY, jugador text, puntaje integer)")
    con.commit()
    print('Tablas agregadas correctamente!')



def sql_Login(con, usr, pswd):     #datos
    msj = 'FAIL'
    pswd = pswd.encode('utf-8')
    cursorObj = con.cursor()     
    cursorObj.execute('SELECT * FROM jugadores WHERE nombre = ?', [usr])
    jugador = cursorObj.fetchall()
    print('1')
    print(jugador)
    if jugador:
        print('2')
        print(jugador)      
        if bcrypt.checkpw(pswd,jugador[0][2].encode('utf-8')):
            msj = 'OK'      
            print("La contraseña coincide")
            return msj
        else:
            print("La contraseña no coincide")
            return msj
    else:
        print('3')
        print(jugador)
        msj = 'FAIL'        
        print("Jugador inexistente")
        return msj

def sql_insert(con, jugador, score):   
    cursorObj = con.cursor()    
    cursorObj.execute('INSERT INTO score (jugador, puntaje) VALUES(?,?)', (jugador, score))    
    con.commit()
    print('datos de ingresados correctamente!')

def sql_insertPlayer(con, usr, pswd):
    msj = 'OK'
    if (len(usr)>0) and (len(pswd)>0): 
        cursorObj = con.cursor()    
        cursorObj.execute('SELECT * FROM jugadores WHERE nombre = ?', [usr])
        if cursorObj.fetchall():
            print('El nombre de usuario ya existe! Por favor pruebe con otro.')
            msj = 'clon'
            return msj 
        else:
            pswd = pswd.encode('utf-8')
            salt = bcrypt.gensalt()
            claveHash = bcrypt.hashpw(pswd,salt)
            cursorObj.execute('INSERT INTO jugadores (nombre, pswd) VALUES(?,?)', (usr,claveHash.decode('utf-8')) )    
            con.commit()
            print('datos ingresados correctamente!')     
    else:
        print('Debe ingresar datos para almacenar!')

con = sql_connection()
sql_tables(con)
#sql_insert(con)
#sql_insertPlayer(con)