import sqlite3

conn = sqlite3.connect("suplementos.db")
cursor = conn.cursor()

produtos = [
    (
        "Creatina Monohidratada Dark Lab 500g",
        "creatina",
        "/static/img/img1.png",
        "Até 3x sem juros!",
        "A Creatina Monohidratada Dark Lab 500g é a escolha certa para quem busca força, potência e resultados reais. Com creatina pura e de alta qualidade, fornece energia rápida para treinos intensos, melhora o desempenho físico e contribui diretamente para o ganho de massa muscular. Produto aprovado pela ANVISA, com laudo de pureza que garante máxima eficiência e segurança.",
        "120,00",
        "99,90"
    ),
    (
        "Whey Protein Concentrado Prime",
        "whey",
        "/static/img/img2.png",
        "Até 3x sem juros!",
        "O Whey Protein Prime é ideal para quem deseja acelerar a recuperação muscular e aumentar a massa magra. Rico em proteínas de alto valor biológico, auxilia na reconstrução muscular após o treino e contribui para resultados mais rápidos e consistentes.",
        "159,90",
        "129,90"
    ),
    (
        "Pré-Treino Insano Extreme",
        "pre-treino",
        "/static/img/img3.png",
        "Até 3x sem juros!",
        "O Pré-Treino Insano Extreme foi desenvolvido para elevar energia, foco e resistência. Sua fórmula potente combate a fadiga, melhora a concentração e permite treinos mais intensos, com mais força e disposição do início ao fim.",
        "149,90",
        "119,90"
    ),
    (
        "BCAA 4:1:1 Hardcore",
        "bcaa",
        "/static/img/img4.png",
        "Até 3x sem juros!",
        "O BCAA 4:1:1 Hardcore auxilia na recuperação muscular, reduz o catabolismo e melhora a resistência durante os treinos. Ideal para quem treina pesado e busca manter o rendimento sem comprometer a musculatura.",
        "69,90",
        "49,90"
    ),
    (
        "Glutamina Recovery Pro",
        "aminoacido",
        "/static/img/img5.png",
        "Até 3x sem juros!",
        "A Glutamina Recovery Pro é essencial para fortalecer o sistema imunológico e acelerar a recuperação muscular. Ajuda a reduzir o desgaste físico e mantém o corpo preparado para treinos frequentes.",
        "79,90",
        "59,90"
    ),
    (
        "Hipercalórico Mass Gainer",
        "hipercalorico",
        "/static/img/img6.png",
        "Até 3x sem juros!",
        "O Hipercalórico Mass Gainer é indicado para quem tem dificuldade em ganhar peso e massa muscular. Com alto valor calórico e excelente perfil nutricional, contribui para aumento de massa e energia diária.",
        "139,90",
        "109,90"
    ),
    (
        "Multivitamínico Power Men",
        "vitamina",
        "/static/img/img7.png",
        "Até 3x sem juros!",
        "O Multivitamínico Power Men fornece vitaminas e minerais essenciais para a saúde, imunidade e disposição. Ideal para manter o corpo equilibrado e melhorar o desempenho nos treinos e na rotina.",
        "59,90",
        "39,90"
    ),
    (
        "Cafeína Anidra 210mg",
        "estimulante",
        "/static/img/img8.png",
        "Até 3x sem juros!",
        "A Cafeína Anidra 210mg aumenta o estado de alerta, melhora o foco e reduz a fadiga. Perfeita para quem busca mais energia e rendimento físico sem depender de grandes volumes de pré-treino.",
        "49,90",
        "34,90"
    ),
    (
        "Whey Isolado Zero Lactose",
        "whey",
        "/static/img/img9.png",
        "Até 3x sem juros!",
        "O Whey Isolado Zero Lactose é ideal para quem busca proteína de rápida absorção com alta pureza. Auxilia na recuperação muscular e no ganho de massa, sendo perfeito para dietas mais restritas.",
        "189,90",
        "159,90"
    ),
    (
        "Ômega 3 Ultra Pure",
        "omega",
        "/static/img/img10.png",
        "Até 3x sem juros!",
        "O Ômega 3 Ultra Pure auxilia na saúde cardiovascular, articulações e função cerebral. Essencial para quem busca bem-estar, recuperação muscular e suporte geral ao organismo.",
        "79,90",
        "59,90"
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
