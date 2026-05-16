import logging

IDADE_MINIMA = 0
IDADE_MAXIMA = 120
IDADE_CORTE = 16

PESOS_QUALIDADE = {
    "nome": 10,
    "idade": 15,
    "cpf": 40,
    "endereco": 20,
    "data": 15,
}


def configurar_logs(nivel: int = logging.INFO) -> None:
    logging.basicConfig(
        level=nivel,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
