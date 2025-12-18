import sqlite3

conn = sqlite3.connect("suplementos.db")
cursor = conn.cursor()

produtos = [
    (
        "Creatina Monohidratada Dark Lab 500g",
        "creatina",
        "/static/img/img1.png",
        "Até 3x sem juros!",
        "A Creatina Monohidratada Dark Lab 500g é a escolha certa para quem busca força, potência e resultados reais. Com creatina pura e de alta qualidade, fornece energia rápida para treinos intensos, melhora o desempenho físico e contribui diretamente para o ganho de massa muscular.",
        120.00,
        99.90
    ),
    (
        "Whey Protein Concentrado Prime",
        "whey",
        "/static/img/img2.png",
        "Até 3x sem juros!",
        "O Whey Protein Prime é ideal para quem deseja acelerar a recuperação muscular e aumentar a massa magra.",
        159.90,
        129.90
    ),
    (
        "Pré-Treino Insano Extreme",
        "pre-treino",
        "/static/img/img3.png",
        "Até 3x sem juros!",
        "O Pré-Treino Insano Extreme foi desenvolvido para elevar energia, foco e resistência.",
        149.90,
        119.90
    ),
    (
        "BCAA 4:1:1 Hardcore",
        "bcaa",
        "/static/img/img4.png",
        "Até 3x sem juros!",
        "O BCAA 4:1:1 Hardcore auxilia na recuperação muscular.",
        69.90,
        49.90
    ),
    (
        "Glutamina Recovery Pro",
        "aminoacido",
        "/static/img/img5.png",
        "Até 3x sem juros!",
        "A Glutamina Recovery Pro é essencial para fortalecer o sistema imunológico.",
        79.90,
        59.90
    ),
    (
        "Hipercalórico Mass Gainer",
        "hipercalorico",
        "/static/img/img6.png",
        "Até 3x sem juros!",
        "O Hipercalórico Mass Gainer é indicado para quem tem dificuldade em ganhar peso.",
        139.90,
        109.90
    ),
    (
        "Multivitamínico Power Men",
        "vitamina",
        "/static/img/img7.png",
        "Até 3x sem juros!",
        "O Multivitamínico Power Men fornece vitaminas e minerais essenciais.",
        59.90,
        39.90
    ),
    (
        "Cafeína Anidra 210mg",
        "estimulante",
        "/static/img/img8.png",
        "Até 3x sem juros!",
        "A Cafeína Anidra 210mg aumenta o estado de alerta.",
        49.90,
        34.90
    ),
    (
        "Whey Isolado Zero Lactose",
        "whey",
        "/static/img/img9.png",
        "Até 3x sem juros!",
        "O Whey Isolado Zero Lactose é ideal para dietas restritas.",
        189.90,
        159.90
    ),
    (
        "Ômega 3 Ultra Pure",
        "omega",
        "/static/img/img10.png",
        "Até 3x sem juros!",
        "O Ômega 3 Ultra Pure auxilia na saúde cardiovascular.",
        79.90,
        59.90
    )
]

cursor.executemany("""
    INSERT INTO Produto (
        nome,
        tipo,
        img,
        descricao,
        descricao2,
        sub_preco,
        preco
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", produtos)

conn.commit()
conn.close()

print("10 produtos inseridos com sucesso!")
