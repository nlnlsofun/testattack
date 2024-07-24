from flask import Flask, request, render_template, g
import sqlite3

app = Flask(__name__)

DATABASE = 'test.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            comment TEXT NOT NULL)''')
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comment', methods=['POST'])
def comment():
    name = request.form['name']
    comment = request.form['comment']

    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, comment) VALUES (?, ?)", (name, comment))
    db.commit()

    return f'感謝您的評論, {name}! 評論內容: {comment}'

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')

    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT name, comment FROM users WHERE comment LIKE '%{query}%'")
    results = cursor.fetchall()

    response = '<h2>搜索結果</h2>'
    for name, comment in results:
        response += f'<p><b>{name}</b>: {comment}</p>'
    
    return response

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
