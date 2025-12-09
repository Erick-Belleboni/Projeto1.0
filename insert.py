import sqlite3

conn = sqlite3.connect("suplementos.db")
cursor = conn.cursor()

produtos = [
    ("Pré-treino Insano", "/static/img/img1.png", "Fórmula concentrada para máximo foco e energia.", 89.90),
    ("Creatina UltraPure", "/static/img/img2.png", "Creatina monohidratada 100% pura.", 59.90),
    ("Whey Protein Prime", "/static/img/img3.png", "Whey concentrado de alta qualidade.", 129.90),
    ("BCAA 4:1:1 Hardcore", "/static/img/img4.png", "Aminoácidos essenciais para recuperação muscular.", 49.90),
    ("Multivitamínico PowerMen", "/static/img/img5.png", "Complexo vitamínico completo.", 39.90),
    ("Hipercalórico Mass Gainer", "/static/img/img6.png", "Alto teor calórico para ganho de massa.", 119.90)
]

cursor.executemany("""
    INSERT INTO produto (nome, img, descricao, preco) 
    VALUES (?, ?, ?, ?)
""", produtos)

conn.commit()
conn.close()

print("Produtos inseridos com sucesso!")
