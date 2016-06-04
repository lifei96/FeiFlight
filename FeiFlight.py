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

search_result = []
passenger_num = 0
@app.route('/index-round-trip', methods=["GET"])
def index_round_trip():
    From = request.args.get('From')
    to = request.args.get('to')
    d_date = datetime.datetime.strptime(request.args.get('d_date'), '%d/%b/%Y').date()
    r_date = datetime.datetime.strptime(request.args.get('r_date'), '%d/%b/%Y').date()
    volume = request.args.get('volume')
    cabin_class = request.args.get('cabin_class')
    cursor = Connection.cursor()
    cursor.execute('SELECT u1.name, f1.id, f1.date, f1.from, f1.depart, f1.to, f1.arrival, f1.price, f1.point, f1.cancel_rule, f1.change_rule, f1.volume, f1.class, \
                    u2.name, f2.id, f2.date, f2.from, f2.depart, f2.to, f2.arrival, f2.price, f2.point, f2.cancel_rule, f2.change_rule, f2.volume, f2.class \
                    FROM flight as f1, users as u1, flight as f2, users as u2\
                    WHERE f1.company_id=u1.id and f2.company_id=u2.id and f1.from=%s and f1.to=%s\
                    and f1.date=%s and f1.volume>=%s and f1.class=%s and f2.from=%s and f2.to=%s\
                    and f2.date=%s and f2.volume>=%s and f2.class=%s and f1.canceled=0 and f2.canceled=0\
                    ORDER BY f1.price+f2.price', [From, to, d_date, volume, cabin_class, to, From, r_date, volume, cabin_class])
    result = cursor.fetchall()
    global search_result
    search_result = list(result)
    global passenger_num
    passenger_num = int(volume)
    res = ['', '']
    res[0] = '<table class="table"><thead><tr><th>Airline</th><th>Flight</th><th>Date</th><th>Depart</th><th>Time</th>\
              <th>Arrival</th><th>Time</th><th>Price</th></tr></thead><tbody>'
    res[1] = ''
    for j in range(len(result)):
        item = result[j]
        res[0] = res[0] + '<tr>'
        res[1] = res[1] + '<div aria-hidden="true" class="modal fade" id="order' + str(j) + '" role="dialog" tabindex="-1">\
                           <div class="modal-dialog container-full"><div class="modal-content"><div class="modal-heading">\
                           <a class="modal-close" data-dismiss="modal">×</a><h2 class="modal-title">Order now</h2></div>\
                           <form class="form" action="new_order" method="POST"><div class="modal-inner"><div class="card">\
                           <div class="card-main"><div class="card-inner margin-bottom-no">\
                           <p class="card-heading">Flight Info</p><div class="card-table">\
                           <div class="table-responsive"><table class="table" title="flight_info">\
                           <thead><tr><th>Airline</th><th>Flight</th><th>Date</th><th>Depart</th><th>Time</th>\
                           <th>Arrival</th><th>Time</th><th>Points/Cancel/Change/Class</th><th>Price</th></tr></thead><tbody>'
        for i in range(7):
            if i == 0:
                res[0] = res[0] + '<th>' + '<p>' + str(item[i]) + '</p>' + '<p>' + str(item[i+13]) + '</p>' + \
                         '<p><a class="btn btn-brand waves-attach" data-toggle="modal" href="#order' + str(j) + '">Order</a></p>' + '</th>'
            elif i != 4 and i !=6:
                res[0] = res[0] + '<th>' + '<p>' + str(item[i]) + '</p>' + '<p>' + str(item[i+13]) + '</p>' + '</th>'
            else:
                res[0] = res[0] + '<th>' + '<p>' + str(item[i])[0:len(str(item[i]))-3] + '</p>' + '<p>' + str(item[i+13])[0:len(str(item[i+13]))-3] + '</p>' + '</th>'
        res[0] = res[0] + '<th>' + '<p>￥' + str(item[7]) + '</p>' + '<p>￥' + str(item[20]) + '</p>' + '<p>￥' + str(item[7]+item[20]) + '</p>' + '</th>'
        res[0] = res[0] + '</tr>'
        for i in range(7):
            if i != 4 and i != 6:
                res[1] = res[1] + '<th>' + '<p>' + str(item[i]) + '</p>' + '<p>' + str(item[i + 13]) + '</p>' + '</th>'
            else:
                res[1] = res[1] + '<th>' + '<p>' + str(item[i])[0:len(str(item[i])) - 3] + '</p>' + '<p>' + str(item[i + 13])[0:len(str(item[i + 13])) - 3] + '</p>' + '</th>'
        res[1] = res[1] + '<th>' + '<p>' + str(item[8]) + '/￥' + str(item[9]) + '/￥' + str(item[10]) + '/' + str(item[12]) + '</p>' + '<p>' + str(item[21]) + '/￥' + str(item[22]) + '/￥' + str(item[23]) + '/' + str(item[25]) + '</p>' + '</th>'
        res[1] = res[1] + '<th>' + '<p>￥' + str(item[7]) + '</p>' + '<p>￥' + str(item[20]) + '</p>' + '<p>￥' + str(item[7] + item[20]) + '</p>' + '</th>'
        res[1] = res[1] + '</tr>'
        res[1] = res[1] + '</tbody></table></div></div></div><div class="card-action"></div></div></div><div class="card">\
                           <div class="card-main"><div class="card-inner">\
                           <p class="card-heading">Passenger Info</p><input id="item" name="item" type="hidden" value=' + str(j) + '>'
        for i in range(int(volume)):
            res[1] = res[1] + '<p><div class="form-group form-group-label form-group-brand form-limit4">\
                               <label class="floating-label" for="Name' + str(i) + '"> Name </label>\
                               <input class="form-control" id="Name' + str(i) + '" type="text" name="Name' + str(i) + '"></div>\
                               <div class="form-group form-group-label form-group-brand form-limit4">\
                               <label class="floating-label" for="ID' + str(i) + '"> ID </label>\
                               <input class="form-control" id="ID' + str(i) + '" type="text" name="ID' + str(i) + '"></div></p>'
        res[1] = res[1] + '</div></div></div></div>\
                           <div class="modal-footer"><p class="text-right"><button class="btn btn-flat btn-brand\
                           waves-attach" data-dismiss="modal" type="button">Close</button><button class="btn btn-flat \
                           btn-brand waves-attach" type="submit">Order</button></p></div></form></div></div></div>'
    res[0] = res[0] + '</tbody></table>'
    return res[0] + res[1]

