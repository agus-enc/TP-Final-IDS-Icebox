from flask import Flask, render_template

app = Flask(__name__)

@app.route('/heladera')
def mostrar_heladera():
    # Nos aseguramos de que todos tengan una posición inicial válida desde acá
    viajes_prueba = [
        {"id": 1, "destino": "Bariloche ❄️", "posicion_x": 60, "posicion_y": 80, "fecha": "Ene 2024"},
        {"id": 2, "destino": "Mendoza 🍷", "posicion_x": 240, "posicion_y": 170, "fecha": "Mar 2025"},
        {"id": 3, "destino": "Salta 🌵", "posicion_x": 420, "posicion_y": 100, "fecha": "Oct 2023"}
    ]
    return render_template('heladera.html', viajes=viajes_prueba)

if __name__ == '__main__':
    app.run(debug=True, port=8000)