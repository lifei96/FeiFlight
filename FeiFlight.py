# -*- coding:utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash, g, jsonify

import mysql.connector
import datetime
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

get_user = get_model('users', ['id', 'email', 'name', 'mobile', 'password', 'user_type'])

def get_authed_user():
    return get_user(session.get('user_id', None))

@app.before_request
def before_request():
    g.authedUser = get_authed_user()
    g.url_path = request.path

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/index-round-trip', methods=["GET"])
def index_round_trip():
    From = request.args.get('From')
    to = request.args.get('to')
    d_date = datetime.datetime.strptime(request.args.get('d_date'), '%d/%b/%Y').date()
    r_date = datetime.datetime.strptime(request.args.get('r_date'), '%d/%b/%Y').date()
    volume = request.args.get('volume')
    cabin_class = request.args.get('cabin_class')
    cursor = Connection.cursor()
    cursor.execute('SELECT u1.name, f1.id, f1.date, f1.from, f1.depart, f1.to, f1.arrival, f1.price, \
                    u2.name, f2.id, f2.date, f2.from, f2.depart, f2.to, f2.arrival, f2.price\
                    FROM flight as f1, users as u1, flight as f2, users as u2\
                    WHERE f1.company_id=u1.id and f2.company_id=u2.id and f1.from=%s and f1.to=%s\
                    and f1.date=%s and f1.volume>=%s and f1.class=%s and f2.from=%s and f2.to=%s\
                    and f2.date=%s and f2.volume>=%s and f2.class=%s and f1.canceled=0 and f2.canceled=0\
                    ORDER BY f1.price+f2.price', [From, to, d_date, volume, cabin_class, to, From, r_date, volume, cabin_class])
    result = cursor.fetchall()
    res = ['', '']
    res[0] = '<table class="table"><thead><tr><th>Airline</th><th>Flight</th><th>Date</th><th>Depart</th><th>Time</th><th>Arrival</th><th>Time</th><th>Price</th></tr></thead><tbody>'
    res[1] = ''
    for j in range(len(result)):
        item = result[j]
        res[0] = res[0] + '<tr>'
        res[1] = res[1] + '<div aria-hidden="true" class="modal fade" id="buy' + str(j) + '" role="dialog" tabindex="-1"><div class="modal-dialog"><div class="modal-content"><div class="modal-heading"><a class="modal-close" data-dismiss="modal">×</a><h2 class="modal-title">Details</h2></div><form class="form" action="buy" method="POST"><div class="modal-inner">'
        for i in range(7):
            if i == 0:
                res[0] = res[0] + '<th>' + '<p>' + str(item[i]) + '</p>' + '<p>' + str(item[i+8]) + '</p>' + '<p><a class="btn btn-brand waves-attach" data-toggle="modal" href="#buy' + str(j) + '">Details</a></p>' + '</th>'
            elif i != 4 and i !=6:
                res[0] = res[0] + '<th>' + '<p>' + str(item[i]) + '</p>' + '<p>' + str(item[i+8]) + '</p>' + '</th>'
            else:
                res[0] = res[0] + '<th>' + '<p>' + str(item[i])[0:len(str(item[i]))-3] + '</p>' + '<p>' + str(item[i+8])[0:len(str(item[i+8]))-3] + '</p>' + '</th>'
        res[0] = res[0] + '<th>' + '<p>￥' + str(item[7]) + '</p>' + '<p>￥' + str(item[15]) + '</p>' + '<p>￥' + str(item[7]+item[15]) + '</p>' + '</th>'
        res[0] = res[0] + '</tr>'
        res[1] = res[1] + '</div><div class="modal-footer"><p class="text-right"><button class="btn btn-flat btn-brand waves-attach" data-dismiss="modal" type="button">Close</button><button class="btn btn-flat btn-brand waves-attach" type="submit">Buy</button></p></div></form></div></div></div>'
    res[0] = res[0] + '</tbody></table>'
    return res[0] + res[1]

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/login.html', methods=["POST"])
def login_post():
    email = request.form['email']
    password = request.form['password']
    cursor = Connection.cursor()
    cursor.execute('SELECT id, user_type, password, name FROM users WHERE email=%s', [email])

    result = cursor.fetchall()
    print(result)
    if len(result) == 0:
        flash(u"The user does not exist!", 'error')
        return redirect('/login.html')

    if password != result[0][2]:
        flash(u"Wrong password!", 'error')
        return redirect('/login.html')

    session['user_id'] = result[0][0]
    session['user_type'] = result[0][1]
    session['name'] = result[0][3]
    print('Success')
    flash(u"Welcome " + session['name'] + u" !", 'success')
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
    session['user_type'] = 2
    session['name'] = name
    print('Success')
    flash(u"Welcome " + session['name'] + u" !", 'success')
    return redirect('/index.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')

@app.route('/profile.html', methods=["POST"])
def profile_post():
    password = request.form['password']
    name = request.form['name']
    mobile = request.form['mobile']
    cursor = Connection.cursor()
    cursor.execute('UPDATE users SET password=%s, name=%s, mobile=%s WHERE id=%s', [password, name, mobile, session['user_id']])
    print('Success')
    flash(u"Profile updated", 'success')
    return redirect('/profile.html')

@app.route('/admin-portal.html')
def admin_portal():
    return render_template('admin-portal.html')

@app.route('/add-company', methods=["POST"])
def admin_portal_add_company():
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    mobile = request.form['mobile']
    cursor = Connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email=%s', [email])

    result = cursor.fetchall()
    if len(result) != 0:
        flash(u"The company already exists", 'error')
        return redirect('/admin-portal.html')

    cursor = Connection.cursor()
    cursor.execute('SELECT * FROM users')
    result = cursor.fetchall()
    number = len(result)
    cursor = Connection.cursor()
    cursor.execute('INSERT INTO users VALUE(%s, 1, %s, %s, %s, %s)', [number, password, name, email, mobile])
    cursor = Connection.cursor()
    cursor.execute('INSERT INTO company VALUE(%s)', [number])
    Connection.commit()
    print('Success')
    flash(u"Company added", 'success')
    return redirect('/admin-portal.html')

@app.route('/company-portal.html')
def company_portal():
    return render_template('company-portal.html')

@app.route('/add-flights', methods=["POST"])
def company_portal_add_flights():
    flight_id = request.form['flight_id']
    date_begin = request.form['date_begin']
    date_end = request.form['date_end']
    From = request.form['From']
    to = request.form['to']
    cabin_class = request.form['cabin_class']
    depart_time = request.form['depart_time']
    arrival_time = request.form['arrival_time']
    price = request.form['price']
    point = request.form['point']
    cancel_fee = request.form['cancel_fee']
    change_fee = request.form['change_fee']
    seats = request.form['seats']
    date_b = datetime.datetime.strptime(date_begin, '%Y-%m-%d').date()
    date_e = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()
    d_time = datetime.datetime.strptime(depart_time, '%H:%M').time()
    a_time = datetime.datetime.strptime(arrival_time, '%H:%M').time()
    Date = date_b
    while Date <= date_e:
        print Date
        cursor = Connection.cursor()
        cursor.execute('INSERT INTO flight VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [flight_id, Date, cabin_class, From, to, d_time, a_time, price, point, cancel_fee, change_fee, seats, 0, session['user_id']])
        Connection.commit()
        Date = Date + datetime.timedelta(days=1)
    print('Success')
    flash(u"Flight added", 'success')
    print(Exception)
    return redirect('/company-portal.html')

if __name__ == '__main__':
    app.run()
