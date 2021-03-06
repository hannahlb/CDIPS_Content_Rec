import csv
import sqlite3
import time
import datetime
    
from flask import Flask, request, g
from flask import render_template, url_for, redirect
   
DATABASE_LSI = '/var/www/html/flaskapp/Wikipedia-lsi.db'
DATABASE_LDA = '/var/www/html/flaskapp/Wikipedia-lda.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_to_database(db_id):
    if db_id == 0: # LSI
        return sqlite3.connect(app.config['DATABASE_LSI'])
    elif db_id == 1: # LDA
        return sqlite3.connect(app.config['DATABASE_LDA'])
    else:
        print("Wrong db_id\n")
        exit(1)

def get_db(db_id):
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database(db_id)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(db_id, query, args=()):
    cur = get_db(db_id).execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route("/viewdb")
def viewdb():
    db_id = 0
    rows = execute_query(db_id,"""SELECT title, url FROM Wikipedia""")
    return '<a href = "http://ec2-34-212-145-50.us-west-2.compute.amazonaws.com">Go back</a><br>'+'<br>'.join(str(row) for row in rows)

@app.route('/')
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    return render_template("my-form.html") 

@app.route('/result',methods = ['POST', 'GET'])
def result():
    from numpy import random
    if request.method == 'POST':
        # Return 0 or 1 randomly
        db_id = random.randint(0,2)
        # need to make this case insensitive
        title_in = request.form['text']
        rows = execute_query(db_id,"""SELECT * FROM Wikipedia WHERE title =?""",
                             [title_in])
        if not rows:
            return 'Error: This title is not in the database.'+'<br><a href = "http://ec2-34-212-145-50.us-west-2.compute.amazonaws.com">Go back</a>'
        else:
            # save time when user makes a valid query and model used
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            if db_id == 0:
                db_print = 'LSI'
            else:
                db_print = 'LDA'
            with open('/tmp/all_clicks.txt','a') as f:
                f.write(db_print + ' ' + st + ' \n')
            # parse query output    
            titles = rows[0][3] # a string that needs to be parsed
            urls = rows[0][4]   # string
            scores = rows[0][5] # string
            titles = titles.replace('[','').replace(']','').replace('\'','').split(',')
            urls = urls.replace('[','').replace(']','').replace('\'','').replace(' ','').split(',')
            scores = scores.replace('[','').replace(']','').replace(' ','').split(',')
            new_rows = [(title,url,score) for title,url,score in zip(titles,urls,scores)]
            # remove queried item from output list:
            new_rows = [row for row in new_rows if row[0] != title_in]
            return render_template("result.html", rows = new_rows, db_id = db_id)

@app.route("/click_on_url_lsi/<path:wiki_url>")
def click_on_url_lsi(wiki_url):
    wiki_url = wiki_url.replace('https:/en','https://en')
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    #with app.open_resource('static/lsi_clicks.txt') as f:
    #with open(url_for('static',filename='lsi_clicks.txt'),'a') as f:
    #with open('lsi_clicks.txt','a') as f:
    with open('/tmp/lsi_clicks.txt','a') as f:
        f.write(st+' \n')
    return redirect(wiki_url)

@app.route("/click_on_url_lda/<path:wiki_url>")
def click_on_url_lda(wiki_url):
    wiki_url = wiki_url.replace('https:/en','https://en')
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    with open('/tmp/lda_clicks.txt','a') as f:
        f.write(st+' \n')
    return redirect(wiki_url)

if __name__ == '__main__':
    app.run(debug='True')
