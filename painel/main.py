import argparse
import logging
from pathlib import Path

from .infra.arquivos import ler_csv, ler_json, escrever_texto
from .infra.relatorios import RelatorioJSON, RelatorioTexto
from .services.processamento import ProcessamentoService


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Consolida notas escolares e gera relatórios.")
    parser.add_argument("--alunos", required=True, help="Caminho do CSV de alunos")
    parser.add_argument("--notas", required=True, help="Caminho do CSV de notas")
    parser.add_argument("--config", required=True, help="Caminho do JSON de configuração")
    parser.add_argument("--formato", choices=("texto", "json"), default="texto")
    parser.add_argument("--output", default="output/", help="Diretório dos relatórios")
    return parser


def main() -> None:
    args = criar_parser().parse_args()
    pasta_saida = Path(args.output)
    pasta_saida.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=pasta_saida / "painel.log", level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s", encoding="utf-8",
    )
    try:
        logging.info("Iniciando processamento")
        linhas_alunos = ler_csv(args.alunos)
        linhas_notas = ler_csv(args.notas)
        config = ler_json(args.config)
        resultado = ProcessamentoService().executar(linhas_alunos, linhas_notas, config)
        relatorios = {"texto": RelatorioTexto(), "json": RelatorioJSON()}
        relatorio = relatorios[args.formato].gerar(resultado)
        extensao = "txt" if args.formato == "texto" else "json"
        escrever_texto(pasta_saida / f"relatorio.{extensao}", relatorio)
        logging.info("Processamento concluído: %s alunos, %s notas válidas, %s erros", len(resultado["alunos"]), len(resultado["notas"]), len(resultado["erros_alunos"]) + len(resultado["erros_notas"]))
        print(relatorio)
    except (OSError, ValueError, KeyError) as erro:
        logging.exception("Falha no processamento")
        raise SystemExit(f"Erro: {erro}") from erro