@app.route('/index-one-way', methods=["GET"])
def index_one_way():
    From = request.args.get('From')
    to = request.args.get('to')
    d_date = datetime.datetime.strptime(request.args.get('d_date'), '%d/%b/%Y').date()
    volume = request.args.get('volume')
    cabin_class = request.args.get('cabin_class')
    print d_date
    cursor = Connection.cursor()
    cursor.execute('SELECT u.name, f.id, f.date, f.from, f.depart, f.to, f.arrival, f.price, f.point, f.cancel_rule, f.change_rule, f.volume, f.class \
                    FROM flight as f, users as u \
                    WHERE f.company_id=u.id and f.from=%s and f.to=%s and f.date=%s and f.volume>=%s and f.class=%s and f.canceled=0 \
                    ORDER BY f.price', [From, to, d_date, volume, cabin_class])
    result = cursor.fetchall()
    print result
    global search_result
    search_result = list(result)
    global passenger_num
    passenger_num = int(volume)
    res = ['', '']
    res[0] = '<table class="table"><thead><tr><th>Airline</th><th>Flight</th><th>Date</th><th>Depart</th><th>Time</th>\
              <th>Arrival</th><th>Time</th><th>Price</th></tr></thead><tbody>'
    res[1] = ''
    for j in range(len(result)):
        item = result[j]
        res[0] = res[0] + '<tr>'
        res[1] = res[1] + '<div aria-hidden="true" class="modal fade" id="oorder' + str(j) + '" role="dialog" tabindex="-1">\
                           <div class="modal-dialog container-full"><div class="modal-content"><div class="modal-heading">\
                           <a class="modal-close" data-dismiss="modal">×</a><h2 class="modal-title">Order now</h2></div>\
                           <form class="form" action="new_order" method="POST"><div class="modal-inner"><div class="card">\
                           <div class="card-main"><div class="card-inner margin-bottom-no">\
                           <p class="card-heading">Flight Info</p><div class="card-table">\
                           <div class="table-responsive"><table class="table" title="flight_info">\
                           <thead><tr><th>Airline</th><th>Flight</th><th>Date</th><th>Depart</th><th>Time</th>\
                           <th>Arrival</th><th>Time</th><th>Points/Cancel/Change/Class</th><th>Price</th></tr></thead><tbody>'
        for i in range(7):
            if i == 0:
                res[0] = res[0] + '<th>' + '<p>' + str(item[i]) + '</p>' \
                         '<p><a class="btn btn-brand waves-attach" data-toggle="modal" href="#oorder' + str(j) + '">Order</a></p>' + '</th>'
            elif i != 4 and i !=6:
                res[0] = res[0] + '<th>' + '<p>' + str(item[i]) + '</p>' + '</th>'
            else:
                res[0] = res[0] + '<th>' + '<p>' + str(item[i])[0:len(str(item[i]))-3] + '</p>' + '</th>'
        res[0] = res[0] + '<th>' + '<p>￥' + str(item[7]) + '</p>' + '</th>'
        res[0] = res[0] + '</tr>'
        for i in range(7):
            if i != 4 and i != 6:
                res[1] = res[1] + '<th>' + '<p>' + str(item[i]) + '</p>' + '</th>'
            else:
                res[1] = res[1] + '<th>' + '<p>' + str(item[i])[0:len(str(item[i])) - 3] + '</p>' + '</th>'
        res[1] = res[1] + '<th>' + '<p>' + str(item[8]) + '/￥' + str(item[9]) + '/￥' + str(item[10]) + '/' + str(item[12]) + '</p>' + '</th>'
        res[1] = res[1] + '<th>' + '<p>￥' + str(item[7]) + '</p>' + '</th>'
        res[1] = res[1] + '</tr>'
        res[1] = res[1] + '</tbody></table></div></div></div><div class="card-action"></div></div></div><div class="card">\
                           <div class="card-main"><div class="card-inner">\
                           <p class="card-heading">Passenger Info</p><input id="item" name="item" type="hidden" value=' + str(j) + '>'
        for i in range(int(volume)):
            res[1] = res[1] + '<p><div class="form-group form-group-label form-group-brand form-limit4">\
                               <label class="floating-label" for="Name' + str(i) + '"> Name </label>\
                               <input class="form-control" id="Name' + str(i) + '" type="text" name="Name' + str(i) + '"></div>\
                               <div class="form-group form-group-label form-group-brand form-limit4">\
                               <label class="floating-label" for="ID' + str(i) + '"> ID </label>\
                               <input class="form-control" id="ID' + str(i) + '" type="text" name="ID' + str(i) + '"></div></p>'
        res[1] = res[1] + '</div></div></div></div>\
                           <div class="modal-footer"><p class="text-right"><button class="btn btn-flat btn-brand\
                           waves-attach" data-dismiss="modal" type="button">Close</button><button class="btn btn-flat \
                           btn-brand waves-attach" type="submit">Order</button></p></div></form></div></div></div>'
    res[0] = res[0] + '</tbody></table>'
    print res
    return res[0] + res[1]

