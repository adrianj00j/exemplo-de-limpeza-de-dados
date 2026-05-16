# Auditor de Dados

Projeto exemplo em Python para limpar, validar e auditar uma base simples de clientes em CSV.

Ele nasceu de um script único (`teste1.py`) e foi organizado em uma estrutura mais adequada para publicar no GitHub: módulos separados, testes automatizados, dados de exemplo e uma interface de linha de comando.

## Aviso sobre os dados

A base `data/clientes.csv` foi criada com a biblioteca Faker. Os nomes, CPFs, enderecos e demais informacoes sao ficticios e foram usados apenas para fins de estudo e demonstracao. Nenhum dado pessoal real deve ser usado neste projeto.

## O que o projeto faz

- Limpa nomes, estados e CPFs.
- Mascara CPF antes de exportar os resultados.
- Valida nome, idade, CPF, endereco e data de nascimento.
- Calcula um score de qualidade para cada registro.
- Separa registros validos e invalidos em arquivos CSV.

> Este projeto tem finalidade didatica. Ele serve como exemplo de organizacao de codigo e pipeline com Pandas, nao como solucao completa de governanca de dados.

## Estrutura

```text
auditor_dados/
├── data/
│   └── clientes.csv
├── outputs/
│   └── .gitkeep
├── src/
│   └── auditor_dados/
│       ├── auditoria.py
│       ├── cli.py
│       ├── config.py
│       ├── limpeza.py
│       ├── pipeline.py
│       └── validacao.py
├── tests/
│   ├── test_pipeline.py
│   └── test_validacao.py
├── main.py
├── pyproject.toml
└── README.md
```

## Como rodar

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependencias:

```bash
pip install -e ".[dev]"
```

Execute com os dados de exemplo:

```bash
python main.py
```

Ou use o modulo/CLI:

```bash
python -m auditor_dados --entrada data/clientes.csv --saida outputs/clientes_validados.csv
```

## Rodando os testes

```bash
pytest
```

## Formato esperado do CSV

O CSV pode conter as colunas abaixo:

- `nome`
- `idade`
- `data`
- `endereco`
- `estado`
- `pais`
- `cpf`

As colunas principais para a auditoria sao `nome`, `idade`, `data`, `endereco` e `cpf`.
