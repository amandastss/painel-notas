from collections import defaultdict
from .entidades import Aluno, Nota


def media_por_disciplina(notas: list[Nota]) -> dict[str, float]:
    valores: dict[str, list[float]] = defaultdict(list)
    for nota in notas:
        valores[nota.disciplina].append(nota.nota)
    return {disciplina: sum(lista) / len(lista) for disciplina, lista in sorted(valores.items())}


def resumo(alunos: list[Aluno], notas: list[Nota], erros_alunos: list, erros_notas: list) -> dict:
    return {
        "alunos_processados": len(alunos),
        "notas_validas": len(notas),
        "notas_invalidas": len(erros_notas),
        "erros_total": len(erros_alunos) + len(erros_notas),
    }
