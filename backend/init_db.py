import os
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root', 
    'charset': 'utf8mb4'
}

def inicializar_estructura():
    print("🛠️ Conectando a MySQL para crear la estructura...")
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()

        ruta_sql = 'db/init.sql' if os.path.exists('db/init.sql') else 'db/icebox.sql'

        if not os.path.exists(ruta_sql):
            print(f"❌ Error: No se encontró el archivo SQL en '{ruta_sql}'")
            return

        print(f"🏗️ Ejecutando comandos de '{ruta_sql}'...")
        with open(ruta_sql, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Separamos el archivo entero usando el punto y coma ';'
        comandos = sql_script.split(';')

        for comando in comandos:
            comando_limpio = comando.strip()
            
            # Solo ejecutamos si el comando no quedó vacío y no es un comentario puro de SQL
            if comando_limpio and not comando_limpio.startswith('--') and not comando_limpio.startswith('/*'):
                cursor.execute(comando_limpio)
                
        conexion.commit()
        print("¡Estructura de base de datos y usuario administrador creados con éxito!")

    except mysql.connector.Error as err:
        print(f"❌ Error al inicializar las tablas: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

if __name__ == '__main__':
    inicializar_estructura()