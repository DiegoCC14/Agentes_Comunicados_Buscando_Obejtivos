import random , time , os

import Escenario as Escenario_py


# Agentes Informados que se comunican

class Agente():
	
	def __init__( self , tupla_pos_inicial , obj_tablero , simbolo_representativo ):
		
		self.x = tupla_pos_inicial[0]
		
		self.y = tupla_pos_inicial[1]
		
		self.simbolo_representativo = simbolo_representativo

		self.obj_tablero = obj_tablero

		obj_tablero.ingresa_objeto_a_tablero( tupla_pos_inicial , simbolo_representativo )


	def mover_agente( self , tupla_new_posicion ):
		self.obj_tablero.borrar_casilla_tablero( ( self.x , self.y ) )
		self.obj_tablero.ingresa_objeto_a_tablero( tupla_new_posicion , self.simbolo_representativo )
		self.x = tupla_new_posicion[0]
		self.y = tupla_new_posicion[1]


	def obtiene_valor_de_casillas_alcanzables_de_agente( self ):
		#El agente solo podra alcanzar los casillas continuas a la actual
		dicc_valor_casillas = {}
		for num_columna in [-1,0,1] :
			for num_fila in [-1,0,1] :
				if not( num_columna == 0 and num_fila == 0 ) :
					tupla = ( self.x+num_columna , self.y+num_fila )
					
					if (tupla[0] >=0) and (tupla[1] >=0) and (tupla[0] <= self.obj_tablero.size-1) and (tupla[1] <= self.obj_tablero.size-1) :
						valor_casilla = self.obj_tablero.obtener_valor_de_casilla( tupla )
						dicc_valor_casillas[ tupla ] = valor_casilla

		return dicc_valor_casillas


class Agente_Escapando( Agente ):
	
	def __init__( self , tupla_pos_inicial , obj_tablero ):
		Agente.__init__( self , tupla_pos_inicial , obj_tablero , "A" )
		self.generando_ruido_en_casillas_continuas()

	def generando_ruido_en_casillas_continuas( self ):
		dicc_casillas_continuas = self.obtiene_valor_de_casillas_alcanzables_de_agente()
		for tupla_pos,valor in dicc_casillas_continuas.items():
			if valor == "[ ]":
				self.obj_tablero.ingresa_objeto_a_tablero( tupla_pos , "R")


class Agente_Buscador( Agente ):
	
	def __init__( self , tupla_pos_inicial , obj_tablero , Simbolo_Objetivo ,ubicasion_agente_buscado=None):
		
		Agente.__init__( self , tupla_pos_inicial , obj_tablero , "Z" )
		
		self.posible_ubicasion_agente_buscado = ubicasion_agente_buscado
		if ubicasion_agente_buscado == None:
			self.ingresa_nuevo_destino( None ) #Le ingresaremos un destino aleatorio

		self.lista_camino_a_objetivo = self.obteniendo_mejor_camino_a_objetivo() #Se le ingrsa el mejor camino	

		self.objetivo_encontrado = False

		self.simbolo_objetivo = Simbolo_Objetivo


	def ingresa_nuevo_destino( self , tupla_destino=None ):
		if tupla_destino == None:
			size_tablero = self.obj_tablero.size
			tupla_destino = ( random.randint( 0 , size_tablero-1 ) , random.randint( 0 , size_tablero-1 ) )
			while tupla_destino == self.posible_ubicasion_agente_buscado:
				tupla_destino = ( random.randint( 0 , size_tablero-1 ) , random.randint( 0 , size_tablero-1 ) )

		self.posible_ubicasion_agente_buscado = tupla_destino 


	def obteniendo_mejor_camino_a_objetivo( self ):
		
		len_camino_minimo = self.obj_tablero.size * self.obj_tablero.size
		lista_camino = []

		dicc_casillas_disponibles = self.obtiene_valor_de_casillas_alcanzables_de_agente()
		for tupla_pos , value in dicc_casillas_disponibles.items():
			if value == "[ ]":
				lista_camino_encontrado = self.obteniendo_list_camino_a_objetivo( tupla_pos , self.posible_ubicasion_agente_buscado )
				if len( lista_camino_encontrado ) < len_camino_minimo:
					len_camino_minimo = len( lista_camino_encontrado )
					lista_camino = lista_camino_encontrado
		return lista_camino


	def obteniendo_list_camino_a_objetivo( self , tupla_pos_inicial , tupla_pos_objetivo ):
		#Definimos el camino hacia el objetivo, el mas corto
		# -El camino siempre es el mas corto, en diagonal
		
		#LAS TUPLAS SON INMUTABLES, NO ES POSIBLE MODIFICARLOS

		tupla_pasos_faltantes = ( tupla_pos_objetivo[0]-tupla_pos_inicial[0] , tupla_pos_objetivo[1]-tupla_pos_inicial[1] )		
		
		list_tupla_camino = []

		while tupla_pasos_faltantes[0] != 0 and tupla_pasos_faltantes[1] != 0 :
			mov_x = 1
			if tupla_pasos_faltantes[0] < 0:
				mov_x = -1

			mov_y = 1
			if tupla_pasos_faltantes[1] < 0:
				mov_y = -1

			list_tupla_camino.append( (mov_x,mov_y) )
			
			tupla_pasos_faltantes = ( tupla_pasos_faltantes[0] + (-1)*mov_x , tupla_pasos_faltantes[1] + (-1)*mov_y )

		while tupla_pasos_faltantes[0] != 0:
			mov_x = 1
			if tupla_pasos_faltantes[0] < 0:
				mov_x = -1

			list_tupla_camino.append( (mov_x,0) )

			tupla_pasos_faltantes = ( tupla_pasos_faltantes[0] + (-1)*mov_x , 0 ) 

		while tupla_pasos_faltantes[1] != 0:
			mov_y = 1
			if tupla_pasos_faltantes[1] < 0:
				mov_y = -1

			list_tupla_camino.append( (0,mov_y) )
			
			tupla_pasos_faltantes = ( 0 , tupla_pasos_faltantes[1] + (-1)*mov_y )

		pos_actual = tupla_pos_inicial
		lista_tupla_camino = [ tupla_pos_inicial ]
		for tupla_paso in list_tupla_camino:
			pos_actual = ( pos_actual[0] + tupla_paso[0] , pos_actual[1] + tupla_paso[1] )
			lista_tupla_camino.append( pos_actual )

		return lista_tupla_camino


	def moviendo_agente_sig_paso( self ):
		if len( self.lista_camino_a_objetivo ) != 0: 
			tupla_sig_paso = self.lista_camino_a_objetivo[0] #Obtenemos la siguiente tupla posicion

			diccionario_casillas_alcanzables = self.obtiene_valor_de_casillas_alcanzables_de_agente()
			
			if diccionario_casillas_alcanzables[ tupla_sig_paso ] != "[ ]":
				if diccionario_casillas_alcanzables[ tupla_sig_paso ] == f"[{self.simbolo_objetivo}]":
					self.objetivo_encontrado = True
				else:
					self.lista_camino_a_objetivo = self.obteniendo_mejor_camino_a_objetivo() #Recalculamos el camino porque tiene obstaculo

			tupla_siguiente_paso = self.lista_camino_a_objetivo.pop(0) #Quitamos de la lista la casilla donde nos moveremos
			self.mover_agente( tupla_siguiente_paso )


