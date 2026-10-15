# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  .....................................
#  Comision:           .....................................
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    try:
        if len(comando) == 0:
            return False
        nombre = comando[0]
        if nombre in ("detenerse", "saludar"):
            return len(comando) == 1
        if nombre in ("avanzar", "girar"):
            if len(comando) != 3:
                return False
            velocidad, tiempo = comando[1], comando[2]
            float(velocidad)
            return float(tiempo) >= 0
        return False
    except (TypeError, ValueError):
        return False


def motivo_invalido(comando):
    """Explica en un texto por que un comando no es valido."""
    try:
        if len(comando) == 0:
            return "comando vacio"
        nombre = comando[0]
        if nombre in ("detenerse", "saludar"):
            return f"'{nombre}' no lleva datos"
        if nombre not in ("avanzar", "girar"):
            return f"el comando '{nombre}' no existe"
        if len(comando) != 3:
            return f"'{nombre}' necesita velocidad y tiempo ({len(comando) - 1} datos recibidos)"
        for etiqueta, valor in (("velocidad", comando[1]), ("tiempo", comando[2])):
            try:
                float(valor)
            except (TypeError, ValueError):
                return f"la {etiqueta} tiene que ser un numero"
        if float(comando[2]) < 0:
            return "el tiempo no puede ser negativo"
    except TypeError:
        return "el comando no es una tupla valida"
    return "comando invalido"


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    nombre = comando[0]
    if nombre == "avanzar":
        robot.avanzar(velocidad=float(comando[1]), tiempo=float(comando[2]))
        return f"avanzo a {comando[1]} m/s durante {comando[2]} s"
    if nombre == "girar":
        robot.girar(velocidad=float(comando[1]), tiempo=float(comando[2]))
        return f"giro a {comando[1]} rad/s durante {comando[2]} s"
    if nombre == "detenerse":
        robot.detenerse()
        return "se detuvo"
    robot.saludar()
    return "saludo"


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """

    for comando in mision:
        if not comando_es_valido(comando):
            historial.append(
                {"comando": comando, "ok": False, "motivo": motivo_invalido(comando)})
            continue
        try:
            resultado = ejecutar_comando(robot, comando)
            historial.append({"comando": comando, "ok": True, "motivo": resultado})
        except ErrorDeSeguridad as error:
            historial.append({"comando": comando, "ok": False, "motivo": f"rechazado por seguridad: {error}"})
        except NotImplementedError as error:
            historial.append(
                {"comando": comando, "ok": False,
                 "motivo": f"el robot no soporta el comando: {error}"})
        except Exception as error:
            historial.append(
                {"comando": comando, "ok": False,
                 "motivo": f"error inesperado: {error}"})


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    ok = [h for h in historial if h["ok"]]
    rechazados = [h for h in historial if not h["ok"]]

    print("=" * 50)
    print("REPORTE DE LA MISION")
    print("=" * 50)
    print(f"Comandos ejecutados correctamente: {len(ok)}")
    print(f"Comandos rechazados: {len(rechazados)}")
    if rechazados:
        print("-" * 50)
        print("Motivos de rechazo:")
        for h in rechazados:
            print(f"  {h['comando']} -> {h['motivo']}")
    print("=" * 50)


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        misiones = {
            "1": ("Mision basica", MISION_BASICA),
            "2": ("Mision con errores", MISION_CON_ERRORES),
            "3": ("Mision cuadrado", MISION_CUADRADO),
        }

        print("Misiones disponibles:")
        for opcion, (nombre, _) in misiones.items():
            print(f"  {opcion}. {nombre}")

        eleccion = input("Elegi una mision: ").strip()
        while eleccion not in misiones:
            eleccion = input("Opcion invalida. Elegi 1, 2 o 3: ").strip()

        nombre, mision = misiones[eleccion]
        print(f"Ejecutando: {nombre}")
        ejecutar_mision(robot, mision, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
