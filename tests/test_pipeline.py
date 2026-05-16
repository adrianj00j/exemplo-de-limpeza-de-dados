import pandas as pd

from auditor_dados.pipeline import calcular_idade, limpar_e_auditar


def test_calcular_idade_com_data_de_referencia():
    assert calcular_idade("10/02/1991", referencia=pd.Timestamp("2026-05-16").date()) == 35


def test_limpar_e_auditar_mascara_cpf_e_cria_status():
    df = pd.DataFrame(
        [
            {
                "nome": "Sr. Joao Silva",
                "idade": 34,
                "data": "1991-02-10",
                "endereco": "Rua A\nCentro\nCidade / UF",
                "estado": "mato grosso",
                "cpf": "529.982.247-25",
            }
        ]
    )

    resultado = limpar_e_auditar(df)

    assert resultado.loc[0, "nome"] == "Joao Silva"
    assert resultado.loc[0, "cpf"] == "529.***.***-25"
    assert resultado.loc[0, "status"] == "Valido"