order_id = 0

@app.route('/order.html')
def order():
    global order_id
    cursor = Connection.cursor()
    cursor.execute('SELECT u.name, f.id, f.class, f.date, f.from, f.depart, f.to, f.arrival, f.point, f.cancel_rule, f.change_rule, f.price \
                    FROM users as u, flight as f, order_flight as o \
                    WHERE u.id=f.company_id and f.id=o.flight_id and f.date=o.flight_date and f.class=o.flight_class and o.order_id=%s\
                    ORDER BY f.date', [order_id])
    f_res = cursor.fetchall()
    f_info = []
    for i in range(len(f_res)):
        flight = []
        for j in range(12):
            if j == 5 or j == 7:
                flight.append(str(f_res[i][j])[0:len(str(f_res[i][j])) - 3])
            else:
                flight.append(str(f_res[i][j]))
        f_info.append(flight)
    cursor = Connection.cursor()
    cursor.execute('SELECT p.name, p.id \
                    FROM passenger as p, order_passenger as o \
                    WHERE p.id=o.passenger_id and o.order_id=%s', [order_id])
    p_info = cursor.fetchall()
    cursor = Connection.cursor()
    cursor.execute('SELECT o.name, o.mobile, o.point, o.price, o.time, o.paid, o.canceled \
                    FROM `order` as o \
                    WHERE o.id=%s', [order_id])
    o_res = cursor.fetchall()
    o_info = []
    for i in range(len(o_res)):
        o = []
        for j in range(7):
            if j == 5 or j == 6:
                if str(o_res[i][j]) == '0':
                    o.append('No')
                elif str(o_res[i][j]) == '1':
                    o.append('Yes')
                else:
                    o.append('Pending')
            else:
                o.append(str(o_res[i][j]))
        o_info.append(o)
    return render_template('order.html', order_id=order_id, f_info=f_info, p_info=p_info, o_info=o_info)

