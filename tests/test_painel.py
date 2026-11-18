import json
import tempfile
import unittest
from pathlib import Path

from painel.core.entidades import Aluno, Nota
from painel.core.validador import Validador
from painel.infra.relatorios import RelatorioJSON, RelatorioTexto
from painel.services.processamento import ProcessamentoService


class TestEntidades(unittest.TestCase):
    def test_media_e_situacao(self):
        aluno = Aluno(1, "Ana", "3A", [Nota(1, "Matemática", "P1", 8), Nota(1, "Matemática", "P2", 6)])
        self.assertEqual(aluno.media(), 7)
        self.assertEqual(aluno.situacao(6, 4), "aprovado")

    def test_sem_notas(self):
        aluno = Aluno(1, "Ana", "3A")
        self.assertIsNone(aluno.media())
        self.assertEqual(aluno.situacao(6, 4), "sem_notas")


class TestValidador(unittest.TestCase):
    def setUp(self):
        self.validador = Validador()

    def test_limpa_espacos_e_aceita_aluno(self):
        alunos, erros = self.validador.validar_alunos([{"matricula": " 10 ", "nome": " Ana ", "turma": " 3A "}])
        self.assertEqual((alunos[0].nome, alunos[0].turma), ("Ana", "3A"))
        self.assertEqual(erros, [])

    def test_rejeita_matricula_duplicada_e_campo_vazio(self):
        linhas = [
            {"matricula": "10", "nome": "Ana", "turma": "3A"},
            {"matricula": "10", "nome": "Bia", "turma": "3A"},
            {"matricula": "11", "nome": "", "turma": "3B"},
        ]
        alunos, erros = self.validador.validar_alunos(linhas)
        self.assertEqual(len(alunos), 1)
        self.assertEqual([e.tipo for e in erros], ["matricula_duplicada", "campo_vazio"])
        self.assertEqual([e.linha for e in erros], [3, 4])

    def test_rejeita_valores_nao_finitos(self):
        linhas = [
            {"matricula": "10", "disciplina": "Física", "avaliacao": "P1", "nota": "nan"},
            {"matricula": "10", "disciplina": "Física", "avaliacao": "P2", "nota": "inf"},
        ]
        notas, erros = self.validador.validar_notas(linhas, {10}, 10)
        self.assertEqual(notas, [])
        self.assertEqual([e.tipo for e in erros], ["nota_fora_do_intervalo", "nota_fora_do_intervalo"])

    def test_nota_invalida_fora_intervalo_inexistente_e_duplicada(self):
        linhas = [
            {"matricula": "10", "disciplina": "Matemática", "avaliacao": "P1", "nota": "oito"},
            {"matricula": "10", "disciplina": "Matemática", "avaliacao": "P1", "nota": "11"},
            {"matricula": "99", "disciplina": "Matemática", "avaliacao": "P1", "nota": "8"},
            {"matricula": "10", "disciplina": "Matemática", "avaliacao": "P1", "nota": "8"},
            {"matricula": "10", "disciplina": "Matemática", "avaliacao": "P1", "nota": "7"},
        ]
        notas, erros = self.validador.validar_notas(linhas, {10}, 10)
        self.assertEqual(len(notas), 1)
        self.assertEqual([e.tipo for e in erros], ["nota_invalida", "nota_fora_do_intervalo", "matricula_inexistente", "avaliacao_duplicada"])


class TestProcessamentoRelatorios(unittest.TestCase):
    def test_processa_e_gera_json_e_texto(self):
        alunos = [{"matricula": "1", "nome": "Ana", "turma": "3A"}]
        notas = [
            {"matricula": "1", "disciplina": "Física", "avaliacao": "P1", "nota": "8"},
            {"matricula": "1", "disciplina": "Física", "avaliacao": "P2", "nota": "6"},
        ]
        config = {"media_aprovacao": 6.0, "media_recuperacao": 4.0, "nota_maxima": 10.0}
        resultado = ProcessamentoService().executar(alunos, notas, config)
        dados = json.loads(RelatorioJSON().gerar(resultado))
        texto = RelatorioTexto().gerar(resultado)
        self.assertEqual(dados["alunos"][0]["media"], 7.0)
        self.assertEqual(dados["alunos"][0]["situacao"], "aprovado")
        self.assertIn("Física", texto)
        self.assertIn("Ana", texto)

    def test_situacao_usa_media_sem_arredondar(self):
        aluno = Aluno(1, "Bia", "3A", [Nota(1, "Física", "P1", 5.995)])
        self.assertEqual(aluno.situacao(6.0, 4.0), "recuperação")


if __name__ == "__main__":
    unittest.main()
