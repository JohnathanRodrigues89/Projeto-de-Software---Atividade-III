from app import db
from app.models import Livro


def test_cadastrar_livro(client, app):
    resposta = client.post("/livros", data={
        "titulo": "O Pequeno Príncipe",
        "autor": "Antoine de Saint-Exupéry",
        "isbn": "9780000000001",
        "categoria": "Literatura",
        "quantidade": "2",
    }, follow_redirects=True)
    assert resposta.status_code == 200
    assert "Livro cadastrado com sucesso" in resposta.get_data(as_text=True)
    with app.app_context():
        assert Livro.query.count() == 1


def test_nao_cadastrar_livro_sem_titulo(client):
    resposta = client.post("/livros", data={
        "titulo": "", "autor": "Autor", "quantidade": "1"
    }, follow_redirects=True)
    assert "Informe título, autor" in resposta.get_data(as_text=True)
