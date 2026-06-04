# Cerebro educativo, definimos la compatibilidad de los problemas con los algoritmos

COMPATIBILIDAD = {
    "FrozenLake": {
        "Backtracking": {"valido": True, "mensaje": "Ejecutando Backtracking (DFS). Explorando exhaustivamente y retrocediendo en los callejones sin salida."},
        "Búsqueda por anchura": {"valido": True, "mensaje": "Ejecutando BFS. Garantiza encontrar la ruta más corta expandiendo niveles de forma uniforme."},
        "GBFS": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: GBFS es una búsqueda informada. En un laberinto a ciegas no hay una heurística (distancia) predefinida hacia la meta."},
        "A*": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: A* requiere una heurística. Este problema se clasificó como Búsqueda No Informada."},
        "Hill climbing": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: Hill Climbing no tiene memoria. El agente avanzará pero se quedará atascado permanentemente en el primer callejón sin salida (mínimo local)."},
        "Hill climbing con reinicio": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: Aunque el reinicio ayuda, los problemas de rutas (Pathfinding) requieren memoria de los nodos visitados, no solo optimización estática."},
        "Recocido": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: El Recocido Simulado optimiza estados, no construye rutas paso a paso desde un inicio hasta un fin."},
        "Minimax": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: Minimax requiere un adversario. Un laberinto determinista no compite contra ti."}
    },
    
    "Sokoban": {
        "Backtracking": {"valido": False, "tipo_error": "Complejidad", "mensaje": "Advertencia: El espacio de estados es masivo. Backtracking (DFS) caerá en ramas infinitas sin encontrar la solución rápidamente."},
        "Búsqueda por anchura": {"valido": False, "tipo_error": "Complejidad", "mensaje": "Advertencia: Explosión combinatoria. BFS saturará la memoria RAM intentando evaluar todas las permutaciones posibles a ciegas."},
        "GBFS": {"valido": True, "mensaje": "Ejecutando Búsqueda Voraz. Compara cómo la heurística Euclidiana vs Manhattan cambia los tiempos, aunque no garantice el mínimo de empujes."},
        "A*": {"valido": True, "mensaje": "Ejecutando A*. Óptimo y completo. La heurística Manhattan es matemáticamente ideal para el movimiento en cuadrículas."},
        "Hill climbing": {"valido": False, "tipo_error": "Eficiencia", "mensaje": "Error: Sokoban requiere planificar secuencias de empujes. Las búsquedas locales no manejan bien este nivel de encadenamiento temporal."},
        "Hill climbing con reinicio": {"valido": False, "tipo_error": "Eficiencia", "mensaje": "Error: Sokoban requiere planificar secuencias de empujes. Las búsquedas locales no manejan bien este nivel de encadenamiento temporal."},
        "Recocido": {"valido": False, "tipo_error": "Eficiencia", "mensaje": "Error: Sokoban requiere planificar secuencias de empujes. Las búsquedas locales no manejan bien este nivel de encadenamiento temporal."},
        "Minimax": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: Sokoban es un rompecabezas de un solo jugador (agente solitario), no hay oponente."}
    },
    
    "8Reinas": {
        "Backtracking": {"valido": True, "mensaje": "Ejecutando Backtracking. Clásico para Problemas de Satisfacción de Restricciones (CSP), colocando reina por reina y validando."},
        "Búsqueda por anchura": {"valido": False, "tipo_error": "Eficiencia", "mensaje": "Error conceptual: BFS busca 'rutas'. Aquí no importa la secuencia de movimientos, sino la configuración final del tablero."},
        "GBFS": {"valido": False, "tipo_error": "Eficiencia", "mensaje": "Error conceptual: GBFS busca 'rutas'. Aquí no importa la secuencia de movimientos, sino la configuración final del tablero."},
        "A*": {"valido": False, "tipo_error": "Eficiencia", "mensaje": "Error conceptual: A* busca 'rutas'. Aquí no importa la secuencia de movimientos, sino la configuración final del tablero."},
        "Hill climbing": {"valido": True, "mensaje": "Ejecutando Hill Climbing. Evaluando tableros vecinos para minimizar los ataques, cuidado con los mínimos locales."},
        "Hill climbing con reinicio": {"valido": True, "mensaje": "Ejecutando Hill Climbing con Reinicio. Al atascarse, el tablero se reinicia aleatoriamente, garantizando encontrar la solución global."},
        "Recocido": {"valido": True, "mensaje": "Ejecutando Recocido Simulado. Aceptando movimientos peores al inicio (temperatura alta) para escapar de los mínimos locales con éxito."},
        "Minimax": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: Colocar 8 reinas no implica un oponente intentando capturarlas."}
    },
    
    "Gato": {
        "Backtracking": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: Ignora las decisiones del oponente. No puedes retroceder los movimientos del otro jugador a voluntad."},
        "Búsqueda por anchura": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: BFS asume un entorno estático. Ignorará por completo la estrategia de bloqueo del jugador humano."},
        "GBFS": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: Ignora al oponente activo."},
        "A*": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: Ignora al oponente activo."},
        "Hill climbing": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: Las métricas locales no sirven cuando un oponente modifica maliciosamente el estado del tablero en el siguiente turno."},
        "Hill climbing con reinicio": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: Las métricas locales no sirven cuando un oponente modifica maliciosamente el estado del tablero en el siguiente turno."},
        "Recocido": {"valido": False, "tipo_error": "Paradigma", "mensaje": "Error: Las métricas locales no sirven cuando un oponente modifica maliciosamente el estado del tablero en el siguiente turno."},
        "Minimax": {"valido": True, "mensaje": "Ejecutando Minimax. El árbol de expansión calculará todas las jugadas asumiendo un oponente perfecto."}
    }
}