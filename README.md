# Painel de Notas da Turma

Aplicação de linha de comando para consolidar notas escolares em CSV, validar registros, calcular médias e gerar relatórios em texto ou JSON.

## Requisitos

- Python 3.10 ou superior
- Nenhuma dependência externa: o projeto utiliza somente a biblioteca padrão.

## Estrutura

```text
painel-notas/
├── painel/
│   ├── core/       # Entidades, validação e métricas
│   ├── infra/      # Leitura e escrita de arquivos e relatórios
│   ├── services/   # Orquestração do processamento
│   ├── __main__.py
│   └── main.py     # Interface de linha de comando
├── data/           # Pequena base de exemplo
├── tests/          # Testes automatizados
└── README.md
```

## Executar

Na raiz do projeto:

```bash
python -m painel --alunos data/alunos.csv --notas data/notas.csv --config data/config.json --formato texto --output output/
```

Para gerar JSON, troque `--formato texto` por `--formato json`. O programa cria a pasta de saída se ela ainda não existir e grava `relatorio.txt` ou `relatorio.json`, além do log `painel.log`.

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes criam os próprios registros em memória e não dependem dos CSVs da pasta `data/`.

## Regras implementadas

- Espaços nas extremidades dos campos são removidos antes da validação.
- O primeiro cadastro de uma matrícula é mantido; duplicatas posteriores são rejeitadas.
- Cada linha inválida gera um erro com arquivo, linha (cabeçalho = linha 1), tipo e mensagem.
- Registros inválidos não interrompem o processamento das linhas seguintes.
- A média do aluno considera todas as notas válidas; a média por disciplina considera todas as notas válidas daquela disciplina.
- A situação é calculada com a média sem arredondamento; a apresentação usa duas casas decimais.
- `core` não importa `csv`, `json` ou `argparse`.

## Dados oficiais do exercício

Os arquivos de exemplo incluídos aqui são apenas para validar a execução local. Para conferir os totais oficiais do enunciado, substitua-os pelos arquivos `alunos.csv`, `notas.csv` e `config.json` disponibilizados na página do projeto final do curso.
