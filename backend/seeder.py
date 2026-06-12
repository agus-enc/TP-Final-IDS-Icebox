import json
import mysql.connector
import os

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'ICEBOX'),
    'charset': 'utf8mb4'
}

def poblar_base_de_datos():
    conexion = None
    cursor = None
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()

        cursor.execute('SELECT COUNT(*) FROM paises')
        if cursor.fetchone()[0] > 0:
            print("✔ Las tablas ya están pobladas. Omitiendo el seeder.")
            return

        print("Abriendo archivos JSON...")
        with open('countries.json', 'r', encoding='utf-8') as f:
            countries_data = json.load(f)['data']

        with open('cities.json', 'r', encoding='utf-8') as f:
            cities_data = json.load(f)['data']

        print("Fase 1: Insertando países...")

        sql_pais = """INSERT INTO paises (nombre, bandera, codigo)
                      VALUES (%s, %s, %s)
                      ON DUPLICATE KEY UPDATE bandera = VALUES(bandera), codigo = VALUES(codigo)
                   """

        for country in countries_data:
            nombre = country.get('name', '')
            bandera = country.get('flag', '')
            codigo = country.get('iso3', '')

            cursor.execute(sql_pais, (nombre[:100], bandera[:255], codigo[:3]))

        conexion.commit()

        mapa_paises = {}
        cursor.execute("SELECT nombre, id_pais FROM paises;")

        for (nombre_db, id_pais_db) in cursor.fetchall():
            mapa_paises[nombre_db] = id_pais_db

        print(f"Países insertados con éxito.")
        print("Fase 2: Insertando ciudades (esto puede tardar unos segundos)...")

        sql_ciudad = "INSERT IGNORE INTO ciudades (id_pais, nombre) VALUES (%s, %s)"

        ciudades_insertadas = 0
        ciudades_omitidas = 0

        for country_block in cities_data:
            nombre_pais_json = country_block.get('country')
            lista_ciudades = country_block.get('cities', [])

            # Buscamos si el país de cities.json existe en countries.json
            if nombre_pais_json in mapa_paises:
                valores_batch = []
                ciudades_vistas = set()
                id_pais_fk = mapa_paises[nombre_pais_json]

                for ciudad in lista_ciudades:
                    ciudad_limpia = ciudad.strip()
                    if ciudad_limpia not in ciudades_vistas:
                        ciudades_vistas.add(ciudad_limpia)
                        valores_batch.append((id_pais_fk, ciudad_limpia[:100]))

                if valores_batch:
                    cursor.executemany(sql_ciudad, valores_batch)
                    ciudades_insertadas += cursor.rowcount
                    conexion.commit()
            else:
                ciudades_omitidas += len(lista_ciudades)

        print(f"{ciudades_insertadas} ciudades vinculadas e insertadas con éxito.")

        if ciudades_omitidas > 0:
            print(
                f"Nota: Se omitieron {ciudades_omitidas} ciudades porque el nombre de su país en cities.json no coincidía exactamente con el de countries.json.")

    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
        if conexion:
            conexion.rollback()
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        print("Conexión cerrada.")


if __name__ == '__main__':
    poblar_base_de_datos()