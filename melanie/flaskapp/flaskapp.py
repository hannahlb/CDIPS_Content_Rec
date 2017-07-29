import csv
import sqlite3
    
from flask import Flask, request, g
from flask import render_template
    
DATABASE = '/var/www/html/flaskapp/wikisearch.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT title, url FROM wikisearch""")
    return '<a href = "http://ec2-34-212-145-50.us-west-2.compute.amazonaws.com">Go back</a><br>'+'<br>'.join(str(row) for row in rows)
                                                                                                                  
@app.route('/')
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    id_in = request.form['text']
    rows = execute_query("""SELECT * FROM wikisearch WHERE title = ?""",
                         [id_in.title()])
    return '<br>'.join(str(row) for row in rows)

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        title_in = request.form['text']
        rows = execute_query("""SELECT * FROM wikisearch WHERE title =?""",
                             [title_in.title()])
    return render_template("result.html",rows = rows)

if __name__ == '__main__':
    app.run()
