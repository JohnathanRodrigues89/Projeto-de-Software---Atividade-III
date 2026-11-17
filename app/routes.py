from datetime import date, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Emprestimo, Livro, Participante

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template(
        "index.html",
        total_livros=Livro.query.count(),
        total_participantes=Participante.query.count(),
        emprestimos_ativos=Emprestimo.query.filter_by(data_devolucao=None).count(),
    )


@bp.route("/livros", methods=["GET", "POST"])
def livros():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        isbn = request.form.get("isbn", "").strip() or None
        categoria = request.form.get("categoria", "").strip() or None
        try:
            quantidade = int(request.form.get("quantidade", "1"))
        except ValueError:
            quantidade = 0

        if not titulo or not autor or quantidade < 1:
            flash("Informe título, autor e uma quantidade maior que zero.", "danger")
        else:
            livro = Livro(
                titulo=titulo,
                autor=autor,
                isbn=isbn,
                categoria=categoria,
                quantidade=quantidade,
            )
            db.session.add(livro)
            try:
                db.session.commit()
                flash("Livro cadastrado com sucesso.", "success")
                return redirect(url_for("main.livros"))
            except IntegrityError:
                db.session.rollback()
                flash("Já existe um livro cadastrado com esse ISBN.", "danger")

    return render_template("livros.html", livros=Livro.query.order_by(Livro.titulo).all())


@bp.post("/livros/<int:livro_id>/excluir")
def excluir_livro(livro_id):
    livro = db.get_or_404(Livro, livro_id)
    if livro.emprestimos:
        flash("Não é possível excluir um livro que possui histórico de empréstimos.", "warning")
    else:
        db.session.delete(livro)
        db.session.commit()
        flash("Livro excluído.", "success")
    return redirect(url_for("main.livros"))


@bp.route("/participantes", methods=["GET", "POST"])
def participantes():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip() or None
        telefone = request.form.get("telefone", "").strip() or None
        if not nome:
            flash("O nome do participante é obrigatório.", "danger")
        else:
            db.session.add(Participante(nome=nome, email=email, telefone=telefone))
            db.session.commit()
            flash("Participante cadastrado com sucesso.", "success")
            return redirect(url_for("main.participantes"))

    return render_template(
        "participantes.html",
        participantes=Participante.query.order_by(Participante.nome).all(),
    )


@bp.post("/participantes/<int:participante_id>/excluir")
def excluir_participante(participante_id):
    participante = db.get_or_404(Participante, participante_id)
    if participante.emprestimos:
        flash("Não é possível excluir participante com histórico de empréstimos.", "warning")
    else:
        db.session.delete(participante)
        db.session.commit()
        flash("Participante excluído.", "success")
    return redirect(url_for("main.participantes"))


@bp.route("/emprestimos", methods=["GET", "POST"])
def emprestimos():
    if request.method == "POST":
        try:
            livro_id = int(request.form.get("livro_id", ""))
            participante_id = int(request.form.get("participante_id", ""))
            prazo = date.fromisoformat(request.form.get("data_prevista_devolucao", ""))
        except (ValueError, TypeError):
            flash("Confira os dados informados para o empréstimo.", "danger")
        else:
            livro = db.session.get(Livro, livro_id)
            participante = db.session.get(Participante, participante_id)
            if not livro or not participante:
                flash("Selecione um livro e um participante válidos.", "danger")
            elif prazo < date.today():
                flash("A data prevista de devolução não pode estar no passado.", "danger")
            elif livro.disponiveis < 1:
                flash("Não há exemplares disponíveis desse livro.", "warning")
            else:
                db.session.add(
                    Emprestimo(
                        livro=livro,
                        participante=participante,
                        data_prevista_devolucao=prazo,
                    )
                )
                db.session.commit()
                flash("Empréstimo registrado com sucesso.", "success")
                return redirect(url_for("main.emprestimos"))

    registros = Emprestimo.query.order_by(Emprestimo.data_emprestimo.desc()).all()
    return render_template(
        "emprestimos.html",
        emprestimos=registros,
        livros=Livro.query.order_by(Livro.titulo).all(),
        participantes=Participante.query.order_by(Participante.nome).all(),
        sugestao_devolucao=date.today() + timedelta(days=7),
    )


@bp.post("/emprestimos/<int:emprestimo_id>/devolver")
def devolver_emprestimo(emprestimo_id):
    emprestimo = db.get_or_404(Emprestimo, emprestimo_id)
    if emprestimo.data_devolucao is None:
        emprestimo.data_devolucao = date.today()
        db.session.commit()
        flash("Devolução registrada.", "success")
    else:
        flash("Este empréstimo já foi devolvido.", "info")
    return redirect(url_for("main.emprestimos"))
