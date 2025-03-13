import os
import urllib
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

server = os.getenv("DB_SERVER")
database = "master"  # Conectar a 'master' para crear la BD
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
driver = os.getenv("DB_DRIVER")

# Conexión inicial a 'master' para crear la base de datos
connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes"
connection_url = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"

engine = create_engine(connection_url, isolation_level="AUTOCOMMIT")  # Permitir crear la BD

# Crear la base de datos si no existe
with engine.connect() as connection:
    connection.execute(text("IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'MigrationDB') CREATE DATABASE MigrationDB;"))

# Ahora, reconectamos a la base de datos 'MigrationDB'
database = "MigrationDB"
connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes"
connection_url = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"

# Crear nueva conexión a MigrationDB
engine = create_engine(connection_url)

# Crear tablas si no existen
with engine.connect() as connection:
    connection.execute(text("""
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'departments')
        CREATE TABLE departments (
            id INT PRIMARY KEY,
            department NVARCHAR(100) NOT NULL
        );

        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'jobs')
        CREATE TABLE jobs (
            id INT PRIMARY KEY,
            job NVARCHAR(100) NOT NULL
        );

        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'hired_employees')
        CREATE TABLE hired_employees (
            id INT PRIMARY KEY,
            name NVARCHAR(200) NOT NULL,
            datetime DATETIME NOT NULL,
            department_id INT NOT NULL,
            job_id INT NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        );
    """))

# Cargar datos desde CSV
csv_folder = "data"

def load_csv_to_db(file_name, table_name, columns):
    file_path = os.path.join(csv_folder, file_name)
    df = pd.read_csv(file_path, names=columns, header=None)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"✅ Datos de {file_name} insertados en {table_name}")

# Cargar los datos desde los archivos CSV
load_csv_to_db("departments.csv", "departments", ["id", "department"])
load_csv_to_db("jobs.csv", "jobs", ["id", "job"])
load_csv_to_db("hired_employees.csv", "hired_employees", ["id", "name", "datetime", "department_id", "job_id"])

print("✅ Base de datos y tablas creadas correctamente, y datos insertados desde CSV.")
