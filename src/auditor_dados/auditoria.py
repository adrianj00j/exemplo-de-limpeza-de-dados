import logging

import pandas as pd

from auditor_dados.config import PESOS_QUALIDADE
from auditor_dados.validacao import (
    validar_cpf,
    validar_data,
    validar_endereco,
    validar_idade,
    validar_nome,
)


def classificar_score(score: int) -> str:
    if score >= 90:
        return "Excelente"
    if score >= 70:
        return "Bom"
    if score >= 50:
        return "Ruim"

    return "Critico"


def auditar_linha(row: pd.Series) -> pd.Series:
    score = 100
    motivos: list[str] = []

    if not validar_nome(row.get("nome")):
        score -= PESOS_QUALIDADE["nome"]
        motivos.append("Nome invalido")

    if not validar_idade(row.get("idade")):
        score -= PESOS_QUALIDADE["idade"]
        motivos.append("Idade invalida")

    if not validar_cpf(row.get("cpf")):
        score -= PESOS_QUALIDADE["cpf"]
        motivos.append("CPF invalido")

    if not validar_endereco(row.get("endereco")):
        score -= PESOS_QUALIDADE["endereco"]
        motivos.append("Endereco incompleto")

    if not validar_data(row.get("data")):
        score -= PESOS_QUALIDADE["data"]
        motivos.append("Data invalida")

    status = "Valido" if score >= 70 else "Invalido"

    if any(motivo in motivos for motivo in ["Nome invalido", "Idade invalida", "CPF invalido"]):
        status = "Invalido"

    return pd.Series(
        {
            "score_qualidade": score,
            "status": status,
            "nivel_qualidade": classificar_score(score),
            "motivos": " | ".join(motivos) if motivos else "Dados perfeitos",
        }
    )


def gerar_relatorio(df: pd.DataFrame) -> dict[str, int | float]:
    total = len(df)
    validos = int((df["status"] == "Valido").sum())
    invalidos = total - validos
    score_medio = round(float(df["score_qualidade"].mean()), 2) if total else 0.0

    resumo = {
        "total": total,
        "validos": validos,
        "invalidos": invalidos,
        "score_medio": score_medio,
    }

    logging.info(
        "Relatorio: %s validos / %s invalidos / score medio %.2f",
        validos,
        invalidos,
        score_medio,
    )

    return resumo
