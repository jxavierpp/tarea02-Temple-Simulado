#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'juliowaissman'


import blocales
from random import shuffle
from random import sample
from itertools import combinations

# Agregados
import time
from decimal import Decimal


class ProblemaNreinas(blocales.Problema):
    """
    Las N reinas en forma de búsqueda local se inicializa como

    entorno = ProblemaNreinas(n) donde n es el número de reinas a colocar

    Por default son las clásicas 8 reinas.

    """
    def __init__(self, n=8):
        self.n = n

    def estado_aleatorio(self):
        estado = list(range(self.n))
        shuffle(estado)
        return tuple(estado)

    @staticmethod
    def swap(x, i, j):
        """
        Intercambia los elemento i y j de la lista x

        """
        if not isinstance(x, type([1, 2])):
            raise TypeError("Este método solo se puede hacer con listas")
        x[i], x[j] = x[j], x[i]

    def vecinos(self, estado):
        """
        Generador vecinos de un estado, todas las 2 permutaciones

        @param estado: una tupla que describe un estado.

        @return: un generador de estados vecinos.

        """
        x = list(estado)
        for i, j in combinations(range(self.n), 2):
            self.swap(x, i, j)
            yield tuple(x)
            self.swap(x, i, j)

    def vecino_aleatorio(self, estado):
        """
        Genera un vecino de un estado intercambiando dos posiciones
        en forma aleatoria.

        @param estado: Una tupla que describe un estado

        @return: Una tupla con un estado vecino.

        """
        vecino = list(estado)
        i, j = sample(range(self.n), 2)
        self.swap(vecino, i, j)
        return tuple(vecino)

    def costo(self, estado):
        """
        Calcula el costo de un estado por el número de conflictos entre reinas

        @param estado: Una tupla que describe un estado

        @return: Un valor numérico, mientras más pequeño, mejor es el estado.

        """
        return sum((1 for (i, j) in combinations(range(self.n), 2)
                    if abs(estado[i] - estado[j]) == abs(i - j)))


def prueba_descenso_colinas(problema=ProblemaNreinas(8), repeticiones=10):
    """ Prueba el algoritmo de descenso de colinas con n repeticiones """

    print("\n\n" + "intento".center(10) +
          "estado".center(60) + "costo".center(10))
    for intento in range(repeticiones):
        solucion = blocales.descenso_colinas(problema)
        print(str(intento).center(10) +
              str(solucion).center(60) +
              str(problema.costo(solucion)).center(10))


def prueba_temple_simulado(problema=ProblemaNreinas(8)):
    """ Prueba el algoritmo de temple simulado """

    solucion = blocales.temple_simulado(problema)
    print("\n\nTemple simulado con calendarización To/(1 + i).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)

if __name__ == "__main__":

    prueba_descenso_colinas(ProblemaNreinas(32), 10)
    prueba_temple_simulado(ProblemaNreinas(32))

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    #
    #   Se realizaron varias pruebas con este metodo, personalmente escojo una cantidad de 64
    #   64 reinas, cuyo resultado 1 loop, best of 3: 3min 17s per loop. Este tiempo lo considero
    #   alto para una cantidad moderada de reinas. Descenso de colinas es lento, pero funciona
    #   8 reinas 8.93ms
    #   32 reinas 5.02
    #   64 reinas 3m 17s
    #   100 reinas 1 loop, best of 3: 26min 3s per loop
    #
    #
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? ¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    #
    #   Los valores del temple simulado cambian con los calendizadores propuestos,
    #   se manejo dos bastantes sencillos con los que se nota una mayor respuesta
    #   Algunos proponen calendizadores exponenciales, pero estos deben ser configurados

    #  
    #  
    #
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario probar diferentes metdos de
    # calendarización, prueba al menos otros dos métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    #   Propusimos dos calendarizaciones dado que un tiende a 1 y la otra 0, la que tiende a
    #   uno funciona de forma mas rapida, llegando al resultado en una visible diferencia de los
    #   tiempos.
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #

    #Pruebas originales propuesta por Julio Waissman
    #prueba_descenso_colinas(ProblemaNreinas(32), 10)
    #prueba_temple_simulado(ProblemaNreinas(32))

    n = 64 # cantidad de reinas a resolver

    problema_reinas = ProblemaNreinas(n)

    prueba_temple_simulado(problema_reinas)

    costos = [problema_reinas.costo(problema_reinas.estado_aleatorio())
                for _ in range(10 * len(problema_reinas.estado_aleatorio()))]
                # aumentamos la cantidad de costos generados
    minimo, maximo = min(costos), max(costos)
    t_inicial = 2 * (maximo - minimo)

    # generadores
    cal_1 = (t_inicial / (0.01 * i) for i in range(1, int(1e10)))
    cal_2 = (t_inicial * (0.9 * i) for i in range(1, int(1e10)))

    for cal in (cal_1, cal_2):
        resultado = blocales.temple_simulado(problema_reinas, cal)
        print("Costo del resultado: ", problema_reinas.costo(resultado))
        print("Resultado: ")
        print(resultado)
