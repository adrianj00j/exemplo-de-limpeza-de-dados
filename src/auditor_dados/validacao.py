import re

import pandas as pd

from auditor_dados.config import IDADE_CORTE, IDADE_MAXIMA
from auditor_dados.limpeza import limpar_cpf


def validar_nome(nome: str) -> bool:
    if pd.isna(nome):
        return False

    nome = str(nome).strip()

    if len(nome) < 2 or len(nome) > 50:
        return False

    if re.search(r"(.)\1{3,}", nome, flags=re.IGNORECASE):
        return False

    return bool(re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome))


def validar_idade(idade) -> bool:
    try:
        idade_float = float(idade)
    except (TypeError, ValueError):
        return False

    return IDADE_CORTE <= idade_float <= IDADE_MAXIMA


def validar_data(data) -> bool:
    data_convertida = pd.to_datetime(data, errors="coerce", dayfirst=True)
    return pd.notna(data_convertida)


def validar_endereco(endereco: str) -> bool:
    if pd.isna(endereco):
        return False

    linhas = [parte.strip() for parte in str(endereco).splitlines() if parte.strip()]
    return len(linhas) >= 3


def validar_cpf(cpf: str) -> bool:
    cpf_limpo = limpar_cpf(cpf)

    if len(cpf_limpo) != 11:
        return False

    if cpf_limpo == cpf_limpo[0] * 11:
        return False

    soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10

    soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10

    return int(cpf_limpo[9]) == digito1 and int(cpf_limpo[10]) == digito2
