from flask import render_template, request
from app import app
import pymysql as mdb
from model import read_url, flag_score

db = mdb.connect(user="root", host="localhost", db="Insightdb",
                 charset='utf8')


@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html",
                           title='Home', user={'nickname': 'Miguel'},
                           )

@app.route("/result")
def result_page():
    url = request.args.get('url')
    post = read_url(url)
    score = flag_score(url)
    with db:
        cur = db.cursor()
        cur.execute(
            '''
            SELECT heading, flagged_status, body, external_url
            FROM Postings
            GROUP BY id
            LIMIT 5;
            '''
        )
        query_results = cur.fetchall()

    flag_results = []
    for result in query_results:
        flag_results.append(dict(heading=result[0], flagged_status=result[1],
                                 body=result[2], url=result[3]))

    return render_template('result.html', flag_results=flag_results,post=post,
                           score=score)