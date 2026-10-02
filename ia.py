from modelo import Ficha

class InteligenciaArtificial:

    def __init__(self, jugador=Ficha.O):
        """Inicializa la inteligencia artificial con el jugador especificado.

        Args:
            jugador (Ficha): El jugador que controlará la IA. Por defecto es Ficha.O.
        """
        self.jugador = jugador
        self.rival = jugador.siguiente()

    def mejor_movimiento(self, tablero):
        """Determina el mejor movimiento para la IA en el tablero dado.

        Args:
            tablero (Tablero): El estado actual del tablero.

        Returns:
            tuple: La posición (fila, columna) del mejor movimiento, o None si no hay movimientos posibles.
        """
        if self._ganador(tablero) is not None or tablero.esta_lleno():
            return None

        mejor_valor = float("-inf")
        mejor_movimiento = None

        # Itera sobre todas las posiciones del tablero para evaluar el mejor movimiento.
        for fila in range(len(tablero.tablero)):
            for columna in range(len(tablero.tablero[fila])):
                # Verifica si la posición está disponible para jugar.
                if not tablero.jugar_acciones(fila, columna):
                    continue

                tablero.jugar(self.jugador, fila, columna)
                valor = self._minimax(tablero, 0, False) # Evalúa el valor del movimiento usando el algoritmo minimax.
                tablero.tablero[fila][columna] = None

                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = (fila, columna)

        return mejor_movimiento

    def _minimax(self, tablero, profundidad, maximiza):
        """Implementa el algoritmo minimax para evaluar el valor de un movimiento en el tablero.

        Args:
            tablero (Tablero): El estado actual del tablero.
            profundidad (int): La profundidad actual en el árbol de decisiones.
            maximiza (bool): Indica si se está maximizando el valor (True) o minimizando (False).

        Returns:
            int: El valor evaluado del movimiento.
        """
        ganador = self._ganador(tablero)
        if ganador == self.jugador:
            return 10 - profundidad # Retorna un valor positivo si la IA gana, ajustado por la profundidad para priorizar victorias rápidas.
        if ganador == self.rival:
            return profundidad - 10 # Retorna un valor negativo si el rival gana, ajustado por la profundidad para priorizar derrotas tardías.
        if tablero.esta_lleno():
            return 0

        # Inicializa el mejor valor dependiendo de si se está maximizando o minimizando.
        mejor_valor = float("-inf") if maximiza else float("inf")
        ficha = self.jugador if maximiza else self.rival

        # Itera sobre todas las posiciones del tablero para evaluar los posibles movimientos.
        for fila in range(len(tablero.tablero)):
            for columna in range(len(tablero.tablero[fila])):
                if not tablero.jugar_acciones(fila, columna):
                    continue

                tablero.jugar(ficha, fila, columna)
                valor = self._minimax(tablero, profundidad + 1, not maximiza)
                tablero.tablero[fila][columna] = None  # Deshace el movimiento para evaluar otras opciones.

                # Actualiza el mejor valor dependiendo de si se está maximizando o minimizando.
                if maximiza:
                    mejor_valor = max(mejor_valor, valor)
                else:
                    mejor_valor = min(mejor_valor, valor)

        return mejor_valor

    def _ganador(self, tablero):
        """Determina el ganador del tablero.

        Args:
            tablero (Tablero): El estado actual del tablero.

        Returns:
            str: La ficha del ganador (self.jugador o self.rival), o None si no hay ganador.
        """
        for ficha in (self.jugador, self.rival):
            if tablero.gana(ficha):
                return ficha

        return None