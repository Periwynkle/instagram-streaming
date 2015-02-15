import sqlite3
import json

from flask import Flask, request, g

DATABASE = './instagram.db'
DEBUG = True
SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    if request.method == 'POST':
        g.db.execute('insert into posts (text) values (?)', [request.get_data()])
        g.db.commit()
        return ""
    else:
        return request.args.get("hub.challenge", "")

@app.route('/show')
def show():
    cur = g.db.execute('select text from posts order by id desc')
    return str([row for row in cur.fetchall()])

if __name__ == "__main__":
    app.run()
