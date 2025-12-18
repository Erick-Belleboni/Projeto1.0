import flask as fk
from secrets import token_hex
import sqlite3

srv = fk.Flask(__name__)
srv.secret_key = token_hex()


# -------------------- BANCO --------------------

def conectar():
    return sqlite3.connect("suplementos.db")


def percorre_email(email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM cliente WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


def cadastrar_cliente(nome, email, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cliente (nome, email, senha) VALUES (?, ?, ?)",
        (nome, email, senha)
    )
    conn.commit()
    conn.close()


def verifica_login(email, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT email FROM cliente WHERE email = ? AND senha = ?",
        (email, senha)
    )
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


def buscar_produtos():
    conn = sqlite3.connect("suplementos.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_produto, nome, descricao, img, preco
        FROM Produto
    """)
    produtos = cursor.fetchall()
    conn.close()
    return produtos


def favoritar(id_cliente, id_produto):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO Favorito (id_cliente, id_produto) VALUES (?, ?)",
            (id_cliente, id_produto)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Erro ao favoritar:", e)
        return False


def desfavoritar(id_cliente, id_produto):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Favorito WHERE id_cliente = ? AND id_produto = ?",
            (id_cliente, id_produto)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Erro ao desfavoritar:", e)
        return False


def get_favoritos(id_cliente):
    """Retorna lista de ids de produtos favoritados pelo cliente"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_produto FROM Favorito WHERE id_cliente = ?", (id_cliente,))
    favoritos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return favoritos


# -------------------- ROTAS --------------------

## Favoritos
@srv.post("/favoritar/<int:id_produto>")
def rota_favoritar(id_produto):
    if "login" not in fk.session:
        return fk.jsonify({"success": False, "msg": "Não logado"}), 401

    email = fk.session["login"]
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente FROM Cliente WHERE email = ?", (email,))
    id_cliente = cursor.fetchone()[0]
    conn.close()

    sucesso = favoritar(id_cliente, id_produto)
    return fk.jsonify({"success": sucesso})


@srv.post("/desfavoritar/<int:id_produto>")
def rota_desfavoritar(id_produto):
    if "login" not in fk.session:
        return fk.jsonify({"success": False, "msg": "Não logado"}), 401

    email = fk.session["login"]
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente FROM Cliente WHERE email = ?", (email,))
    id_cliente = cursor.fetchone()[0]
    conn.close()

    sucesso = desfavoritar(id_cliente, id_produto)
    return fk.jsonify({"success": sucesso})


## Páginas principais
@srv.get("/")
def get_home():
    produtos = buscar_produtos()
    qtd = len(produtos)
    favoritos_list = []

    if "login" in fk.session:
        email = fk.session["login"]
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente FROM Cliente WHERE email = ?", (email,))
        id_cliente = cursor.fetchone()[0]
        conn.close()
        favoritos_list = get_favoritos(id_cliente)

    return fk.render_template(
        "paginas/home.html",
        produtos=produtos,
        quantidade=qtd,
        favoritos=favoritos_list
    )


@srv.get("/base")
def get_base():
    return fk.render_template("paginas/base.html")


@srv.get("/login")
def get_login():
    return fk.render_template("paginas/login.html")


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
    return fk.render_template("paginas/cadastro.html")

@srv.post("/cadastro")
def valida_cadastro():
    nome = fk.request.form["nome"]
    email = fk.request.form["email"]
    senha = fk.request.form["senha"]

    if percorre_email(email):
        return fk.render_template("paginas/cadastro.html")
    else:
        cadastrar_cliente(nome, email, senha)
        fk.session["login"] = email
        return fk.redirect("/")


@srv.get("/logout")
def get_logout():
    fk.session.pop("login", None)
    return fk.redirect("/")


@srv.get("/favoritos")
def get_favoritos_page():
    if "login" not in fk.session:
        return fk.redirect("/login")

    email = fk.session["login"]
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente FROM Cliente WHERE email = ?", (email,))
    id_cliente = cursor.fetchone()[0]
    conn.close()

    favoritos_ids = get_favoritos(id_cliente)
    produtos = [p for p in buscar_produtos() if p["id_produto"] in favoritos_ids]

    return fk.render_template(
        "paginas/favoritos.html",
        produtos=produtos
    )


@srv.get("/carrinho")
def get_carrinho():
    if "login" not in fk.session:
        return fk.redirect("/login")

    return fk.render_template(
        "paginas/carrinho.html",
        login=fk.session["login"]
    )

@srv.route("/adicionar-carrinho", methods=["POST"])
def adicionar_carrinho():
    if "login" not in fk.session:
        return fk.redirect("/login")

    email = fk.session["login"]

    conn = conectar()
    cursor = conn.cursor()

    # cliente
    cursor.execute(
        "SELECT id_cliente FROM Cliente WHERE email = ?",
        (email,)
    )
    row_cliente = cursor.fetchone()
    if not row_cliente:
        conn.close()
        return fk.redirect("/login")

    id_cliente = row_cliente[0]

    produto_id = fk.request.form.get("produto_id")
    quantidade = int(fk.request.form.get("quantidade", 1))

    # carrinho
    cursor.execute(
        "SELECT id_carrinho FROM Carrinho WHERE id_cliente = ?",
        (id_cliente,)
    )
    row_carrinho = cursor.fetchone()

    if row_carrinho:
        id_carrinho = row_carrinho[0]
    else:
        cursor.execute(
            "INSERT INTO Carrinho (id_cliente) VALUES (?)",
            (id_cliente,)
        )
        id_carrinho = cursor.lastrowid

    # produto
    cursor.execute(
        "SELECT preco FROM Produto WHERE id_produto = ?",
        (produto_id,)
    )
    row_produto = cursor.fetchone()
    if not row_produto:
        conn.close()
        return fk.redirect("/")

    preco_unitario = float(row_produto[0])

    # item
    cursor.execute("""
        INSERT INTO Carrinho_Item
        (id_carrinho, tipo_item, id_produto, quantidade, preco_unitario)
        VALUES (?, 'produto', ?, ?, ?)
    """, (id_carrinho, produto_id, quantidade, preco_unitario))

    conn.commit()
    conn.close()

    return fk.redirect("/carrinho")


@srv.get("/ingredientes")
def get_ingredientes():
    return fk.render_template("paginas/ingredientes.html")


@srv.get("/produtos")
def get_produtos():
    return fk.render_template("paginas/produtos.html")


@srv.get("/produto_item/<int:id_produto>")
def produto(id_produto):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Produto WHERE id_produto = ?",
        (id_produto,)
    )
    produto = cursor.fetchone()

    cursor.execute(
        "SELECT img FROM Produto_Galeria WHERE id_produto = ? ORDER BY ordem",
        (id_produto,)
    )
    imagens = cursor.fetchall()

    conn.close()

    return fk.render_template(
        "paginas/produto_item.html",
        produto=produto,
        imagens=imagens
    )

# -------------------- START --------------------

if __name__ == "__main__":
    srv.run(host="localhost", port=5050, debug=True)