@app.route('/new_order', methods=["POST"])
def new_order():
    passengers = []
    for i in range(passenger_num):
        passengers.append([request.form['Name'+str(i)], request.form['ID'+str(i)]])
    item = search_result[int(request.form['item'])]
    cursor = Connection.cursor()
    cursor.execute('SELECT id FROM `order`')
    result = cursor.fetchall()
    global order_id
    order_id = len(result)
    time = datetime.datetime.now()
    price = 0
    point = 0
    i = 7
    while(i<len(item)):
        price = price + int(item[i]) * passenger_num
        point = point + int(item[i+1]) * passenger_num
        i = i + 13
    cursor = Connection.cursor()
    print order_id
    cursor.execute('INSERT INTO `order` VALUE(%s, %s, %s, %s, %s, %s, %s, 0, 0)', [order_id, session['user_id'], session['name'], session['mobile'], time, price, point])
    Connection.commit()
    i = 1
    while(i<len(item)):
        cursor = Connection.cursor()
        cursor.execute('INSERT INTO order_flight VALUE(%s, %s, %s, %s)', [order_id, item[i], item[i+1], item[i+11]])
        Connection.commit()
        i = i + 13
    for person in passengers:
        try:
            cursor = Connection.cursor()
            cursor.execute('INSERT INTO passenger VALUE(%s, %s)', [person[1], person[0]])
            Connection.commit()
        except:
            print('exist')
        cursor = Connection.cursor()
        print(order_id, person[1])
        cursor.execute('INSERT INTO order_passenger VALUE(%s, %s)', [order_id, person[1]])
        Connection.commit()
    return redirect("/order.html")

@app.route('/pay_now')
def pay_now():
    user_id = session['user_id']
    global order_id
    print user_id
    cursor = Connection.cursor()
    cursor.execute('SELECT balance FROM customer WHERE user_id=%s', [user_id])
    result = cursor.fetchall()
    balance = int(result[0][0])
    print balance
    cursor = Connection.cursor()
    cursor.execute('SELECT price, point FROM `order` WHERE id=%s', [order_id])
    result = cursor.fetchall()
    price = int(result[0][0])
    point = int(result[0][1])
    print price, point
    if balance >= price:
        cursor = Connection.cursor()
        cursor.execute('UPDATE customer SET balance=balance-%s, point=point+%s WHERE user_id=%s', [price, point, user_id])
        Connection.commit()
        cursor = Connection.cursor()
        cursor.execute('UPDATE `order` SET paid=1 WHERE id=%s', [order_id])
        Connection.commit()
    else:
        flash(u'Balance not enough!', 'error')
    return redirect('/order.html')

