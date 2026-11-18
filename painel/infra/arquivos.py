import csv
import json
from pathlib import Path


def ler_csv(caminho: str | Path) -> list[dict]:
    with Path(caminho).open("r", encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def ler_json(caminho: str | Path) -> dict:
    with Path(caminho).open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    for campo in ("media_aprovacao", "media_recuperacao", "nota_maxima"):
        if campo not in dados:
            raise ValueError(f"Configuração ausente: {campo}")
        dados[campo] = float(dados[campo])
    if dados["nota_maxima"] <= 0 or dados["media_recuperacao"] > dados["media_aprovacao"]:
        raise ValueError("Configuração de médias ou nota máxima inválida")
    return dados


def escrever_texto(caminho: str | Path, conteudo: str) -> None:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")


def escrever_json(caminho: str | Path, dados: dict) -> None:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
