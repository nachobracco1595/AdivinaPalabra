import random

class Palabras:

    def __init__(self):

        self.p_elegida = ""
        self.p_desordenada = ""

        self.l_facil = ["perro","gato","ratón","casa","auto","avión","árbol","flor","abeja","clavo","vaso",
        "rojo","azul","taza","mano","mono","león","pie","hola","ala","lápiz","goma","pelo","pala","gorro"]

        self.l_normal = ["pelota","lápida","escalera","rodilla","sillón","tejado","pantalla","monitor",
        "elefante","jirafa","ventana","edificio","bebida","alcohol","enfermero","cuchillo","cuchara","tenedor",
        "caballo","amarillo","morado","costilla","ensalada","tiburón","gabinete"]

        self.l_dificil = ["electrónico","electricidad","murcielago","hipopotamo","rinoceronte","motocicleta",
        "paracaídas","constitución","argentina","cartuchera","telaraña","circunferencia","holograma","almohada",
        "cumpleaños","asteroide","tecnología","puercoespin","ornitorrinco","calculadora","computadora",
        "descampado","ventilador","ingeniería","astronauta",]
    
    def __str__(self):
        return '{0} - {1}'.format(self.p_elegida,self.p_desordenada)

    def elegir_palabra(self,num):
        #Mientras mas alto sea el score de la partida mayor dificultad en las palabras que aparecen.
        if num > 200:
            self.p_elegida = random.choice(self.l_dificil)
        elif num > 100:
            self.p_elegida = random.choice(self.l_normal)
        else:
            self.p_elegida = random.choice(self.l_facil)
        #-------------------------------------------------------------------------------------------
        self.p_desordenada = self.p_elegida
        #return self.p_elegida

    def desordenar_palabra(self):
        #While que verifica que si la p_desordenada es igual a p_elegida vuelve a desordenar.
        while self.p_desordenada == self.p_elegida:
            aux = random.sample(self.p_elegida,len(self.p_elegida))
            self.p_desordenada = ''.join(aux)
        #------------------------------------------------------------------------------------
        #return self.p_desordenada
    


#pal = Palabras()
#pal.elegir_palabra()
#pal.desordenar_palabra()
#print(pal)
