"""
Created on Wed Jan 29 18:57:53 2025

@author: flipi
"""

import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
from functools import partial

from modelo import Ficha, Partida
from ia import InteligenciaArtificial

TAM_BOTON = 3
TAM_FUENTE = 12

TAMANYO = 3

COLORES_FICHA = {Ficha.X: "#ff0000", Ficha.O: "#00ff00"}

TITULO = "****3 en raya****"
INICIO = "Primer turno: {}"
TERMINADA = "Partida terminada: ganó {}"
EMPATE = "Partida terminada: empate"
TURNO = "Turno: {}"
OCUPADA = "Casilla ocupada"
GANADOR = "¡{} gana!"


class Ventana(tk.Frame):
    def __init__(self, ventana):
        super().__init__(ventana)
        self.ventana = ventana
        self.partida = None
        self.tableroGrafico = None
        self.menu = tk.Menu(self.ventana)
        self.ventana.config(menu=self.menu)
        self.menu.add_command(label="Salir", command=self.ventana.quit)
        self.menu.add_command(label="Nueva Partida", command=self.partida_nueva)
        self.bienvenida = tk.Label(self, text= TITULO, font=("Arial", 20), fg="blue", bg="lightyellow")
        self.bienvenida.grid(row=0, column=0, pady=(24, 8), columnspan=3, sticky="n")
        self.jugar = tk.Button(self, text="Jugar", font=("Arial", 15), fg="blue", bg="lightgreen", command=self.partida_nueva)
        self.jugar.grid(row=1, column=0, pady=8, columnspan=3, sticky="n")
        self.pack(fill="both", expand=True)

        for columna in range(3):
            self.grid_columnconfigure(columna, weight=1)

        self.grid_rowconfigure(2, weight=1)

    def partida_nueva(self):
        if self.tableroGrafico is not None:
            self.tableroGrafico.destroy()

        self.partida = Partida(TAMANYO)
        self.tableroGrafico = TableroGrafico(self.partida, self)


class TableroGrafico(tk.Frame):

    def __init__(self, partida, ventana):
        self.partida = partida
        super().__init__(ventana)
        self.grid(row=2, column=0, columnspan=3, pady=16, sticky="n")
        self.juegoYo = JugadasPC(self, partida)
        self.listener = JugadasListener(partida, self)
        self.casillero = Casillero(self, partida, self.listener)
        self.barraEstado = tk.Label(self)
        if self.partida.turno == Ficha.X:
            self.barraEstado.config(text= INICIO.format(partida.turno.name))
        else:
            self.partida.jugar(1, 1)
            self.casillero.casillas[1][1].ocupar(Ficha.O)
            self.barraEstado.config(text= TURNO.format(Ficha.X.name))
        self.barraEstado.pack()

    def actualizar_estado(self, mensaje):
        self.barraEstado.config(text = mensaje)
        if self.partida.turno == Ficha.O:
            self.juegoYo.jugar()

    def actualizar_despues_de_jugada(self):
        """Actualiza el estado del tablero después de una jugada, verificando si hay un ganador o un empate.

        Esta función se encarga de actualizar la barra de estado con el mensaje correspondiente,
        ya sea indicando el turno del siguiente jugador, la victoria de un jugador o un empate.
        """
        ganador = self.partida.ganador()

        if ganador is not None:
            self.casillero.bloquear()
            self.barraEstado.config(text=GANADOR.format(ganador.name))
        elif self.partida.terminada():
            self.casillero.bloquear()
            self.barraEstado.config(text=EMPATE)
            messagebox.showinfo(
                "Fin del juego",
                "Hemos empatado, Enhorabuena!! Teniendo en cuenta que no puedes ganarme, has estado brillante"
            )
        else:
            self.actualizar_estado(TURNO.format(self.partida.turno.name))

    def jugar(self, fila, columna, jugador):
        self.casillero.jugar(fila, columna, jugador)

class Casillero(tk.Frame):

    def __init__(self, tablero, partida, listener):
        super().__init__(tablero)
        self.partida = partida
        self.casillas = []
        for i in range(partida.tamanyo):
            fila = []
            for j in range(partida.tamanyo):
                pulsarIJ = partial(listener.pulsar, i, j)
                casilla  = Casilla(self, i, j, pulsarIJ)
                fila.append(casilla)
            self.casillas.append(fila)
        self.pack()

    def jugar(self, fila, columna, jugador):
        self.casillas[fila][columna].ocupar(jugador)

    def bloquear(self):
        """Bloquea todas las casillas del tablero, deshabilitándolas para que no se puedan realizar más jugadas."""
        for fila in self.casillas:
            for casilla in fila:
                casilla.configure(state=tk.DISABLED)

class Casilla(tk.Button):

    def __init__(self, casillero, fila, col, pulsarIJ):
        super().__init__(casillero, command = pulsarIJ, height = TAM_BOTON, width = TAM_BOTON)
        self.grid(row = fila, column = col)

    def ocupar(self, jugador):
        FUENTE = font.Font(size=TAM_FUENTE, weight="bold")
        self["font"] = FUENTE
        self["text"] = jugador.name
        self["fg"] = COLORES_FICHA[jugador]

class JugadasListener:

    def __init__(self, partida, gui):
        self.partida = partida
        self.gui = gui

    def pulsar(self, fila, columna):

        if self.partida.terminada():
            ganador = self.partida.ganador()
            if ganador is None:
                self.gui.actualizar_estado(EMPATE)
            else:
                self.gui.actualizar_estado(TERMINADA.format(ganador.name))
            return
        jugador = self.partida.turno
        if self.partida.jugar(fila, columna):
            self.gui.jugar(fila, columna, jugador)
            self.gui.actualizar_despues_de_jugada()
        else:
            self.gui.actualizar_estado(OCUPADA.format(jugador.name))

class JugadasPC:

    def __init__(self, gui, partida):
        self.partida = partida
        self.gui = gui
        self.inteligencia = InteligenciaArtificial(Ficha.O)

    def jugar(self):
        """Realiza la jugada de la IA en el tablero, actualizando la interfaz gráfica según corresponda.

        Returns:
            None
        """
        if self.partida.terminada():
            return

        movimiento = self.inteligencia.mejor_movimiento(self.partida.tablero)
        if movimiento is None:
            return

        jugador = Ficha.O
        if self.partida.jugar(movimiento[0], movimiento[1]):
            self.gui.jugar(movimiento[0], movimiento[1], jugador)
            self.gui.actualizar_despues_de_jugada()
        else:
            self.gui.actualizar_estado(OCUPADA.format(jugador.name))