import mysql.connector

# Misma configuración que en tu seeder.py
DB_CONFIG = {'host': 'localhost', 'user': 'root', 'password': 'root', 'database': 'ICEBOX'}

def insertar_datos_prueba():
    conexion = mysql.connector.connect(**DB_CONFIG)
    cursor = conexion.cursor()

    try:
        # 1. Usuario
        cursor.execute("INSERT IGNORE INTO usuarios (nombre_usuario, email, password) VALUES (%s, %s, %s)", 
                       ("viajero_test", "test@test.com", "1234"))
        id_usuario = cursor.lastrowid if cursor.lastrowid else 1

        # 2. Viaje
        cursor.execute("INSERT INTO viajes (id_usuario, titulo) VALUES (%s, %s)", (id_usuario, "Mi gran viaje"))
        id_viaje = cursor.lastrowid

        # 3. Parada (Buscamos ID de ciudad Madrid, ESP - ejemplo)
        cursor.execute("SELECT id_ciudad FROM ciudades WHERE nombre = 'Madrid' LIMIT 1")
        id_ciudad = cursor.fetchone()[0]

        cursor.execute("INSERT INTO paradas (id_viaje, id_ciudad, orden_en_ruta, relato_texto) VALUES (%s, %s, %s, %s)",
                       (id_viaje, id_ciudad, 1, "¡La mejor tortilla de patatas en Madrid!"))
        id_parada = cursor.lastrowid

        # 4. Iman
        cursor.execute("INSERT INTO imanes (id_usuario, id_ciudad, id_parada, imagen_url) VALUES (%s, %s, %s, %s)",
                       (id_usuario, id_ciudad, id_parada, "https://example.com/iman_madrid.jpg"))

        # Repetir para otro país (ej: Buenos Aires, ARG)
        cursor.execute("SELECT id_ciudad FROM ciudades WHERE nombre = 'Buenos Aires' LIMIT 1")
        id_ciudad_arg = cursor.fetchone()[0]
        
        cursor.execute("INSERT INTO paradas (id_viaje, id_ciudad, orden_en_ruta, relato_texto) VALUES (%s, %s, %s, %s)",
                       (id_viaje, id_ciudad_arg, 2, "Café, tango y milonga en Buenos Aires."))
        id_parada_arg = cursor.lastrowid
        
        cursor.execute("INSERT INTO imanes (id_usuario, id_ciudad, id_parada, imagen_url) VALUES (%s, %s, %s, %s)",
                       (id_usuario, id_ciudad_arg, id_parada_arg, "https://example.com/iman_ba.jpg"))

        conexion.commit()
        print("✅ Datos de prueba insertados correctamente.")
    except Exception as e:
        print(f"❌ Error: {e}")
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()

if __name__ == '__main__':
    insertar_datos_prueba()