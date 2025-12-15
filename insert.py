import sqlite3

conn = sqlite3.connect("suplementos.db")
cursor = conn.cursor()

produtos = [
    ("Pré-treino Insano", "pre-treino", "/static/img/img1.png", "Fórmula concentrada para máximo foco e energia.", 89.90),
    ("Creatina UltraPure", "creatina", "/static/img/img2.png", "Creatina monohidratada 100% pura.", 59.90),
    ("Whey Protein Prime", "whey", "/static/img/img3.png", "Whey concentrado de alta qualidade.", 129.90),
    ("BCAA 4:1:1 Hardcore", "bcaa", "/static/img/img4.png", "Aminoácidos essenciais para recuperação muscular.", 49.90),
    ("Multivitamínico PowerMen", "vitamina", "/static/img/img5.png", "Complexo vitamínico completo.", 39.90),
    ("Hipercalórico Mass Gainer", "hipercalorico", "/static/img/img6.png", "Alto teor calórico para ganho de massa.", 119.90),
    ("Whey Isolado Zero Lactose", "whey", "/static/img/img7.png", "Whey isolado com rápida absorção.", 159.90),
    ("Creatina Creapure", "creatina", "/static/img/img8.png", "Creatina alemã com selo Creapure.", 79.90),
    ("BCAA Drink Lemon", "bcaa", "/static/img/img9.png", "BCAA em pó sabor limão.", 54.90),
    ("Pré-treino Focus Pro", "pre-treino", "/static/img/img10.png", "Energia limpa sem crash.", 94.90),
    ("Glutamina Recovery", "aminoacido", "/static/img/img11.png", "Auxilia na recuperação muscular.", 44.90)
]


cursor.executemany("""
    INSERT INTO produto (nome, tipo, img, descricao, preco) 
    VALUES (?, ?, ?, ?, ?)
""", produtos)

conn.commit()
conn.close()

print("Produtos inseridos com sucesso!")
