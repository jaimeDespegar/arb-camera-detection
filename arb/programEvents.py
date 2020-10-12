import sched
import time

# Función que es llamada por los eventos
def abrir_cerrar(estado):
    print('TIEMPO:', int(time.time()))
    if estado:
        print("Abriendo compuertas...")
    else:
        print("Cerrando compuertas...")

# Declarar el programador
programador = sched.scheduler(time.time, time.sleep)

# Asignar el tiempo de comienzo (en segundos)
comienzo = int(time.time())
t1 = comienzo + 1   # Tiempo para abrir compuertas (1")
t2 = t1 + 4         # Tiempo para cerrar compuertas (5")
print('PROGRAMADOR INICIADO:', comienzo)

# Definir los dos eventos indicando: momento de ejecución, 
# prioridad, función a la que se llama y el valor que se
# pasa al argumento de la función:
programador.enterabs(t1, 1, abrir_cerrar, (1,))
programador.enterabs(t2, 1, abrir_cerrar, (0,))

# Poner en marcha el programador.
# El programa permanece a la espera hasta que se
# ejecuten los dos eventos. La ejecución se producirá
# cuando se alcance el momento definido.
programador.run()
print('PROGRAMADOR FINALIZADO:', int(time.time()))