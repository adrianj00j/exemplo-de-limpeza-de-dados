import argparse
from pathlib import Path

from auditor_dados.config import configurar_logs
from auditor_dados.pipeline import processar_csv


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Limpa, valida e audita uma base de clientes em CSV.",
    )
    parser.add_argument(
        "--entrada",
        default="data/clientes.csv",
        help="Caminho do CSV de entrada.",
    )
    parser.add_argument(
        "--saida",
        default="outputs/clientes_validados.csv",
        help="Caminho do CSV com os registros validos.",
    )
    parser.add_argument(
        "--invalidos",
        default="outputs/clientes_invalidos.csv",
        help="Caminho do CSV com os registros invalidos.",
    )
    return parser


def main() -> None:
    configurar_logs()
    args = criar_parser().parse_args()

    resumo = processar_csv(
        caminho_entrada=Path(args.entrada),
        caminho_saida=Path(args.saida),
        caminho_invalidos=Path(args.invalidos),
    )

    print("Resumo do processamento")
    print(f"Total: {resumo['total']}")
    print(f"Validos: {resumo['validos']}")
    print(f"Invalidos: {resumo['invalidos']}")
    print(f"Score medio: {resumo['score_medio']}")
