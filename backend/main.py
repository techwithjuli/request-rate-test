from flask import Flask, request, jsonify
import requests
import psycopg2

app = Flask(__name__)

# Datenbankverbindung (Postgres)
# Hostname "db" kommt aus docker-compose
db_config = {
    'host': 'db',
    'dbname': 'example_db',
    'user': 'example',
    'password': 'example'
}

# Hilfsfunktion zum Erstellen einer Tabelle (falls nicht vorhanden)
def init_db():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id SERIAL PRIMARY KEY,
            text VARCHAR(255),
            category VARCHAR(50)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route('/api/data', methods=['POST'])
def receive_data():
    input_text = request.form.get('inputText')
    if not input_text:
        return "Fehlender 'inputText' im Formular.", 400

    try:
        # An Middleware schicken zur Kategorisierung
        response = requests.post("http://middleware:6000/categorize", json={
            "inputText": input_text
        })
        if response.status_code != 200:
            return "Fehler in Middleware-Antwort", 500

        category = response.json().get("category", "Unkown")

        # In Datenbank speichern
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        insert_query = "INSERT INTO requests (text, category) VALUES (%s, %s);"
        cur.execute(insert_query, (input_text, category))
        conn.commit()
        cur.close()
        conn.close()

        return f"Eingegangen und gespeichert: '{input_text}' mit Kategorie '{category}'", 200

    except Exception as e:
        return f"Fehler bei der Verarbeitung: {str(e)}", 500

@app.route('/api/entries', methods=['GET'])
def get_entries():
    # Liefert alle Einträge aus der DB
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT id, text, category FROM requests;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        data = [
            {"id": r[0], "text": r[1], "category": r[2]}
            for r in rows
        ]
        return jsonify(data), 200

    except Exception as e:
        return f"Fehler beim Lesen aus der DB: {str(e)}", 500

if __name__ == '__main__':
    # Debug nur lokal, für Produktion besser gunicorn usw. nutzen
    app.run(host='0.0.0.0', port=5000, debug=True)