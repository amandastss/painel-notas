# Painel de Notas da Turma

Aplicação em Python para consolidar notas escolares a partir de arquivos CSV, validar registros, calcular médias e gerar relatórios em texto ou JSON.

O projeto utiliza apenas a biblioteca padrão do Python. Não precisa instalar dependências externas.

## Requisitos

- Python 3.10 ou superior.

## Como executar

Na raiz do repositório, execute:

```bash
python -m painel \
  --alunos data/alunos.csv \
  --notas data/notas.csv \
  --config data/config.json \
  --formato json \
  --output output/
```

Para gerar o relatório em texto, troque `--formato json` por `--formato texto`.

O diretório informado em `--output` é criado automaticamente. O programa grava nele o relatório (`relatorio.json` ou `relatorio.txt`) e o arquivo de log `painel.log`.

## Dados de entrada

Os arquivos em `data/` são os dados oficiais fornecidos no enunciado do projeto:

- `alunos.csv`: matrícula, nome e turma;
- `notas.csv`: matrícula, disciplina, avaliação e nota;
- `config.json`: média para aprovação, média para recuperação e nota máxima.

Os dados contêm registros inválidos intencionalmente. O programa registra os erros com o nome do arquivo, a linha (contando o cabeçalho como linha 1) e o tipo de problema, sem interromper o processamento. Em caso de duplicata, mantém o primeiro registro válido. Espaços extras nas extremidades dos campos são removidos antes da validação.

Com os arquivos oficiais, o resultado esperado é:

- 32 alunos processados;
- 457 notas válidas;
- 27 registros de nota rejeitados;
- 30 erros no total, incluindo os erros encontrados em `alunos.csv`.

A situação de cada aluno é calculada usando a média sem arredondamento. Os relatórios exibem as médias com duas casas decimais.

## Testes

Execute a suíte com:

```bash
python -m unittest discover -s tests -v
```

Os testes usam dados criados em memória e não dependem dos CSVs oficiais.

## Organização

```text
painel/
├── __main__.py
├── main.py
├── core/
│   ├── entidades.py
│   ├── validador.py
│   └── metricas.py
├── infra/
│   ├── arquivos.py
│   └── relatorios.py
└── services/
    └── processamento.py
data/
tests/
README.md
```

- `core/`: entidades, regras de validação e cálculos;
- `infra/`: leitura e escrita de CSV/JSON e geração dos relatórios;
- `services/`: coordenação do fluxo de processamento;
- `main.py`: interface de linha de comando com `argparse` e registro de execução com `logging`.

Os relatórios em texto e JSON implementam a mesma interface abstrata `GeradorRelatorio`, permitindo selecionar o formato por polimorfismo.
