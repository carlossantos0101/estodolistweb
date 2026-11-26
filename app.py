from flask import Flask, render_template, request, session, redirect, flash
from database import consultar_tarefas, inserir_tarefa
from datetime import date

# Lista de categorias que aparecem no <select> do formulario.html
CATEGORIAS = ["Escola", "Trabalho", "Projetos", "Pessoal", "Saúde", "Outros"]

# A aplicação precisa ser criada ANTES de usar o decorador @app.route
app = Flask(__name__)                 # cria a aplicação Flask
app.secret_key = "dssenai"            # chave secreta (necessária pra sessão/flash funcionar)


# Dados de acesso do ADMIN (login fixo da aplicação)
ADMIN_EMAIL = "carloseduardo@gmail.com"
ADMIN_SENHA = "123456"

# Função que CONFERE os dados da tarefa e devolve uma lista de erros.
# Lista vazia = tudo certo. Lista com itens = algo errado.
def validar_tarefa(nome, descricao, categoria, prazo, prioridade):
    erros = []
    # Nome: entre 5 e 30 caracteres e nao pode ser so numeros
    if len(nome) < 5 or len(nome) > 30 or nome.isdigit():
        erros.append("Nome: de 5 a 30 caracteres, não só números.")
    # Descricao: no maximo 100 caracteres
    if len(descricao) > 100:
        erros.append("Descrição: no máximo 100 caracteres.")
    # Categoria: entre 5 e 30 caracteres e nao pode ser so numeros
    if len(categoria) < 5 or len(categoria) > 30 or categoria.isdigit():
        erros.append("Categoria: de 5 a 30 caracteres, não só números.")
    # Prioridade: so aceita ALTA, MEDIA ou BAIXA
    if prioridade not in ("ALTA", "MEDIA", "BAIXA"):
        erros.append("Prioridade inválida.")
    # Prazo (data): nao pode ser vazio nem estar no passado
    if not prazo:
        erros.append("Data de prazo é obrigatória.")
    else:
        try:
            data = date.fromisoformat(prazo)   # texto "2026-11-23" vira data
            if data < date.today():            # data menor que hoje = passou
                erros.append("A data de prazo não pode estar no passado.")
        except ValueError:                     # data em formato invalido
            erros.append("Data de prazo inválida.")
    return erros                               # SEMPRE devolve a lista

@app.route("/")  # HomePage - Página Inicial
def home():
    if "login" not in session:                 # se nao estiver logado...
        return redirect("/login")              # ...manda pro login

    # Usuário logado: consulta as tarefas e envia para o template
    tarefas = consultar_tarefas()  # Chama a função consultar_tarefas() do database.py
    return render_template("index.html", tarefas=tarefas)  # Passa a lista de tarefas para o HTML


# -----------------------------------------
# Rota de Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if "login" in session:                     # ja logado? volta pra home
        return redirect("/")

    if request.method == "GET":                # GET = so abrir a pagina
        return render_template("login.html")

    # POST = usuario clicou "Entrar"
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
    if request.method == "GET":                # GET = abrir o formulario
        return render_template("formulario.html", categorias=CATEGORIAS, dados={}, erros=[])

    # --- A partir daqui e POST (usuario clicou Salvar) ---
    # ler o POST aqui (request.form.get le o campo pelo atributo name)
    nome_tarefa = request.form.get("nome_tarefa", "").strip()
    descricao = request.form.get("descricao", "").strip()
    categoria = request.form.get("categoria", "").strip()
    data_prazo = request.form.get("data_prazo", "").strip()
    prioridade = request.form.get("prioridade", "").strip()

    erros = validar_tarefa(nome_tarefa, descricao, categoria, data_prazo, prioridade)  # CHAMA a validacao

    if erros:                                  # se tem erro...
        return render_template("formulario.html", categorias=CATEGORIAS,  # ...volta pro form
                               dados={"nome_tarefa": nome_tarefa, "descricao": descricao,
                                      "categoria": categoria, "data_prazo": data_prazo,
                                      "prioridade": prioridade}, erros=erros)

    if inserir_tarefa(nome_tarefa, descricao, categoria, data_prazo, prioridade):  # tenta salvar
        flash("Tarefa adicionada com sucesso!")      # recado temporario (some no proximo refresh)
    else:
        flash("Não foi possível salvar. Confira a conexão com o banco.")
    return redirect("/")                       # volta pra home

# --------------------------------------
# Tratamento de erro - Código 404
@app.errorhandler(404)
def not_found(erro):
    return render_template("erro404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    # host='0.0.0.0' Habilita o IP Público