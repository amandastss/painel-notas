from dataclasses import dataclass, field


@dataclass
class Aluno:
    matricula: int
    nome: str
    turma: str
    notas: list["Nota"] = field(default_factory=list)

    def media(self) -> float | None:
        if not self.notas:
            return None
        return sum(n.nota for n in self.notas) / len(self.notas)

    def situacao(self, media_aprovacao: float, media_recuperacao: float) -> str:
        media = self.media()
        if media is None:
            return "sem_notas"
        if media >= media_aprovacao:
            return "aprovado"
        if media >= media_recuperacao:
            return "recuperação"
        return "reprovado"


@dataclass(frozen=True)
class Nota:
    matricula: int
    disciplina: str
    avaliacao: str
    nota: float


@dataclass(frozen=True)
class Erro:
    arquivo: str
    linha: int
    tipo: str
    mensagem: str

    def como_dict(self) -> dict:
        return {
            "arquivo": self.arquivo,
            "linha": self.linha,
            "tipo": self.tipo,
            "mensagem": self.mensagem,
        }
