import sqlite3

# Cria/liga ao banco de dados local
conn = sqlite3.connect('banco_dados.db')
cursor = conn.cursor()

# Cria uma tabela de teste
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto TEXT,
        valor REAL
    )
''')

# Insere um registo
cursor.execute(
    "INSERT INTO vendas (produto, valor) VALUES ('Curso SQL', 150.0)"
)
conn.commit()

# Consulta e exibe no terminal
cursor.execute('SELECT * FROM vendas')
print(cursor.fetchall())

conn.close()
