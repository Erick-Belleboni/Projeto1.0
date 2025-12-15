import sqlite3

# Conexão com o banco (cria se não existir)
conn = sqlite3.connect("suplementos.db")
cursor = conn.cursor()

# ============================
# TABELAS
# ============================


# 1) CLIENTE
cursor.execute("""
CREATE TABLE IF NOT EXISTS Cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);
""")

# 2) ENDERECO
cursor.execute("""
CREATE TABLE IF NOT EXISTS Endereco (
    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    rua TEXT NOT NULL,
    numero TEXT,
    bairro TEXT,
    cidade TEXT,
    estado TEXT,
    cep TEXT,
    complemento TEXT,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);
""")

# 3) INGREDIENTE
cursor.execute("""
CREATE TABLE IF NOT EXISTS Ingrediente (
    id_ingrediente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco_por_unidade REAL NOT NULL,
    unidade TEXT NOT NULL -- ex: 'g', 'ml'
);
""")

# 4) MIX personalizado (cabeçalho)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Mix (
    id_mix INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    nome_mix TEXT,
    preco_total REAL NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);
""")

# 5) Ingredientes dentro do MIX
cursor.execute("""
CREATE TABLE IF NOT EXISTS Mix_Ingrediente (
    id_mix INTEGER NOT NULL,
    id_ingrediente INTEGER NOT NULL,
    quantidade REAL NOT NULL,
    subtotal REAL NOT NULL,
    PRIMARY KEY (id_mix, id_ingrediente),
    FOREIGN KEY (id_mix) REFERENCES Mix(id_mix),
    FOREIGN KEY (id_ingrediente) REFERENCES Ingrediente(id_ingrediente)
);
""")

# 6) Produto pronto da loja
cursor.execute("""
CREATE TABLE IF NOT EXISTS Produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    img TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL
);
""")

# 7) Carrinho
cursor.execute("""
CREATE TABLE IF NOT EXISTS Carrinho (
    id_carrinho INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);
""")

# 8) Itens do carrinho (Produtos prontos OU mixes)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Carrinho_Item (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_carrinho INTEGER NOT NULL,
    tipo_item TEXT NOT NULL,  -- 'produto' ou 'mix'
    id_produto INTEGER,
    id_mix INTEGER,
    quantidade INTEGER NOT NULL DEFAULT 1,
    preco_unitario REAL NOT NULL,
    FOREIGN KEY (id_carrinho) REFERENCES Carrinho(id_carrinho),
    FOREIGN KEY (id_produto) REFERENCES ProdutoPronto(id_produto),
    FOREIGN KEY (id_mix) REFERENCES Mix(id_mix)
);
""")

# 9) Pedido
cursor.execute("""
CREATE TABLE IF NOT EXISTS Pedido (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_endereco INTEGER NOT NULL,
    valor_total REAL NOT NULL,
    forma_pagamento TEXT NOT NULL, -- 'cartao', 'pix', 'dinheiro'
    status TEXT DEFAULT 'Pendente',
    data DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    FOREIGN KEY (id_endereco) REFERENCES Endereco(id_endereco)
);
""")

# 10) Itens do pedido
cursor.execute("""
CREATE TABLE IF NOT EXISTS Pedido_Item (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL,
    tipo_item TEXT NOT NULL, -- 'produto' ou 'mix'
    id_produto INTEGER,
    id_mix INTEGER,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido),
    FOREIGN KEY (id_produto) REFERENCES ProdutoPronto(id_produto),
    FOREIGN KEY (id_mix) REFERENCES Mix(id_mix)
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Favorito (
    id_favorito INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    FOREIGN KEY (id_produto) REFERENCES Produto(id_produto),
    UNIQUE(id_cliente, id_produto) -- evita duplicados
);
""")
conn.commit()
conn.close()

print("Banco criado com sucesso!")
