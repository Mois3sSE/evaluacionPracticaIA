import time
import threading
from Controlador.matriz_compatibilidad import COMPATIBILIDAD

class ControladorProyectoIA: 
    def __init__(self,vista,modelo):
        self.vista = vista
        self.modelo = modelo
        self.matriz = COMPATIBILIDAD
        
    def procesar_peticion(self,problema:str,algoritmo:str) -> None : 
        """Punto de entrada: Se llamara la vsta cuando el usuario de 'Ejecutar'"""
        # Validamos la existencia de la combinacion en el menu 
        if problema not in self.matriz or algoritmo not in self.matriz[problema]: 
            self.vista.mostrar_alerta_educativa("Error",f"Combinacion no configurada: {problema} + {algoritmo}",True)
            return
        config_validacion = self.matriz[problema][algoritmo]
        
        # Manejamos la incompatibilidad de algoritmos 
        if not config_validacion["valido"]: 
            titulo_error = f"Error de {config_validacion['tipo_error']}"
            self.vista.mostrar_alerta_educativa(titulo_error,config_validacion["mensaje"],True)
            return 
        
        # Si es valido , se arrancara el segundo hilo de trabajo 
        self.vista.mostrar_alerta_educativa("Ejecutando", config_validacion["mensaje"],False)
        
        hilo_ia = threading.Thread(
            target=self._ejecutar_ia_en_segundo_plano,
            args=(problema,algoritmo)
        )
        hilo_ia.daemon = True
        hilo_ia.start()
    
    def _ejecutar_ia_en_segundo_plano(self, problema:str, algoritmo:str) -> None : 
        """Hilo para correr las demas actvidades"""
        # Invocamos el contrato de la logica
        resultado = self.modelo.resolver_problemas(problema,algoritmo)
        if resultado["exito"]: 
            for paso in resultado["camino_solucion"]: 
                self.vista.actualizar_tablero(problema,paso)
                time.sleep(0.5)
        else: 
            self.vista.mostrar_alerta_educativa("Fallo", resultado["mensaje"], True)
            
# Zona de pruebas 
class VistaMock:
    def mostrar_alerta_educativa(self, titulo, mensaje, es_error):
        color = "🔴 ROJO" if es_error else "🟢 VERDE"
        print(f"\n[VISTA - PANEL] {color} | {titulo}: {mensaje}")

    def actualizar_tablero(self, problema, estado):
        print(f"   [VISTA - TABLERO] Animando paso de {problema}: {estado}")

class ModeloMock:
    def resolver_problema(self, problema, algoritmo):
        print(f"[MODELO] Calculando {algoritmo} para {problema} (tardará 2 segundos)...")
        time.sleep(2) # Simulando los cálculos matemáticos pesados
        return {
            "exito": True,
            "mensaje": "Solución hallada",
            "camino_solucion": ["Estado 1", "Estado 2", "Estado Final"]
        }

# Zona main 
if __name__ == "__main__": 
    print("--- INICIANDO EL CONTROLADOR DE PRUEBA --- ")
    vista_falsa = VistaMock()
    modelo_falso = ModeloMock()
    controlador = ControladorProyectoIA(vista_falsa, modelo_falso)
    
    #Prueba 1: Error educativo
    print("\n --> PRUEBA 1: Usuario intenta FrozenLake con Minimax")
    controlador.procesar_peticion("FronzenLake","Minimax")
    time.sleep(1)
    
    #Prueba 2: Ejecucion valida 
    print("\n --> PRUEBA 2: Usuario intenta Sokoban con A* ")
    controlador.procesar_peticion("Sokoban","A*")
    
    # Este mensaje demuestra el éxito del Threading:
    # Se imprimirá ANTES de que el algoritmo termine de pensar.
    print("\n[MAIN] La interfaz gráfica sigue viva y respondiendo a clics mientras la IA piensa en el fondo...\n")
        
        