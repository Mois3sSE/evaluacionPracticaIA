import heapq
import random
import math


class ModeloIA:
    def resolver_problema(self, problema: str, algoritmo: str, evento_cancelar) -> dict:
        """Punto de entrada único que cumple con el contrato del Controlador."""
        
        if problema == "FrozenLake":
            matriz = [[0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 0],
                      [0, 0, 0, 1, 0],
                      [1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
            inicio, meta = (0, 0), (4, 4)
            return self._buscar_frozen_lake(matriz, inicio, meta, algoritmo, evento_cancelar)

        elif problema == "Sokoban":
            matriz = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
            inicio_jugador, inicio_caja, meta_caja = (0,0), (1,2), (2,4)
            return self._buscar_sokoban(matriz, inicio_jugador, inicio_caja, meta_caja, algoritmo, evento_cancelar)

        elif problema == "8Reinas":
            return self._buscar_8_reinas(algoritmo, evento_cancelar)

        elif problema == "Gato":
            tablero = [0] * 9
            return self._minimax_lanzador(tablero, evento_cancelar)

        return {"exito": False, "mensaje": "Problema no reconocido por el modelo.", "camino_solucion": []}

# Algoritmos
    
    def _buscar_frozen_lake(self, matriz, inicio, meta, algoritmo, evento_cancelar):
        filas, columnas = len(matriz), len(matriz[0])
        frontera = [[inicio]]
        visitados = set([inicio])
        pasos_exploracion = []

        while frontera:
            if evento_cancelar.is_set():
                return {"exito": False, "mensaje": "Búsqueda cancelada por el usuario.", "camino_solucion": []}

            camino = frontera.pop(0) if algoritmo == "BFS" else frontera.pop()
            nodo_actual = camino[-1]
            pasos_exploracion.append(nodo_actual)

            if nodo_actual == meta:
                return {"exito": True, "mensaje": f"Solución hallada con {algoritmo}. Pasos: {len(camino)}", "camino_solucion": camino}

            r, c = nodo_actual
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < filas and 0 <= nc < columnas and matriz[nr][nc] != 1:
                    if (nr, nc) not in visitados:
                        visitados.add((nr, nc))
                        frontera.append(camino + [(nr, nc)])
                        
        return {"exito": False, "mensaje": "No se encontró ruta posible.", "camino_solucion": pasos_exploracion}

    def _heuristica_sokoban(self, caja, meta, tipo="Manhattan"):
        if tipo == "Euclidiana":
            return math.sqrt((caja[0] - meta[0])**2 + (caja[1] - meta[1])**2)
        return abs(caja[0] - meta[0]) + abs(caja[1] - meta[1])

    def _buscar_sokoban(self, matriz, inicio_jugador, inicio_caja, meta_caja, algoritmo, evento_cancelar):
        tipo_heuristica = "Euclidiana" if "Euclidiana" in algoritmo else "Manhattan"
        es_a_estrella = "A*" in algoritmo
        
        estado_inicial = (inicio_jugador, inicio_caja)
        cola = []
        h_ini = self._heuristica_sokoban(inicio_caja, meta_caja, tipo_heuristica)
        heapq.heappush(cola, (h_ini, 0, estado_inicial, [estado_inicial]))
        visitados = set()

        while cola:
            if evento_cancelar.is_set():
                return {"exito": False, "mensaje": "Búsqueda cancelada por el usuario.", "camino_solucion": []}

            prioridad, g, estado_actual, camino = heapq.heappop(cola)
            p_jugador, p_caja = estado_actual

            if estado_actual in visitados: continue
            visitados.add(estado_actual)

            if p_caja == meta_caja:
                return {"exito": True, "mensaje": f"Sokoban resuelto con {algoritmo}", "camino_solucion": camino}

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                np_jugador = (p_jugador[0] + dr, p_jugador[1] + dc)
                
                if not (0 <= np_jugador[0] < len(matriz) and 0 <= np_jugador[1] < len(matriz[0])): continue
                if matriz[np_jugador[0]][np_jugador[1]] == 1: continue

                if np_jugador == p_caja:
                    np_caja = (p_caja[0] + dr, p_caja[1] + dc)
                    if not (0 <= np_caja[0] < len(matriz) and 0 <= np_caja[1] < len(matriz[0])): continue
                    if matriz[np_caja[0]][np_caja[1]] == 1: continue
                    nuevo_estado = (np_jugador, np_caja)
                else:
                    nuevo_estado = (np_jugador, p_caja)

                if nuevo_estado not in visitados:
                    nuevo_g = g + 1
                    h = self._heuristica_sokoban(nuevo_estado[1], meta_caja, tipo_heuristica)
                    f = (nuevo_g + h) if es_a_estrella else h
                    heapq.heappush(cola, (f, nuevo_g, nuevo_estado, camino + [nuevo_estado]))

        return {"exito": False, "mensaje": "Atrapado. No hay solución.", "camino_solucion": []}

    def _calcular_conflictos(self, estado):
        conflictos = 0
        n = len(estado)
        for i in range(n):
            for j in range(i + 1, n):
                if estado[i] == estado[j] or abs(estado[i] - estado[j]) == abs(i - j):
                    conflictos += 1
        return conflictos

    def _buscar_8_reinas(self, algoritmo, evento_cancelar):
        estado_actual = [random.randint(0, 7) for _ in range(8)]
        conflictos_actual = self._calcular_conflictos(estado_actual)
        pasos_exploracion = [list(estado_actual)]
        t = 100.0

        for _ in range(1000):
            if evento_cancelar.is_set():
                return {"exito": False, "mensaje": "Búsqueda cancelada por el usuario.", "camino_solucion": []}

            if conflictos_actual == 0:
                return {"exito": True, "mensaje": "Configuración óptima encontrada", "camino_solucion": pasos_exploracion}

            if "Hill Climbing" in algoritmo:
                mejor_vecino = None
                mejor_conflictos = conflictos_actual

                for fila in range(8):
                    for col in range(8):
                        if col == estado_actual[fila]: continue
                        vecino = list(estado_actual)
                        vecino[fila] = col
                        c = self._calcular_conflictos(vecino)
                        if c < mejor_conflictos:
                            mejor_conflictos = c
                            mejor_vecino = vecino

                if mejor_vecino is None:
                    if "reinicio" not in algoritmo.lower():
                        return {"exito": False, "mensaje": "Atascado en mínimo local", "camino_solucion": pasos_exploracion}
                    estado_actual = [random.randint(0, 7) for _ in range(8)]
                    conflictos_actual = self._calcular_conflictos(estado_actual)
                else:
                    estado_actual = mejor_vecino
                    conflictos_actual = mejor_conflictos
                    pasos_exploracion.append(list(estado_actual))

            elif "Recocido" in algoritmo:
                vecino = list(estado_actual)
                fila_aleatoria = random.randint(0, 7)
                vecino[fila_aleatoria] = random.randint(0, 7)
                conflictos_vecino = self._calcular_conflictos(vecino)

                diff = conflictos_actual - conflictos_vecino
                if diff > 0 or random.random() < math.exp(diff / t):
                    estado_actual = vecino
                    conflictos_actual = conflictos_vecino
                    pasos_exploracion.append(list(estado_actual))
                t *= 0.95

        return {"exito": False, "mensaje": "Límite de iteraciones alcanzado", "camino_solucion": pasos_exploracion}

    def _evaluar_tablero(self, b):
        lineas = [b[0:3], b[3:6], b[6:9], b[0::3], b[1::3], b[2::3], b[0::4], b[2:7:2]]
        if [1, 1, 1] in lineas: return 1   
        if [-1, -1, -1] in lineas: return -1 
        if 0 not in b: return 0 
        return None

    def _minimax_recursivo(self, tablero, es_max, evento_cancelar):
        if evento_cancelar.is_set(): return 0, -1 

        puntuacion = self._evaluar_tablero(tablero)
        if puntuacion is not None: return puntuacion, -1

        mejor_val = -float('inf') if es_max else float('inf')
        mejor_mov = -1

        for i in range(9):
            if tablero[i] == 0:
                tablero[i] = 1 if es_max else -1
                val, _ = self._minimax_recursivo(tablero, not es_max, evento_cancelar)
                tablero[i] = 0
                
                if es_max and val > mejor_val: 
                    mejor_val, mejor_mov = val, i
                elif not es_max and val < mejor_val: 
                    mejor_val, mejor_mov = val, i
                    
        return mejor_val, mejor_mov

    def _minimax_lanzador(self, tablero, evento_cancelar):
        """Prepara el retorno para el Gato."""
        _, movimiento = self._minimax_recursivo(tablero, True, evento_cancelar)
        if evento_cancelar.is_set():
            return {"exito": False, "mensaje": "Cancelado", "camino_solucion": []}
        return {"exito": True, "mensaje": "Movimiento calculado", "camino_solucion": [movimiento]}