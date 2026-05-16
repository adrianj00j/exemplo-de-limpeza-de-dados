import logging
from datetime import date
from pathlib import Path

import pandas as pd

from auditor_dados.auditoria import auditar_linha, gerar_relatorio
from auditor_dados.limpeza import limpar_cpf, limpar_estado, limpar_nome, mascarar_cpf


def calcular_idade(data_nascimento, referencia: date | None = None) -> int | None:
    data_convertida = pd.to_datetime(data_nascimento, errors="coerce", dayfirst=True)

    if pd.isna(data_convertida):
        return None

    referencia = referencia or date.today()
    nascimento = data_convertida.date()
    idade = referencia.year - nascimento.year

    if (referencia.month, referencia.day) < (nascimento.month, nascimento.day):
        idade -= 1

    return idade


def corrigir_idade_por_data(df: pd.DataFrame) -> pd.DataFrame:
    if "data" not in df.columns:
        return df

    df = df.copy()
    df["data"] = pd.to_datetime(df["data"], errors="coerce", dayfirst=True)

    if "idade" not in df.columns:
        df["idade"] = pd.NA
    else:
        df["idade"] = pd.to_numeric(df["idade"], errors="coerce")

    corrigidos = 0

    for index, row in df.iterrows():
        idade_calculada = calcular_idade(row["data"])

        if idade_calculada is None:
            continue

        if pd.isna(row["idade"]) or row["idade"] != idade_calculada:
            df.at[index, "idade"] = idade_calculada
            corrigidos += 1

    if corrigidos:
        logging.info("Idades corrigidas com base na data de nascimento: %s", corrigidos)

    return df


def limpar_e_auditar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "nome" in df.columns:
        df["nome"] = df["nome"].apply(limpar_nome)

    if "estado" in df.columns:
        df["estado"] = df["estado"].apply(limpar_estado)

    if "cpf" in df.columns:
        df["cpf"] = df["cpf"].apply(limpar_cpf)
        df["cpf_mascarado"] = df["cpf"].apply(mascarar_cpf)

    df = corrigir_idade_por_data(df)

    colunas_auditoria = df.apply(auditar_linha, axis=1)
    df = pd.concat([df, colunas_auditoria], axis=1)

    if "cpf_mascarado" in df.columns:
        df["cpf"] = df["cpf_mascarado"]
        df = df.drop(columns=["cpf_mascarado"])

    return df.sort_values(by="score_qualidade", ascending=False)


def processar_csv(
    caminho_entrada: str | Path,
    caminho_saida: str | Path,
    caminho_invalidos: str | Path | None = None,
) -> dict[str, int | float]:
    caminho_entrada = Path(caminho_entrada)
    caminho_saida = Path(caminho_saida)
    caminho_invalidos = Path(caminho_invalidos) if caminho_invalidos else caminho_saida.parent / "clientes_invalidos.csv"

    logging.info("Lendo arquivo: %s", caminho_entrada)
    df = pd.read_csv(caminho_entrada)

    resultado = limpar_e_auditar(df)
    resumo = gerar_relatorio(resultado)

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    caminho_invalidos.parent.mkdir(parents=True, exist_ok=True)

    resultado[resultado["status"] == "Valido"].to_csv(caminho_saida, index=False)
    resultado[resultado["status"] == "Invalido"].to_csv(caminho_invalidos, index=False)

    logging.info("Clientes validos salvos em: %s", caminho_saida)
    logging.info("Clientes invalidos salvos em: %s", caminho_invalidos)

    return resumo
