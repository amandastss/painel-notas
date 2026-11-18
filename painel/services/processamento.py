from ..core.validador import Validador


class ProcessamentoService:
    def __init__(self, validador: Validador | None = None):
        self.validador = validador or Validador()

    def executar(self, linhas_alunos: list[dict], linhas_notas: list[dict], config: dict) -> dict:
        alunos, erros_alunos = self.validador.validar_alunos(linhas_alunos)
        matriculas = {aluno.matricula for aluno in alunos}
        notas, erros_notas = self.validador.validar_notas(linhas_notas, matriculas, config["nota_maxima"])
        por_matricula = {aluno.matricula: aluno for aluno in alunos}
        for nota in notas:
            por_matricula[nota.matricula].notas.append(nota)
        return {
            "alunos": alunos,
            "notas": notas,
            "erros_alunos": erros_alunos,
            "erros_notas": erros_notas,
            "config": config,
        }
