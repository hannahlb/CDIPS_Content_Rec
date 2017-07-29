import csv
import sqlite3

from flask import Flask, request, g
from flask import render_template

#DATABASE = '/var/www/html/flaskapp/Wikipedia-sims-hdp.db'
DATABASE = '/Users/rangel/CDIPS_Content_Rec/Tonatiuh/flaskapp/Wikipedia-lsi.db'

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
    rows = execute_query("""SELECT * FROM Wikipedia""")
    return '<br>'.join(str(row) for row in rows)

@app.route('/')
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['GET','POST'])
def my_form_post():
    id_in = request.form['text']
    rows = execute_query("""SELECT other_titles, other_urls,scores FROM Wikipedia WHERE id =  ?""",
                         [id_in.title()])
    return render_template("my-form.html", headers = rows)


if __name__ == '__main__':
	app.run(debug=True)
