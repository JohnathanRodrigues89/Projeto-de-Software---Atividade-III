from datetime import date, timedelta

from app import db
from app.models import Emprestimo, Livro, Participante


def preparar_acervo():
    livro = Livro(titulo="Dom Casmurro", autor="Machado de Assis", quantidade=1)
    participante = Participante(nome="João")
    db.session.add_all([livro, participante])
    db.session.commit()
    return livro.id, participante.id


def test_registrar_emprestimo(client, app):
    with app.app_context():
        livro_id, participante_id = preparar_acervo()
    resposta = client.post("/emprestimos", data={
        "livro_id": str(livro_id),
        "participante_id": str(participante_id),
        "data_prevista_devolucao": (date.today() + timedelta(days=7)).isoformat(),
    }, follow_redirects=True)
    assert resposta.status_code == 200
    with app.app_context():
        assert Emprestimo.query.count() == 1


def test_impedir_emprestimo_sem_exemplar_disponivel(client, app):
    with app.app_context():
        livro_id, participante_id = preparar_acervo()
        db.session.add(Emprestimo(
            livro_id=livro_id,
            participante_id=participante_id,
            data_prevista_devolucao=date.today() + timedelta(days=5),
        ))
        db.session.commit()
    resposta = client.post("/emprestimos", data={
        "livro_id": str(livro_id),
        "participante_id": str(participante_id),
        "data_prevista_devolucao": (date.today() + timedelta(days=7)).isoformat(),
    }, follow_redirects=True)
    assert "Não há exemplares disponíveis" in resposta.get_data(as_text=True)
