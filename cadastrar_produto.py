import sqlite3

def conectar():
    conn = sqlite3.connect("suplementos.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inserir_imagem_galeria(id_produto, img, ordem=1):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO Produto_Galeria (id_produto, img, ordem)
            VALUES (?, ?, ?)
        """, (id_produto, img, ordem))

        conn.commit()
        return True

    except sqlite3.Error as e:
        conn.rollback()
        print("Erro ao inserir imagem:", e)
        return False

    finally:
        conn.close()

inserir_imagem_galeria(1, "/static/img/img1-1.png", 1)
inserir_imagem_galeria(1, "/static/img/img1-2.png", 2)
inserir_imagem_galeria(1, "/static/img/img1-3.png", 3)