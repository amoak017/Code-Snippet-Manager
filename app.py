from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('snippets.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            language TEXT,
            tags TEXT,
            code TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/snippets', methods=['GET'])
def get_snippets():
    conn = sqlite3.connect('snippets.db')
    c = conn.cursor()
    c.execute("SELECT * FROM snippets")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/snippets', methods=['POST'])
def add_snippet():
    data = request.json
    conn = sqlite3.connect('snippets.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO snippets (title, language, tags, code) VALUES (?, ?, ?, ?)",
        (data['title'], data['language'], data['tags'], data['code'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Snippet added!"})

@app.route('/snippets/<int:id>', methods=['DELETE'])
def delete_snippet(id):
    conn = sqlite3.connect('snippets.db')
    c = conn.cursor()
    c.execute("DELETE FROM snippets WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)