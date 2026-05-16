from auditor_dados.validacao import (
    validar_cpf,
    validar_data,
    validar_endereco,
    validar_idade,
    validar_nome,
)


def test_validar_cpf_valido():
    assert validar_cpf("529.982.247-25")


def test_validar_cpf_invalido():
    assert not validar_cpf("111.111.111-11")


def test_validar_nome_valido_com_acento():
    assert validar_nome("Joao Silva")
    assert validar_nome("Maria Goncalves")


def test_validar_nome_invalido_com_numeros():
    assert not validar_nome("Ana 123")


def test_validar_idade_respeita_corte_minimo():
    assert validar_idade(16)
    assert not validar_idade(15)


def test_validar_endereco_exige_tres_linhas():
    assert validar_endereco("Rua A\nCentro\nCidade / UF")
    assert not validar_endereco("Rua A")


def test_validar_data_rejeita_valor_invalido():
    assert validar_data("1991-02-10")
    assert not validar_data("nao e uma data")
