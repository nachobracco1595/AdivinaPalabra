from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QMessageBox
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import bcrypt
import time

import sqlite3
from conexion import *

from Listas_Palabras import *

con = sql_connection()



#-------------------------
# clave1 = b'123456' 
# clave2 = '123456'.encode("utf-8")
# salt = bcrypt.gensalt()
# claveHash = bcrypt.hashpw(clave2,salt)

#VENTANA DE LOGIN.
class vLogin(QMainWindow):    
    def __init__(self):
        super().__init__()
        uic.loadUi("views/V_Login.ui",self)
        self.b_Login.clicked.connect(self.clicked_login)
        self.b_NewA.clicked.connect(self.clicked_register)
        
    def clicked_register(self):
        ventana_login.hide()
        ventana_register.show()

    def clicked_login(self):
        ventana_menu.lb_UserOn.setText(self.le_User.text())
        usr = self.le_User.text()
        pswd = self.le_Password.text()
        res = sql_Login(con, usr, pswd)
        if res == 'OK':
            ventana_login.hide()
            ventana_menu.show()
            ventana_menu.lb_UserOn.setText(self.le_User.text())
            self.le_User.setText('')
            self.le_Password.setText('')            
        elif res == 'FAIL':
            QMessageBox.about(self, "Error!", "Usuario y/o Contraseña invalidos!")
            self.le_Password.setText('')
            print('Error en usuario o password')
    
    def keyPressEvent(self, qKeyEvent):
        print(qKeyEvent.key())
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            self.clicked_login()
            
    
#FIN VENTANA DE LOGIN.