@app.route('/change_order', methods=["POST"])
def change_order():
    paid = request.form['change_paid']
    flight_id = request.form['flight_id']
    flight_date = request.form['flight_date']
    flight_class = request.form['flight_class']
    flight_d = datetime.datetime.strptime(flight_date, '%Y-%m-%d').date()
    print flight_d
    print flight_class
    if paid == 'No':
        cursor = Connection.cursor()
        cursor.execute('SELECT price, point FROM `order` WHERE id=%s', [order_id])
        result = cursor.fetchall()
        cursor = Connection.cursor()
        cursor.execute('UPDATE customer SET balance=balance+%s, point=point-%s WHERE user_id=%s', [result[0][0], result[0][1], session['user_id']])
        Connection.commit()
        cursor = Connection.cursor()
        cursor.execute('DELETE FROM order_flight WHERE order_id=%s', [order_id])
        Connection.commit()
        cursor = Connection.cursor()
        cursor.execute('INSERT INTO order_flight VALUE(%s, %s, %s, %s)', [order_id, flight_id, flight_d, flight_class])
        Connection.commit()
        cursor = Connection.cursor()
        cursor.execute('SELECT price, point FROM flight WHERE id=%s and date=%s and class=%s', [flight_id, flight_d, flight_class])
        result = cursor.fetchall()
        price = result[0][0]
        point = result[0][1]
        cursor = Connection.cursor()
        cursor.execute('SELECT passenger_id FROM order_passenger WHERE order_id=%s', [order_id])
        result = cursor.fetchall()
        volume = len(result)
        cursor = Connection.cursor()
        cursor.execute('UPDATE `order` SET price=%s, point=%s WHERE id=%s', [price*volume, point*volume, order_id])
        Connection.commit()
    else:
        cursor = Connection.cursor()
        cursor.execute('SELECT id FROM order_change_application')
        result = cursor.fetchall()
        cursor = Connection.cursor()
        cursor.execute('INSERT INTO order_change_application VALUE(%s, %s, %s, %s, %s, "Pending")', [len(result), order_id, flight_id, flight_d, flight_class])
        Connection.commit()
        flash(u'Please wait for the permission from flight company', 'success')
    return redirect('/order.html')

@app.route('/cancel_order', methods=["POST"])
def cancel_order():
    paid = request.form['cancel_paid']
    if paid == 'No':
        cursor = Connection.cursor()
        cursor.execute('UPDATE `order` SET canceled=1 WHERE id=%s', [order_id])
        Connection.commit()
    else:
        cursor = Connection.cursor()
        cursor.execute('SELECT id FROM order_cancel_application')
        result = cursor.fetchall()
        cursor = Connection.cursor()
        cursor.execute('INSERT INTO order_cancel_application VALUE(%s, %s, "Pending")', [len(result), order_id])
        Connection.commit()
        flash(u'Please wait for the permission from flight company', 'success')
    return redirect('/order.html')

@app.route('/my-trips.html')
def my_trips():
    cursor = Connection.cursor()
    cursor.execute('SELECT balance, point FROM customer WHERE user_id=%s', [session['user_id']])
    result = cursor.fetchall()
    balance = result[0][0]
    points = result[0][1]
    cursor = Connection.cursor()
    cursor.execute('SELECT o.time, f.from, f.to, o.paid, o.canceled, o.price, o.id FROM `order` as o, order_flight as of, flight as f \
                    WHERE o.customer_id=%s and o.id=of.order_id and of.flight_id=f.id and of.flight_date=f.date and of.flight_class=f.class\
                    ORDER by o.id', [session['user_id']])
    result = cursor.fetchall()
    orders = []
    for i in range(len(result)):
        if i:
            if result[i][6]!=result[i-1][6]:
                o = []
                for j in range(7):
                    if j == 3 or j == 4:
                        print result[i][j]
                        if result[i][j] == 1:
                            o.append('Yes')
                        else:
                            o.append('No')
                    else:
                        o.append(result[i][j])
                orders.append(o)
        else:
            o = []
            for j in range(7):
                if j == 3 or j == 4:
                    if result[i][j] == 1:
                        o.append('Yes')
                    else:
                        o.append('No')
                else:
                    o.append(result[i][j])
            orders.append(o)
    print orders
    return render_template('my-trips.html', balance=balance, points=points, orders=orders)

@app.route('/add_money', methods=["POST"])
def add_money():
    add_amount = request.form['add_amount']
    cursor = Connection.cursor()
    cursor.execute('UPDATE customer SET balance=balance+%s WHERE user_id=%s', [add_amount, session['user_id']])
    Connection.commit()
    return redirect('my-trips.html')

@app.route('/withdraw', methods=["POST"])
def withdraw():
    withdraw_amount = request.form['withdraw_amount']
    cursor = Connection.cursor()
    cursor.execute('UPDATE customer SET balance=balance-%s WHERE user_id=%s', [withdraw_amount, session['user_id']])
    Connection.commit()
    return redirect('my-trips.html')