class Poblacion_Agentes_Buscadores():
	
	def __init__( self , cant_agentes , obj_tablero , simb_objetivo , tupla_pos_objetivo ):
		
		self.objetivo_encontrado = False
		self.tupla_pos_objetivo = tupla_pos_objetivo 
		self.obj_tablero = obj_tablero
		self.simb_objetivo = simb_objetivo

		self.list_poblacion = self.generando_Agentes_poblacion( cant_agentes )

	def generando_Agentes_poblacion( self , cantidad_Agentes ):
		list_pos_agentes_buscadores = []
		for index in range( cantidad_Agentes ):
			dim_tablero = self.obj_tablero.size
			random_pos_inicial = ( random.randint(0,dim_tablero-1) , random.randint(0,dim_tablero-1) )
			agente = Agente_Buscador( random_pos_inicial , self.obj_tablero , self.simb_objetivo , self.tupla_pos_objetivo )
			list_pos_agentes_buscadores.append( agente ) 
		return list_pos_agentes_buscadores

	def buscando_y_comunicando_ruido( self ):
		
		casillas_con_ruido = []

		for Agente in self.list_poblacion:
			
			dicc_casillas_continuas = Agente.obtiene_valor_de_casillas_alcanzables_de_agente()
			
			objetivo_encontrado = False
			for tupla_casilla,value in dicc_casillas_continuas.items():
				if value == f"[{self.simb_objetivo}]": #Simbolo de Objetivo
					self.tupla_pos_objetivo = tupla_casilla
					objetivo_encontrado = True
					break
			 
			if objetivo_encontrado == True:
				break
			else:
				ruido_encontrado = False
				for tupla_casilla,value in dicc_casillas_continuas.items():
					if value == "[R]": #Simbolo de Ruido
						casillas_con_ruido.append( tupla_casilla )
						ruido_encontrado = True

		if objetivo_encontrado == True:
			for Agente in self.list_poblacion:
				Agente.posible_ubicasion_agente_buscado = self.tupla_pos_objetivo
				Agente.lista_camino_a_objetivo = Agente.obteniendo_mejor_camino_a_objetivo()
		
		elif ruido_encontrado == True:
			for Agente in self.list_poblacion:
				casilla_ruido = casillas_con_ruido[ random.randint( 0 , len(casillas_con_ruido) ) ]
				
				Agente.posible_ubicasion_agente_buscado = self.tupla_pos_objetivo
				Agente.lista_camino_a_objetivo = Agente.obteniendo_mejor_camino_a_objetivo()

	def moviendo_poblacion(self):
		for Agente in self.list_poblacion:

			Agente.moviendo_agente_sig_paso()
			
			if Agente.objetivo_encontrado == True:
				self.objetivo_encontrado = True
				break

		

if __name__ == "__main__":
	
	# Dimencion Tablero(int) ------>>>>>
	Dimencion_Escenario = 30
	
	cant_agentes_buscadores = 10
	
	pos_Agente_objetivo = (10,14)

	simb_objetivo = "O"
	# ----------------------------->>>>>
	
	tablero = Escenario_py.Tablero( Dimencion_Escenario )
	
	tablero.ingresando_bloques_bloquedos()

	tablero.ingresa_objeto_a_tablero( pos_Agente_objetivo , simb_objetivo )
	
	Poblacion = Poblacion_Agentes_Buscadores( cant_agentes_buscadores , tablero , simb_objetivo , pos_Agente_objetivo )

	while Poblacion.objetivo_encontrado == False: 	
		
		os.system('CLS')

		tablero.mostrarMatriz()
		
		Poblacion.moviendo_poblacion()

		Poblacion.buscando_y_comunicando_ruido()

		time.sleep( 0.65 )

	print("OBJETIVO ENCONTRADO")
	tablero.mostrarMatriz()
