import csv
import sqlite3
    
from flask import Flask, request, g
from flask import render_template, url_for, redirect
    
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
    rows = execute_query("""SELECT itle, url FROM Wikipedia""")
    return '<a href = "http://ec2-34-212-145-50.us-west-2.compute.amazonaws.com">Go back</a><br>'+'<br>'.join(str(row) for row in rows)
                                                                                                                  
@app.route('/')
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    return render_template("my-form.html") 

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        title_in = request.form['text']
        rows = execute_query("""SELECT * FROM Wikipedia WHERE title =?""",
                             [title_in])
        if not rows:
            return 'Error: This title is not in the database.'+'<br><a href = "http://ec2-34-212-145-50.us-west-2.compute.amazonaws.com">Go back</a>'
        else:
            titles = rows[0][3] # a string that needs to be parsed
            urls = rows[0][4]   # string
            scores = rows[0][5] # string
            titles = titles.replace('[','').replace(']','').replace('\'','').split(',')
            urls = urls.replace('[','').replace(']','').replace('\'','').split(',')
            scores = scores.replace('[','').replace(']','').replace(' ','').split(',')
            new_rows = [(title,url,score) for title,url,score in zip(titles,urls,scores)]
            return render_template("result.html",rows = new_rows)


@app.route("/click_on_url/<path:wiki_url>")
def click_on_url(wiki_url):
    return redirect(wiki_url)

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=8000,debug='True')