@app.route('/get_order', methods=["POST"])
def get_order():
    global order_id
    order_id = request.form['order_id']
    return redirect("/order.html")

@app.route('/admin-portal-order-id', methods=["POST"])
def admin_portal_order_id():
    global order_id
    order_id = request.form['order_id']
    return redirect("/order.html")

@app.route('/admin-portal-user-id', methods=["POST"])
def admin_portal_user_id():
    user_id = request.form['user_id']
    cursor = Connection.cursor()
    cursor.execute('SELECT name FROM users WHERE id=%s', [user_id])
    result = cursor.fetchall()
    user_name = result[0][0]
    cursor = Connection.cursor()
    cursor.execute('SELECT o.time, f.from, f.to, o.paid, o.canceled, o.price, o.id FROM `order` as o, order_flight as of, flight as f \
                    WHERE o.customer_id=%s and o.id=of.order_id and of.flight_id=f.id and of.flight_date=f.date and of.flight_class=f.class\
                    ORDER by o.id', [user_id])
    result = cursor.fetchall()
    orders = []
    for i in range(len(result)):
        if i:
            if result[i][6]!=result[i-1][6]:
                o = []
                for j in range(7):
                    if j == 3 or j == 4:
                        print result[i][j]
                        if result[i][j] == 1:
                            o.append('Yes')
                        else:
                            o.append('No')
                    else:
                        o.append(result[i][j])
                orders.append(o)
        else:
            o = []
            for j in range(7):
                if j == 3 or j == 4:
                    if result[i][j] == 1:
                        o.append('Yes')
                    else:
                        o.append('No')
                else:
                    o.append(result[i][j])
            orders.append(o)
    print orders
    return render_template('user-orders.html', orders=orders, user_name=user_name)

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/login.html', methods=["POST"])
def login_post():
    email = request.form['email']
    password = request.form['password']
    cursor = Connection.cursor()
    cursor.execute('SELECT id, user_type, password, name, mobile FROM users WHERE email=%s', [email])
    result = cursor.fetchall()
    if len(result) == 0:
        flash(u"The user does not exist!", 'error')
        return redirect('/login.html')
    if password != result[0][2]:
        flash(u"Wrong password!", 'error')
        return redirect('/login.html')
    session['user_id'] = result[0][0]
    session['user_type'] = result[0][1]
    session['name'] = result[0][3]
    session['mobile'] = result[0][4]
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
    Connection.commit()
    flash(u"Profile updated", 'success')
    return redirect('/profile.html')

@app.route('/admin-portal.html')
def admin_portal():
    cursor = Connection.cursor()
    cursor.execute('SELECT * FROM flight_cancel_application')
    cancel_info = cursor.fetchall()
    return render_template('admin-portal.html', cancel_info=cancel_info)

@app.route('/f_cancel_accept', methods=["POST"])
def f_cancel_accept():
    cancel_id = request.form['cancel_id']
    flight_id = request.form['flight_id']
    flight_date = request.form['flight_date']
    flight_class = request.form['flight_class']
    cursor = Connection.cursor()
    cursor.execute('UPDATE flight SET canceled=1 WHERE id=%s and date=%s and class=%s', [flight_id, flight_date, flight_class])
    Connection.commit()
    cursor = Connection.cursor()
    cursor.execute('UPDATE flight_cancel_application SET process="Accepted" WHERE id=%s', [cancel_id])
    Connection.commit()
    return redirect('/admin-portal.html')

@app.route('/f_cancel_reject', methods=["POST"])
def f_cancel_reject():
    cancel_id = request.form['cancel_id']
    cursor = Connection.cursor()
    cursor.execute('UPDATE flight_cancel_application SET process="Rejected" WHERE id=%s', [cancel_id])
    Connection.commit()
    return redirect('/admin-portal.html')

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
    flash(u"Company added", 'success')
    return redirect('/admin-portal.html')

