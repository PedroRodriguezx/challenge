import requests
import psycopg2

# Configurações de conexão ao banco de dados
conn = psycopg2.connect(
    dbname="mydatabase",
    user="myuser",
    password="mypassword",
    host="db",
    port="5432"
)

# Cria um cursor
cur = conn.cursor()

# Cria as tabelas
cur.execute("""
CREATE TABLE IF NOT EXISTS country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    iso3_code VARCHAR(3) UNIQUE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS gdp (
    country_id INT,
    year INT,
    value NUMERIC,
    PRIMARY KEY (country_id, year),
    FOREIGN KEY (country_id) REFERENCES country(id)
)
""")

# Função para obter dados da API
def get_gdp_data():
    url = "https://api.worldbank.org/v2/country/ARG;BOL;BRA;CHL;COL;ECU;GUY;PRY;PER;SUR;URY;VEN/indicator/NY.GDP.MKTP.CD?format=json&page=1&per_page=50"
    response = requests.get(url)
    data = response.json()
    return data[1] if len(data) > 1 else []

# Extrair dados
data = get_gdp_data()

# Inserir dados nas tabelas
countries = {}
for record in data:
    country_name = record['country']['value']
    iso3_code = record['countryiso3code']
    year = int(record['date'])
    value = float(record['value']) if record['value'] is not None else None
    
    if iso3_code not in countries:
        cur.execute("INSERT INTO country (name, iso3_code) VALUES (%s, %s) ON CONFLICT (iso3_code) DO NOTHING RETURNING id", (country_name, iso3_code))
        country_id = cur.fetchone()
        if country_id:
            countries[iso3_code] = country_id[0]
        else:
            cur.execute("SELECT id FROM country WHERE iso3_code = %s", (iso3_code,))
            countries[iso3_code] = cur.fetchone()[0]

    if value is not None:
        cur.execute("INSERT INTO gdp (country_id, year, value) VALUES (%s, %s, %s) ON CONFLICT (country_id, year) DO NOTHING", (countries[iso3_code], year, value))

# Confirmar a transação
conn.commit()

# Fechar a conexão
cur.close()
conn.close()
