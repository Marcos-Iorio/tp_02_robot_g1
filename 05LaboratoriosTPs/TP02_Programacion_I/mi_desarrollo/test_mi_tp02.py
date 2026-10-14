from mi_tp02 import (
    comando_es_valido,
    ejecutar_mision,
    generar_reporte,
    motivo_invalido,
)
from misiones import MISION_BASICA, MISION_CON_ERRORES


def test_comandos_validos():
    assert comando_es_valido(("avanzar", 0.2, 2.0))
    assert comando_es_valido(("girar", -0.5, 3.14))
    assert comando_es_valido(("detenerse",))
    assert comando_es_valido(("saludar",))


def test_comando_vacio():
    assert not comando_es_valido(())


def test_comando_inexistente():
    assert not comando_es_valido(("volar", 0.2, 1.0))


def test_cantidad_de_datos_incorrecta():
    assert not comando_es_valido(("avanzar", 0.2))
    assert not comando_es_valido(("avanzar", 0.2, 1.0, 5))
    assert not comando_es_valido(("detenerse", 1))
    assert not comando_es_valido(("saludar", 1))


def test_velocidad_o_tiempo_no_numerico():
    assert not comando_es_valido(("avanzar", "rapido", 2.0))
    assert not comando_es_valido(("girar", 0.5, "mucho"))
    assert not comando_es_valido(("avanzar", None, 2.0))


def test_tiempo_negativo():
    assert not comando_es_valido(("avanzar", 0.2, -3.0))


def test_tiempo_cero_es_valido():
    assert comando_es_valido(("avanzar", 0.2, 0))


def test_no_es_una_tupla():
    assert not comando_es_valido(5)
    assert not comando_es_valido(None)


def test_motivos():
    assert motivo_invalido(()) == "comando vacio"
    assert "no existe" in motivo_invalido(("volar", 0.2, 1.0))
    assert "numero" in motivo_invalido(("avanzar", "rapido", 2.0))
    assert "negativo" in motivo_invalido(("avanzar", 0.2, -3.0))
    assert "necesita" in motivo_invalido(("avanzar", 0.2))


def test_reporte_no_falla():
    historial = [
        {"comando": ("saludar",), "ok": True, "motivo": "saludo"},
        {"comando": ("volar", 1, 1), "ok": False, "motivo": "el comando 'volar' no existe"},
    ]
    generar_reporte(historial)


def test_en_mision_con_errores_hay_4_comandos_mal_formados():
    invalidos = [c for c in MISION_CON_ERRORES if not comando_es_valido(c)]
    assert len(invalidos) == 4
