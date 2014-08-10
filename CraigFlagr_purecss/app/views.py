from flask import render_template, request
from app import app
import pymysql as mdb
from model import read_url, flag_score, flag_score_post

db = mdb.connect(user="root", host="localhost", db="Insightdb",
                 charset='utf8')


@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html")

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
        flg_score = flag_score_post(result[2])
        flag_results.append(dict(heading=result[0], flagged_status=result[1],
                                 body=result[2], url=result[3],
                                 flag_score=flg_score))

    flag_results_sorted = sorted(flag_results, key=lambda k: k['flag_score'])
    return render_template('result.html', flag_results=flag_results_sorted,post=post,
                           score=str(score))