#VENTANA CREAR NUEVO USUARIO.
class vRegister(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("views/V_Register.ui",self)
        self.b_Register.clicked.connect(self.clicked_register)
        self.b_BackLogin.clicked.connect(self.clicked_backLogin)
        
    def clicked_register(self):        
        usr = self.le_User.text()
        pswd = self.le_Password.text()
        if  (3<len(usr)<17) and (3<len(pswd)<17) and (pswd == self.le_ConfirmPass.text() ):
            resRg = sql_insertPlayer(con, usr, pswd)
            if (resRg == 'clon'):
                print('Nombre de usuario ya en uso!')
                QMessageBox.about(self, "Ups!", "Nombre de usuario existente!")
                self.le_User.setText('')
                self.le_Password.setText('')
                self.le_ConfirmPass.setText('')
            else:
                QMessageBox.about(self, "Excelente!", "Usuario creado correctamente!")
                print('Usuario creado correctamente!')
                ventana_register.hide()
                ventana_login.show()
                self.le_User.setText('')
                self.le_Password.setText('')
                self.le_ConfirmPass.setText('')
        else:
            QMessageBox.about(self, "Error!", "Datos ingresados invalidos!")    
            self.le_Password.setText('')
            self.le_ConfirmPass.setText('')
    
    def clicked_backLogin(self):
        ventana_register.hide()
        ventana_login.show()    

#FIN VENTANA CREAR NUEVO USUARIO.

#VENTANA DEL MENU.
class vMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("views/V_Menu.ui",self)
        self.b_Start.clicked.connect(self.clicked_start)#Botón Start te lleva a ventana game.
        self.b_Score.clicked.connect(self.clicked_score)#Botón Score te lleva a ventana score.
        self.b_Logout.clicked.connect(self.clicked_logout)#Botón Logout te lleva a ventana login.
        
        

    #Función del botón Start.
    def clicked_start(self):
        ventana_menu.hide()
        ventana_game.show()
        ventana_game.mostrar_palabra()
        ventana_game.temporizador()

    #Función del botón Score.
    def clicked_score(self):
        ventana_menu.hide()
        ventana_score.actScores()
        ventana_score.show()

            

    #Función del botón Logout.
    def clicked_logout(self):
        ventana_menu.hide()
        ventana_login.show()
       
#FIN VENTANA DEL MENU. 

       
#VENTANA DEL JUEGO.
class vGame(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("views/V_Game.ui",self)
        self.palabra = Palabras()
        self.puntos = 0 #Puntos Score actual en la partida.
        self.vidas = 3 #Total de vidas de la partida.
        self.count = 0 #Acumulador que suma 1 cada segundo.
        #---------------------------------------------
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.temporizador)
        #---------------------------------------------
        self.b_Intentar.clicked.connect(self.clickled_intentar)#Botón Intentar de momento te lleva directo a ventana endgame.
        self.lb_Msg.setText("")
        self.b_Finalizar.clicked.connect(self.finalizar) #Boton para finalizar el juego antes de lo provisto.

    def finalizar(self):
        self.timer.stop()#Detiene el tiempo. 
        self.count = 0 #El contador se regresa a 0.
        self.puntos = 0 #El contador de puntos regresa a 0.
        self.vidas = 3
        self.lb_Vida1.setText("♥")
        self.lb_Vida2.setText("♥")
        self.lb_Vida3.setText("♥")
        ventana_game.hide()
        ventana_menu.show()

    #Función del botón Intentar.
    def clickled_intentar(self):
        if self.palabra.p_elegida == self.le_Palabra.text().lower():
            self.count = 0 #El contador se regresa a 0.
            self.mostrar_palabra()
            self.temporizador()
            self.puntos += 10 #Suma 10 puntos.
            self.lb_ScoreActual.setText(str(self.puntos))
        else:
            self.lb_Msg.setText("Incorrecto!!!") #Muestra un mensaje cuando fallas la palabra.

        self.le_Palabra.setText('')
        self.le_Palabra.setFocus()
    
    def keyPressEvent(self, qKeyEvent):
        print(qKeyEvent.key())
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            self.clickled_intentar()
    
    #Función para mostrar la palabra desordenada en la ventana.
    def mostrar_palabra(self):
        self.lb_Msg.setText("")
        self.palabra.elegir_palabra(self.puntos) #Elige una palabra.
        self.palabra.desordenar_palabra() #Desordena la palabra
        self.lb_MessyWord.setText(self.palabra.p_desordenada.upper()) #Muestra la palabra en el label
        self.lb_CorrectWord.setText(self.palabra.p_elegida.upper()) #Muestra la palabra en el label
        self.lb_ScoreActual.setText(str(self.puntos))

    
    #Función que maneja el tiempo limite del juego.
    def temporizador(self):
        self.timer.start(1000)#Inicia el tiempo.
        self.lcd_Time.display(20 - self.count)
        #Cuando el tiempo llega a 0 te manda a la ventana endgame.     
        if self.count == 20:
            if self.vidas == 3:
                self.count = 0 #El contador se regresa a 0.
                self.lb_Vida3.setText("-")
                self.vidas -= 1 #Resta una vida
            elif self.vidas == 2:
                self.count = 0 #El contador se regresa a 0.
                self.lb_Vida2.setText("-")
                self.vidas -= 1 #Resta una vida
            elif self.vidas == 1:
                self.count = 0 #El contador se regresa a 0.
                self.lb_Vida1.setText("-")
                self.vidas -= 1 #Resta una vida
            else:
                self.timer.stop()#Detiene el tiempo. 
                score = str(self.puntos)
                ventana_endgame.lb_Score.setText(score)
                jugador = ventana_menu.lb_UserOn.text()
                sql_insert(con, jugador, int(self.puntos))
                self.count = 0 #El contador se regresa a 0.
                self.puntos = 0 #El contador de puntos regresa a 0.
                self.vidas = 3
                self.lb_Vida1.setText("♥")
                self.lb_Vida2.setText("♥")
                self.lb_Vida3.setText("♥")
                ventana_game.hide()
                ventana_endgame.show()
                ventana_score.actScores()
                
        else:
            self.lcd_Time.display(20 - self.count)
            self.count += 1 #Se incrementa el contador.


#FIN VENTANA DEL JUEGO.


#VENTANA FIN DEL JUEGO.
class vEndGame(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("views/V_Endgame.ui",self)
        self.b_PlayAgain.clicked.connect(self.clicked_playagain)#Botón Play Again te lleva a ventana game.
        self.b_Back.clicked.connect(self.clicked_back)#Boton Back to Menu te lleva a ventana menu.
        #(cancelado por edición xD)
        #self.lbRecord.hide()

    #Función del botón Play Again.
    def clicked_playagain(self):
        ventana_endgame.hide()
        ventana_game.show()
        ventana_game.mostrar_palabra()
        ventana_game.temporizador()

    #Función del botón Back to Menu de la ventana endgame.
    def clicked_back(self):
        ventana_endgame.hide()
        ventana_menu.show()
    
    

#FIN VENTANA FIN DEL JUEGO.


#VENTANA DE PUNTUACIONES.
class vScore(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("views/V_Score.ui",self)
        self.b_Back.clicked.connect(self.clicked_back)#Botón Back to Menu te lleva a ventana menu.
        #self.actScores()
        

    def actScores(self):
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM score ORDER BY puntaje DESC LIMIT 3')
        self.bestScores = cursorObj.fetchall()     
        if(len(self.bestScores) == 1):            
            self.lb_Player1.setText(str(self.bestScores[0][1]))
            self.lb_Score1.setText(str(self.bestScores[0][2]))
        elif(len(self.bestScores) == 2):
            self.lb_Player1.setText(str(self.bestScores[0][1]))
            self.lb_Score1.setText(str(self.bestScores[0][2]))              
            self.lb_Player2.setText(str(self.bestScores[1][1]))
            self.lb_Score2.setText(str(self.bestScores[1][2]))
        elif(len(self.bestScores) == 3):
            self.lb_Player1.setText(str(self.bestScores[0][1]))
            self.lb_Score1.setText(str(self.bestScores[0][2]))
            self.lb_Player2.setText(str(self.bestScores[1][1]))
            self.lb_Score2.setText(str(self.bestScores[1][2]))               
            self.lb_Player3.setText(str(self.bestScores[2][1]))
            self.lb_Score3.setText(str(self.bestScores[2][2]))   
            
    #Función del botón Back to Menu de la ventana score.
    def clicked_back(self):
        ventana_score.hide()
        ventana_menu.show()

#FIN VENTANA DE PUNTUACIONES. 
       


  


app = QApplication([])


ventana_login = vLogin() #Ventana Principal de la aplicación.
ventana_register = vRegister() #Ventana para registrar usuario
ventana_menu = vMenu() #Ventana del Menu de la aplicación.
ventana_game = vGame() #Ventana Juego Iniciado.
ventana_endgame = vEndGame() #Ventana Fin del Juego.
ventana_score = vScore() #Ventana de Puntuaciones.

ventana_login.show()

app.exec_()