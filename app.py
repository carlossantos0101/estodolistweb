from flask import Flask, render_template, request, session, redirect, flash
from database import consultar_tarefas, inserir_tarefa
from datetime import date

CATEGORIAS = ["Escola", "Trabalho", "Projetos", "Pessoal", "Saúde", "Outros"]

# A aplicação precisa ser criada ANTES de usar o decorador @app.route
app = Flask(__name__)
app.secret_key = "dssenai"


# Dados de acesso do ADMIN
ADMIN_EMAIL = "carloseduardo@gmail.com"
ADMIN_SENHA = "123456"


@app.route("/")  # HomePage - Página Inicial
def home():
    if "login" not in session:
        return redirect("/login")

    # Usuário logado: consulta as tarefas e envia para o template
    tarefas = consultar_tarefas()  # Chama a função consultar_tarefas() do database.py
    return render_template("index.html", tarefas=tarefas)  # Passa a lista de tarefas para o HTML




# -----------------------------------------
# Rota de Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if "login" in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")

    # POST
    email = request.form.get("email")  # Pegando o email que estava no form HTML
    senha = request.form.get("senha")  # Essa informação está no atributo name

    if email == ADMIN_EMAIL and senha == ADMIN_SENHA:
        session["login"] = True  # Cria a sessão login
        return redirect("/")  # Redireciona para a rota inicial
    else:
        return render_template("login.html", msgerro="E-mail ou senha estão incorretos!")


# ----------------------
# Rota Logout
@app.route("/logout")
def logout():
    session.clear()  # Apaga a lista sessão
    return redirect("/login")

# -----------------------------------------
# Rota para adicionar tarefa
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "GET":
        return render_template("formulario.html", categorias=CATEGORIAS, dados={}, erros=[])

    # ler o POST aqui
    nome_tarefa = request.form.get("nome_tarefa", "").strip()
    descricao = request.form.get("descricao", "").strip()
    categoria = request.form.get("categoria", "").strip()
    data_prazo = request.form.get("data_prazo", "").strip()
    prioridade = request.form.get("prioridade", "").strip()

    erros = []
    if not nome_tarefa:
        erros.append("O nome da tarefa é obrigatório.")
    if not categoria:
        erros.append("A categoria é obrigatória.")
    if not data_prazo:
        erros.append("A data de prazo é obrigatória.")
    if not prioridade:
        erros.append("A prioridade é obrigatória.")

    if erros:
        return render_template("formulario.html", categorias=CATEGORIAS,
                               dados={"nome_tarefa": nome_tarefa, "descricao": descricao,
                                      "categoria": categoria, "data_prazo": data_prazo,
                                      "prioridade": prioridade}, erros=erros)

    if inserir_tarefa(nome_tarefa, descricao, categoria, data_prazo, prioridade):
        flash("Tarefa adicionada com sucesso!")
    else:
        flash("Não foi possível salvar. Confira a conexão com o banco.")
    return redirect("/")

# --------------------------------------
# Tratamento de erro - Código 404
@app.errorhandler(404)
def not_found(erro):
    return render_template("erro404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    # host='0.0.0.0' Habilita o IP Público