@app.route('/company-portal.html')
def company_portal():
    cursor = Connection.cursor()
    cursor.execute('SELECT * FROM order_cancel_application')
    cancel_info = cursor.fetchall()
    cursor = Connection.cursor()
    cursor.execute('SELECT * FROM order_change_application')
    change_info = cursor.fetchall()
    print change_info
    return render_template('company-portal.html', cancel_info=cancel_info, change_info=change_info)

@app.route('/cancel_accept', methods=["POST"])
def cancel_accept():
    cancel_id = request.form['cancel_id']
    o_id = request.form['o_id']
    cursor = Connection.cursor()
    cursor.execute('UPDATE `order` SET canceled=1 WHERE id=%s', [o_id])
    Connection.commit()
    cursor = Connection.cursor()
    cursor.execute('UPDATE order_cancel_application SET process="Accepted" WHERE id=%s', [cancel_id])
    Connection.commit()
    cursor = Connection.cursor()
    cursor.execute('SELECT price, point, customer_id FROM `order` WHERE id=%s', [o_id])
    result = cursor.fetchall()
    Connection.commit()
    cursor = Connection.cursor()
    cursor.execute('UPDATE customer SET balance=balance+%s, point=point-%s WHERE user_id=%s',
                   [result[0][0], result[0][1], result[0][2]])
    Connection.commit()
    return redirect('/company-portal.html')

@app.route('/cancel_reject', methods=["POST"])
def cancel_reject():
    cancel_id = request.form['cancel_id']
    cursor = Connection.cursor()
    cursor.execute('UPDATE order_cancel_application SET process="Rejected" WHERE id=%s', [cancel_id])
    Connection.commit()
    return redirect('/company-portal.html')

@app.route('/change_accept', methods=["POST"])
def change_accept():
    change_id = request.form['change_id']
    o_id = request.form['o_id']
    flight_id = request.form['flight_id']
    flight_date = request.form['flight_date']
    flight_class = request.form['flight_class']
    cursor = Connection.cursor()
    cursor.execute('UPDATE order_change_application SET process="Accepted" WHERE id=%s', [change_id])
    Connection.commit()
    cursor = Connection.cursor()
    cursor.execute('SELECT price, point, customer_id FROM `order` WHERE id=%s', [o_id])
    result = cursor.fetchall()
    cursor = Connection.cursor()
    cursor.execute('UPDATE customer SET balance=balance+%s, point=point-%s WHERE user_id=%s',
                   [result[0][0], result[0][1], result[0][2]])
    Connection.commit()
    cursor = Connection.cursor()
    cursor.execute('DELETE FROM order_flight WHERE order_id=%s', [o_id])
    Connection.commit()
    cursor = Connection.cursor()
    cursor.execute('INSERT INTO order_flight VALUE(%s, %s, %s, %s)', [o_id, flight_id, flight_date, flight_class])
    Connection.commit()
    cursor = Connection.cursor()
    cursor.execute('SELECT price, point FROM flight WHERE id=%s and date=%s and class=%s',
                   [flight_id, flight_date, flight_class])
    result = cursor.fetchall()
    price = result[0][0]
    point = result[0][1]
    cursor = Connection.cursor()
    cursor.execute('SELECT passenger_id FROM order_passenger WHERE order_id=%s', [o_id])
    result = cursor.fetchall()
    volume = len(result)
    cursor = Connection.cursor()
    cursor.execute('UPDATE `order` SET price=%s, point=%s WHERE id=%s', [price * volume, point * volume, o_id])
    Connection.commit()
    return redirect('/company-portal.html')

@app.route('/change_reject', methods=["POST"])
def change_reject():
    change_id = request.form['change_id']
    cursor = Connection.cursor()
    cursor.execute('UPDATE order_change_application SET process="Rejected" WHERE id=%s', [change_id])
    Connection.commit()
    return redirect('/company-portal.html')

