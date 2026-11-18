from abc import ABC, abstractmethod
import json
from ..core.metricas import media_por_disciplina, resumo


class GeradorRelatorio(ABC):
    @abstractmethod
    def gerar(self, resultado: dict) -> str:
        raise NotImplementedError


class RelatorioTexto(GeradorRelatorio):
    def gerar(self, resultado: dict) -> str:
        totais = resumo(resultado["alunos"], resultado["notas"], resultado["erros_alunos"], resultado["erros_notas"])
        linhas = [
            "PAINEL DE NOTAS — RESUMO",
            f"Alunos processados: {totais['alunos_processados']}",
            f"Registros de nota válidos: {totais['notas_validas']} | inválidos: {totais['notas_invalidas']}",
            "", "Situação dos alunos",
        ]
        cfg = resultado["config"]
        for aluno in resultado["alunos"]:
            media = aluno.media()
            media_txt = f"{media:.2f}" if media is not None else "sem notas"
            situacao = aluno.situacao(cfg["media_aprovacao"], cfg["media_recuperacao"])
            linhas.append(f"  {aluno.nome:<22} {aluno.turma:<5} média {media_txt}  {situacao}")
        linhas.extend(["", "Média por disciplina"])
        for disciplina, media in media_por_disciplina(resultado["notas"]).items():
            linhas.append(f"  {disciplina:<18} {media:.2f}")
        todos_erros = resultado["erros_alunos"] + resultado["erros_notas"]
        linhas.extend(["", f"Erros encontrados ({len(todos_erros)})"])
        for erro in todos_erros:
            linhas.append(f"  {erro.arquivo}:{erro.linha} [{erro.tipo}] {erro.mensagem}")
        return "\n".join(linhas) + "\n"


class RelatorioJSON(GeradorRelatorio):
    def gerar(self, resultado: dict) -> str:
        cfg = resultado["config"]
        alunos = []
        for aluno in resultado["alunos"]:
            media = aluno.media()
            alunos.append({
                "matricula": aluno.matricula,
                "nome": aluno.nome,
                "turma": aluno.turma,
                "media": round(media, 2) if media is not None else None,
                "situacao": aluno.situacao(cfg["media_aprovacao"], cfg["media_recuperacao"]),
            })
        notas_disciplina = media_por_disciplina(resultado["notas"])
        dados = {
            "resumo": resumo(resultado["alunos"], resultado["notas"], resultado["erros_alunos"], resultado["erros_notas"]),
            "alunos": alunos,
            "medias_por_disciplina": {k: round(v, 2) for k, v in notas_disciplina.items()},
            "erros": [e.como_dict() for e in resultado["erros_alunos"] + resultado["erros_notas"]],
        }
        return json.dumps(dados, ensure_ascii=False, indent=2) + "\n"
