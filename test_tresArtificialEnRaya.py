import pytest

from modelo import Ficha, Tablero, Partida
from ia import InteligenciaArtificial


def test_jugada_ocupa_casilla_vacia():
    tablero = Tablero(3)

    assert tablero.jugar(Ficha.X, 0, 0)
    assert tablero.tablero[0][0] is Ficha.X


def test_no_permite_ocupar_una_casilla_ya_usada():
    tablero = Tablero(3)
    assert tablero.jugar(Ficha.X, 0, 0)

    assert not tablero.jugar(Ficha.O, 0, 0)
    assert tablero.tablero[0][0] is Ficha.X


@pytest.mark.parametrize(
    "casillas_ganadoras",
    [
        [(0, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ],
)
def test_detecta_victorias_en_filas_columnas_y_diagonales(casillas_ganadoras):
    tablero = Tablero(3)

    for fila, columna in casillas_ganadoras:
        tablero.jugar(Ficha.X, fila, columna)

    assert tablero.gana(Ficha.X)


def test_detecta_empate_sin_ganador():
    tablero = Tablero(3)
    filas = [
        [Ficha.X, Ficha.O, Ficha.X],
        [Ficha.X, Ficha.O, Ficha.O],
        [Ficha.O, Ficha.X, Ficha.X],
    ]

    for fila, fichas in enumerate(filas):
        for columna, ficha in enumerate(fichas):
            tablero.jugar(ficha, fila, columna)

    assert tablero.esta_lleno()
    assert not tablero.gana(Ficha.X)
    assert not tablero.gana(Ficha.O)


def test_ia_elige_una_victoria_inmediata():
    tablero = Tablero(3)
    for fila, columna in [(1, 0), (1, 1)]:
        tablero.jugar(Ficha.O, fila, columna)
    tablero.jugar(Ficha.X, 0, 0)
    tablero.jugar(Ficha.X, 0, 1)

    ia = InteligenciaArtificial(Ficha.O)

    assert ia.mejor_movimiento(tablero) == (1, 2)


def test_ia_bloquea_una_victoria_inmediata():
    tablero = Tablero(3)
    tablero.jugar(Ficha.X, 0, 0)
    tablero.jugar(Ficha.X, 0, 1)
    tablero.jugar(Ficha.O, 1, 1)

    ia = InteligenciaArtificial(Ficha.O)

    assert ia.mejor_movimiento(tablero) == (0, 2)

def test_partida_cambia_turno_al_aceptar_una_jugada():
    partida = Partida(3)
    turno_inicial = partida.turno

    assert partida.jugar(0, 0)
    assert partida.tablero.tablero[0][0] is turno_inicial
    assert partida.turno is turno_inicial.siguiente()


def test_partida_no_cambia_turno_si_la_casilla_esta_ocupada():
    partida = Partida(3)
    assert partida.jugar(0, 0)
    turno_actual = partida.turno

    assert not partida.jugar(0, 0)
    assert partida.turno is turno_actual

@pytest.mark.parametrize(
    "fila,columna",
    [
        (-1, 0),
        (3, 0),
        (0, -1),
        (0, 3),
    ],
)
def test_tablero_rechaza_coordenadas_fuera_rango(fila, columna):
    tablero = Tablero(3)

    assert not tablero.jugar_acciones(fila, columna)
    assert not tablero.jugar(Ficha.X, fila, columna)
    assert all(casilla is None for fila_tablero in tablero.tablero for casilla in fila_tablero)