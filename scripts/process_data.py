import sqlite3
import pandas as pd

# 1. Conexão/Criação da base de dados local SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 2. Dados de exemplo (imóveis e transações)
data = {
    'bairro': ['Boa Viagem', 'Espinheiro', 'Casa Amarela', 'Graças', 'Parnamirim'],
    'quartos': [3, 2, 2, 3, 2],
    'preco': [750000, 480000, 390000, 580000, 450000],
    'area_m2': [95, 68, 55, 75, 62]
}

# 3. Tratamento com Pandas
df = pd.DataFrame(data)
df['preco_m2'] = (df['preco'] / df['area_m2']).round(2)

# 4. Guardar no SQLite
df.to_sql('imoveis_recife', conn, if_exists='replace', index=False)

# 5. Consulta via SQL para validação
query = "SELECT bairro, preco, preco_m2 FROM imoveis_recife WHERE preco_m2 > 6000"
resultado = pd.read_sql_query(query, conn)

print("--- Imóveis Selecionados (Consulta SQL) ---")
print(resultado)

conn.close()
