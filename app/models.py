from datetime import date

from app import db


class Livro(db.Model):
    __tablename__ = "livros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    categoria = db.Column(db.String(80), nullable=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    emprestimos = db.relationship("Emprestimo", back_populates="livro")

    @property
    def disponiveis(self):
        ativos = sum(1 for emprestimo in self.emprestimos if emprestimo.data_devolucao is None)
        return max(self.quantidade - ativos, 0)


class Participante(db.Model):
    __tablename__ = "participantes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    telefone = db.Column(db.String(30), nullable=True)

    emprestimos = db.relationship("Emprestimo", back_populates="participante")


class Emprestimo(db.Model):
    __tablename__ = "emprestimos"

    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey("livros.id"), nullable=False)
    participante_id = db.Column(
        db.Integer, db.ForeignKey("participantes.id"), nullable=False
    )
    data_emprestimo = db.Column(db.Date, nullable=False, default=date.today)
    data_prevista_devolucao = db.Column(db.Date, nullable=False)
    data_devolucao = db.Column(db.Date, nullable=True)

    livro = db.relationship("Livro", back_populates="emprestimos")
    participante = db.relationship("Participante", back_populates="emprestimos")

    @property
    def esta_atrasado(self):
        return (
            self.data_devolucao is None
            and self.data_prevista_devolucao < date.today()
        )
