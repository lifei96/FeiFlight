# -*- coding:utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash, g

import mysql.connector
import json

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'database16'

Connection = mysql.connector.connect(host='localhost', port=3306, user='database16', password='database16', database='FeiFlight')

def get_model(table_name, attributes, sql_override=None):
    def func(id):
        if (id == None): return None

        cursor = Connection.cursor()
        cursor.execute(sql_override if sql_override is not None else 'SELECT ' + ','.join(attributes) + ' FROM ' + table_name + ' WHERE id=%s', [id])
        result = cursor.fetchall()
        if len(result) == 0:
            return None
        else:
            ret = {}
            for i in range(0, len(attributes)):
                ret[attributes[i]] = result[0][i]

            return ret

    return func

get_user = get_model('users', ['id', 'email', 'name', 'password', 'user_type'])

def get_authed_user():
    return get_user(session.get('user_id', None))

@app.before_request
def before_request():
    g.authedUser = get_authed_user()
    g.url_path = request.path

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/login.html', methods=["POST"])
def login_post():
    email = request.form['email']
    password = request.form['password']
    cursor = Connection.cursor()
    cursor.execute('SELECT id, password, name FROM users WHERE email=%s', [email])

    result = cursor.fetchall()
    print(result)
    if len(result) == 0:
        flash(u"The user does not exist!", 'error')
        return redirect('/login.html')

    if password != result[0][1]:
        flash(u"Wrong password!", 'error')
        return redirect('/login.html')

    session['user_id'] = result[0][0]
    print('Success')
    return redirect('/index.html')

@app.route('/logout.html')
def page_logout():
    del session['user_id']
    return redirect('/index.html')

@app.route('/sign-up.html')
def sign_up():
    return render_template('sign-up.html')

@app.route('/sign-up.html', methods=["POST"])
def sign_up_post():
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    mobile = request.form['mobile']
    cursor = Connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email=%s', [email])

    result = cursor.fetchall()
    if len(result) != 0:
        flash(u"The user already exists", 'error')
        return redirect('/sign-up.html')

    cursor = Connection.cursor()
    cursor.execute('SELECT * FROM users')
    result = cursor.fetchall()
    number = len(result)
    cursor = Connection.cursor()
    cursor.execute('INSERT INTO users VALUE(%s, 2, %s, %s, %s, %s)', [number, password, name, email, mobile])
    cursor = Connection.cursor()
    cursor.execute('INSERT INTO customer VALUE(%s, 0, 0)', [number])
    Connection.commit()
    session['user_id'] = number
    print('Success')
    return redirect('/index.html')

if __name__ == '__main__':
    app.run()
