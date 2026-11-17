from app import db
from app.models import Participante


def test_cadastrar_participante(client, app):
    resposta = client.post("/participantes", data={
        "nome": "Maria da Silva",
        "email": "maria@example.com",
        "telefone": "83999990000",
    }, follow_redirects=True)
    assert resposta.status_code == 200
    with app.app_context():
        assert Participante.query.count() == 1
        assert Participante.query.first().nome == "Maria da Silva"
