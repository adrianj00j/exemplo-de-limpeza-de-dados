import re

import pandas as pd


def limpar_nome(nome: str) -> str:
    if pd.isna(nome):
        return ""

    nome = str(nome)
    padrao_tratamento = r"^(Dr\.|Dra\.|Sr\.|Sra\.|Srta\.)\s*"
    nome = re.sub(padrao_tratamento, "", nome, flags=re.IGNORECASE)
    nome = re.sub(r"\s+", " ", nome)

    return nome.strip().title()


def limpar_cpf(cpf: str) -> str:
    if pd.isna(cpf):
        return ""

    return re.sub(r"\D", "", str(cpf))


def mascarar_cpf(cpf: str) -> str:
    cpf_limpo = limpar_cpf(cpf)

    if len(cpf_limpo) != 11:
        return "CPF invalido"

    return f"{cpf_limpo[:3]}.***.***-{cpf_limpo[-2:]}"


def limpar_estado(estado: str) -> str:
    if pd.isna(estado):
        return ""

    return str(estado).strip().title()
