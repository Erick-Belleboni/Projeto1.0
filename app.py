import flask as fk
from secrets import token_hex
import sqlite3

srv = fk.Flask(__name__)
srv.secret_key = token_hex()

@srv.get("/")
def get_home():
    return fk.render_template("home.html")

@srv.get("/base")
def get_base():
   return fk.render_template("base.html")

@srv.get("/login")
def get_login():
    return fk.render_template("login.html")


@srv.post("/login")
def valida_login():
    login = fk.request.form["login"]
    senha = fk.request.form["senha"]
    if login=="usuario" and senha=="123":
    # se login válido:
        # inicializa session[
        fk.session["login"] = login
        # redireciona para home.html
        return fk.redirect("/")
    else:
        # se login inválido, volta pra login.html
        return fk.redirect("login")
    
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

@srv.get("/cadastro")
def get_cadastro():
   return fk.render_template("cadastro.html")

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
   