@app.route('/add_flights', methods=["POST"])
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
        cursor = Connection.cursor()
        cursor.execute('INSERT INTO flight VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [flight_id, Date, cabin_class, From, to, d_time, a_time, price, point, cancel_fee, change_fee, seats, 0, session['user_id']])
        Connection.commit()
        Date = Date + datetime.timedelta(days=1)
    flash(u"Flights added", 'success')
    return redirect('/company-portal.html')

@app.route('/flight.html', methods=["POST"])
def search_flights():
    flight_id = request.form['flight_no']
    flight_date = request.form['flight_date']
    flight_class = request.form['flight_class']
    cursor = Connection.cursor()
    cursor.execute('SELECT * FROM flight WHERE id=%s and date=%s and class=%s', [flight_id, flight_date, flight_class])
    result = cursor.fetchall()
    f_info = []
    for i in range(len(result[0])):
        if i == 12:
            if result[0][i] == 1:
                f_info.append('Yes')
            else:
                f_info.append('No')
        else:
            f_info.append(result[0][i])
    cursor = Connection.cursor()
    cursor.execute('SELECT p.name, p.id FROM passenger as p, order_passenger as op, order_flight as of \
                    WHERE of.flight_id=%s and of.flight_date=%s and of.flight_class=%s and of.order_id=op.order_id and \
                    op.passenger_id=p.id', [flight_id, flight_date, flight_class])
    p_info = cursor.fetchall()
    return render_template('/flight.html', f_info=f_info, p_info=p_info)

@app.route('/modify_flight', methods=["POST"])
def modify_flight():
    flight_id = request.form['Flight_id']
    flight_date = request.form['Flight_date']
    flight_class = request.form['Flight_class']
    volume = request.form['seats']
    price = request.form['price']
    point = request.form['point']
    cancel_fee = request.form['cancel_fee']
    change_fee = request.form['change_fee']
    cursor = Connection.cursor()
    cursor.execute('UPDATE flight SET volume=%s, price=%s, point=%s, cancel_rule=%s, change_rule=%s WHERE id=%s and \
                    date=%s and class=%s', [volume, price, point, cancel_fee, change_fee, flight_id, flight_date, flight_class])
    Connection.commit()
    cursor = Connection.cursor()
    cursor.execute('SELECT * FROM flight WHERE id=%s and date=%s and class=%s', [flight_id, flight_date, flight_class])
    result = cursor.fetchall()
    f_info = []
    for i in range(len(result[0])):
        if i == 12:
            if result[0][i] == 1:
                f_info.append('Yes')
            else:
                f_info.append('No')
        else:
            f_info.append(result[0][i])
    cursor = Connection.cursor()
    cursor.execute('SELECT p.name, p.id FROM passenger as p, order_passenger as op, order_flight as of \
                    WHERE of.flight_id=%s and of.flight_date=%s and of.flight_class=%s and of.order_id=op.order_id and \
                    op.passenger_id=p.id', [flight_id, flight_date, flight_class])
    p_info = cursor.fetchall()
    flash(u'Flight modified', 'success')
    return render_template('/flight.html', f_info=f_info, p_info=p_info)

@app.route('/cancel_flight', methods=["POST"])
def cancel_flight():
    flight_id = request.form['Flight_id']
    flight_date = request.form['Flight_date']
    flight_class = request.form['Flight_class']
    cursor = Connection.cursor()
    cursor.execute('SELECT id FROM flight_cancel_application')
    result = cursor.fetchall()
    fca_id = len(result)
    cursor = Connection.cursor()
    cursor.execute('INSERT INTO flight_cancel_application VALUE(%s, %s, %s, %s, "Pending")', [fca_id, flight_id, flight_date, flight_class])
    Connection.commit()
    cursor = Connection.cursor()
    cursor.execute('SELECT * FROM flight WHERE id=%s and date=%s and class=%s', [flight_id, flight_date, flight_class])
    result = cursor.fetchall()
    f_info = []
    for i in range(len(result[0])):
        if i == 12:
            if result[0][i] == 1:
                f_info.append('Yes')
            else:
                f_info.append('No')
        else:
            f_info.append(result[0][i])
    cursor = Connection.cursor()
    cursor.execute('SELECT p.name, p.id FROM passenger as p, order_passenger as op, order_flight as of \
                    WHERE of.flight_id=%s and of.flight_date=%s and of.flight_class=%s and of.order_id=op.order_id and \
                    op.passenger_id=p.id', [flight_id, flight_date, flight_class])
    p_info = cursor.fetchall()
    flash(u'Please wait for the permission from admin', 'success')
    return render_template('/flight.html', f_info=f_info, p_info=p_info)

if __name__ == '__main__':
    app.run()
