from scripts.info import mensajes
from scripts.cargar_datos import obtener_tickers_sp500_wiki
from scripts import entrenar_modelo
from scripts import evaluar_modelo
from scripts import predecir_per
import subprocess
import sys

# tf.get_logger().setLevel('ERROR') # evita errores minimos de tensorflow

def main():
    while True:
        mensajes()
        print("\n=== MENÚ ===")
        print("1. Cargar datos")
        print("2. Entrenar modelo")
        print("3. Evaluar modelo")
        print("4. Predecir PER")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            subprocess.run([sys.executable, "scripts/cargar_datos.py"])
        elif opcion == "2":
            subprocess.run([sys.executable, "scripts/entrenar_modelo.py"])
        elif opcion == "3":
            evaluar_modelo()
        elif opcion == "4":
            predecir_per()
        elif opcion == "5":
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    import sys
    print(sys.executable)
    main()