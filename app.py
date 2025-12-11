import flask as fk
from secrets import token_hex
import sqlite3

srv = fk.Flask(__name__)
srv.secret_key = token_hex()


def percorre_email(email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM cliente WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    conn.close()

    return resultado is not None

def cadastrar_cliente(nome,email,senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cliente (nome, email, senha)
        VALUES (?, ?, ?)
    """, (nome, email, senha))

    conn.commit()
    conn.close()

def verifica_login(email, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT email FROM cliente
        WHERE email = ? AND senha = ?
    """, (email, senha))

    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def contar_linhas_tabela(tabela):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    quantidade = cursor.fetchone()[0]
    conn.close()
    return quantidade


@srv.get("/")
def get_home():
    qtd = contar_linhas_tabela("Produto")
    return fk.render_template("home.html", quantidade=qtd)




@srv.get("/base")
def get_base():
   return fk.render_template("base.html")

@srv.get("/login")
def get_login():
    return fk.render_template("login.html")


@srv.post("/login")
def valida_login():
    email = fk.request.form["email"]
    senha = fk.request.form["senha"]

    if verifica_login(email, senha):
        fk.session["login"] = email
        return fk.redirect("/")
    else:
        return fk.redirect("/login")


@srv.get("/cadastro")
def get_cadastro():
   return fk.render_template("cadastro.html")

@srv.post("/cadastro")
def valida_cadastro():
    nome = fk.request.form["nome"]
    email = fk.request.form["email"]
    senha = fk.request.form["senha"]

    if percorre_email(email):
        return fk.render_template("cadastro.html")
    else:
        cadastrar_cliente(nome,email,senha)
        fk.session["login"] = email
        return fk.redirect("/")

    
   
    
@srv.get("/logout")
def get_logout():
    del fk.session["login"]
    return fk.redirect("/")

@srv.get("/favoritos")
def get_favoritos():
    try:
        login = fk.session["login"]
        return fk.render_template("favoritos.html", login=login)
    except KeyError:
        return fk.redirect("login")
        
@srv.get("/carrinho")
def get_carrinho():
    try:
        login = fk.session["login"]
        return fk.render_template("carrinho.html", login=login)
    except KeyError:
        return fk.redirect("login")

@srv.get("/mixes")
def get_mixes():
    try:
        login = fk.session["login"]
        return fk.render_template("mixes.html", login=login)
    except KeyError:
        return fk.redirect("login")


@srv.get("/ingredientes")
def get_ingredientes():
    return fk.render_template("ingredientes.html")

@srv.get("/produtos")
def get_produtos():
   return fk.render_template("produtos.html")

def conectar():
    return sqlite3.connect("suplementos.db")

@srv.route("/produto_item/<int:id_produto>")
def produto(id_produto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produto WHERE id_produto = ?", (id_produto,))
    produto_item = cursor.fetchone()
    conn.close()

    return fk.render_template("produto_item.html", produto_item=produto_item)

if __name__ == "__main__":
    srv.run(host="localhost",port=5050, debug=True)
   