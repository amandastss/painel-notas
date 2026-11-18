import math

from .entidades import Aluno, Erro, Nota


class Validador:
    """Valida registros sem interromper o processamento do arquivo."""

    def validar_alunos(self, linhas: list[dict], arquivo: str = "alunos.csv") -> tuple[list[Aluno], list[Erro]]:
        alunos: list[Aluno] = []
        erros: list[Erro] = []
        matriculas: set[int] = set()

        for numero, linha in enumerate(linhas, start=2):
            matricula_txt = (linha.get("matricula") or "").strip()
            nome = (linha.get("nome") or "").strip()
            turma = (linha.get("turma") or "").strip()

            if not matricula_txt or not nome or not turma:
                erros.append(Erro(arquivo, numero, "campo_vazio", "campo obrigatório vazio"))
                continue
            if not matricula_txt.isdigit():
                erros.append(Erro(arquivo, numero, "matricula_invalida", f"matrícula inválida ({matricula_txt})"))
                continue
            matricula = int(matricula_txt)
            if matricula in matriculas:
                erros.append(Erro(arquivo, numero, "matricula_duplicada", f"matrícula {matricula} já cadastrada"))
                continue

            matriculas.add(matricula)
            alunos.append(Aluno(matricula=matricula, nome=nome, turma=turma))
        return alunos, erros

    def validar_notas(
        self, linhas: list[dict], matriculas_validas: set[int], nota_maxima: float,
        arquivo: str = "notas.csv",
    ) -> tuple[list[Nota], list[Erro]]:
        notas: list[Nota] = []
        erros: list[Erro] = []
        chaves: set[tuple[int, str, str]] = set()

        for numero, linha in enumerate(linhas, start=2):
            matricula_txt = (linha.get("matricula") or "").strip()
            disciplina = (linha.get("disciplina") or "").strip()
            avaliacao = (linha.get("avaliacao") or "").strip()
            nota_txt = (linha.get("nota") or "").strip()

            if not matricula_txt or not disciplina or not avaliacao or not nota_txt:
                erros.append(Erro(arquivo, numero, "campo_vazio", "campo obrigatório vazio"))
                continue
            try:
                valor = float(nota_txt.replace(",", "."))
            except ValueError:
                erros.append(Erro(arquivo, numero, "nota_invalida", f"nota inválida ({nota_txt!r})"))
                continue
            if not math.isfinite(valor) or valor < 0 or valor > nota_maxima:
                erros.append(Erro(arquivo, numero, "nota_fora_do_intervalo", f"nota {valor:g} fora do intervalo permitido"))
                continue
            if not matricula_txt.isdigit() or int(matricula_txt) not in matriculas_validas:
                erros.append(Erro(arquivo, numero, "matricula_inexistente", f"matrícula inexistente ({matricula_txt})"))
                continue
            matricula = int(matricula_txt)
            chave = (matricula, disciplina.casefold(), avaliacao.casefold())
            if chave in chaves:
                erros.append(Erro(arquivo, numero, "avaliacao_duplicada", "avaliação já lançada para esta matrícula e disciplina"))
                continue

            chaves.add(chave)
            notas.append(Nota(matricula, disciplina, avaliacao, valor))
        return notas, erros
