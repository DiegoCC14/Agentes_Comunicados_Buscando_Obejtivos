import os , time , random


class MatrizNew():
		def __init__(self,filas,columnas):
				self.matriz = []
				for i in range(filas):
						self.matriz.append(['[ ]']*columnas)

		def mostrarMatriz(self):
				for x in range(len(self.matriz)):
					print("-",end="")
				print("")
				for x in range(len(self.matriz)-1,-1,-1):
						for i in range(len(self.matriz[0])):
								print(self.matriz[x][i],end=" ")
						print("")
				for x in range(len(self.matriz)):
					print("-",end="")
				print("")

class Tablero(MatrizNew):
	
	def __init__(self,tamanio_tablero):
		MatrizNew.__init__(self,tamanio_tablero,tamanio_tablero)
		self.tablero = self.matriz
		self.size = tamanio_tablero
		self.casillas_bloqueadas = []

	def obtener_valor_de_casilla(self,tupla_posicion):
		return self.tablero[tupla_posicion[0]][tupla_posicion[1]]

	def ingresa_objeto_a_tablero( self , tupla_posicion , string_simbolo ):
		self.tablero[ tupla_posicion[0] ][ tupla_posicion[1] ] = '['+string_simbolo+']'

	def borrar_casilla_tablero( self , tupla_posicion ):
		self.tablero[tupla_posicion[0]][tupla_posicion[1]] = '[ ]'

	def ingresando_bloques_bloquedos( self , lista_tuplas_posicion_bloques=None):
		if lista_tuplas_posicion_bloques == None: #Si no se ingresa sera random
			cantidad_bloques = int( ( self.size * self.size )/3)

			lista_tuplas_posicion_bloques = [ ( random.randint(0,self.size-1) , random.randint(0,self.size-1) ) for x in range( cantidad_bloques )]
			
		for tupla in lista_tuplas_posicion_bloques:
			self.ingresa_objeto_a_tablero( tupla , '■' )


if __name__ == "__main__":
	
	# Dimencion Tablero(int) ------>>>>>
	Dimencion_Escenario = 15
	# ----------------------------->>>>>

	tablero = Tablero( Dimencion_Escenario )
	
	tablero.ingresando_bloques_bloquedos()

	tablero.mostrarMatriz()