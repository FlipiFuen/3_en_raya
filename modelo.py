import random

from enum import Enum

class Ficha(Enum):
    X = "X"
    O = "O"

    def siguiente(self):
        if self == self.X:
            return self.O
        if self == self.O:
            return self.X
        return None

class Tablero:

    def __init__(self, tamanyo):
        self.tablero = []
        for i in range(tamanyo):
            fila = []
            for j in range(tamanyo):
                fila.append(None)
            self.tablero.append(fila)

    def jugar(self, ficha, fila, columna):
        """Realiza una jugada en el tablero si es posible.

        Args:
            ficha (Ficha): La ficha del jugador que realiza la jugada.
            fila (int): La fila donde se desea colocar la ficha.
            columna (int): La columna donde se desea colocar la ficha.

        Returns:
            bool: True si la jugada fue exitosa, False en caso contrario.
        """
        if not self.jugar_acciones(fila, columna):
            return False

        self.tablero[fila][columna] = ficha
        return True

    def jugar_acciones(self, fila, columna):
        """Verifica si es posible realizar una jugada en la posición especificada.

        Args:
            fila (int): La fila donde se desea colocar la ficha.
            columna (int): La columna donde se desea colocar la ficha.

        Returns:
            bool: True si la jugada es posible, False en caso contrario.
        """
        if not 0 <= fila < len(self.tablero):
            return False
        if not 0 <= columna < len(self.tablero[fila]):
            return False

        return self.tablero[fila][columna] is None

    def esta_lleno(self):
        for linea in self.tablero:
            for ficha in linea:
                if ficha == None:
                    return False
        return True

    def gana(self, jugador):
        return self.gana_horizontal(jugador) or self.gana_vertical(jugador) or self.gana_diagonal_directa(jugador) or self.gana_diagonal_inversa(jugador)

    def gana_horizontal(self, jugador):
        gana = False
        for linea in self.tablero:
            gana = True
            for ficha in linea:
                gana &= ficha == jugador
            if gana:
                break
        return gana

    def gana_vertical(self, jugador):
        gana = False
        for i in range(len(self.tablero)):
            gana = True
            for j in range(len(self.tablero[i])):
                gana &= self.tablero[j][i] == jugador
            if gana:
                break
        return gana

    def gana_diagonal_directa(self, jugador):
        gana = True
        for i in range(len(self.tablero)):
            gana &= self.tablero[i][i] == jugador
        return gana

    def gana_diagonal_inversa(self, jugador):
        gana = True
        for i in range(len(self.tablero)):
            gana &= self.tablero[len(self.tablero) - 1 - i][i] == jugador
        return gana

class Partida:

    def __init__(self, tamanyo):
        self.tablero = Tablero(tamanyo)
        self.turno = random.choice(list(Ficha))
        self.tamanyo = tamanyo

    def jugar(self, fila, columna):
        if self.terminada():
            return False

        posible = self.tablero.jugar(self.turno, fila, columna)
        if posible:
            self.turno = self.turno.siguiente()
        return posible

    def terminada(self):
        return self.tablero.esta_lleno() or self.ganador() is not None

    def ganador(self):
        for jugador in list(Ficha):
            if self.tablero.gana(jugador):
                return jugador
        return None