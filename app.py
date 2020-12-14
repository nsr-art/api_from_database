from flask import Flask
from flask import Response
from flask import request
from flask import g
import json
import MySQLdb

app = Flask(__name__)

@app.before_request
def db_connect():
    g.conn = MySQLdb.connect(host='34.87.24.61',
                                user='nsr-admin',
                                passwd='natthapon024299',
                                db='smart_home')
    g.cursor = g.conn.cursor()

@app.after_request
def db_disconnect(response):
    g.cursor.close()
    g.conn.close()
    return response

def query_db(query, args=(), one=False):
    g.cursor.execute(query, args)
    rv = [dict((g.cursor.description[idx][0], value)
    for idx, value in enumerate(row)) for row in g.cursor.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/dht11",methods=['GET'])    # work 1 select from each room 
def dht11():
    result = query_db("SELECT temperature,humidity FROM dht11 where room_id = 1 order by id desc limit 1")
    data = json.dumps(result)
    resp = Response(data, status=200)
    return resp

@app.route('/pm')
def pm():
    result = query_db("SELECT * from bu_pm order by id desc limit 1")
    data = json.dumps(result)
    resp = Response(data, status=200)
    return resp

@app.route('/covid')
def covid():
    result = query_db("SELECT * from covid19_thai order by id desc limit 1")
    data = json.dumps(result)
    resp = Response(data, status=200)
    return resp

@app.route('/ldr')
def ldr():
    result = query_db("SELECT value from ldr where room_id = 1 order by id desc limit 1")
    data = json.dumps(result)
    resp = Response(data, status=200)
    return resp

@app.route('/mq2')
def mq2():
    result = query_db("SELECT value from mq2 where room_id = 1 order by id desc limit 1")
    data = json.dumps(result)
    resp = Response(data, status=200)
    return resp

if __name__ == '__main__':
    app.run(debug=True,port=8000)