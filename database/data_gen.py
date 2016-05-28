from flask import Flask, render_template, session, request, redirect, flash, g

import mysql.connector
import datetime
import random

def add_flights():
    Connection = mysql.connector.connect(host='localhost', port=3306, user='database16', password='database16',
                                         database='FeiFlight')
    ID  = 1
    flight_id = 'HA223'
    date_begin = '2016-06-01'
    date_end = '2017-05-31'
    From = 'Shanghai'
    to = 'Guangzhou'
    cabin_class = 'Economy'
    depart_time = '08:50'
    arrival_time = '11:20'
    price = 700
    point = 700
    cancel_fee = 100
    change_fee = 50
    seats = 200
    date_b = datetime.datetime.strptime(date_begin, '%Y-%m-%d').date()
    date_e = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()
    d_time = datetime.datetime.strptime(depart_time, '%H:%M').time()
    a_time = datetime.datetime.strptime(arrival_time, '%H:%M').time()
    Date = date_b
    while Date <= date_e:
        print Date
        cursor = Connection.cursor()
        cursor.execute('INSERT INTO flight VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [flight_id, Date, cabin_class, From, to, d_time, a_time, price + random.randint(0, 400) - 200, point + random.randint(0, 400) - 200, cancel_fee + random.randint(0, 30) - 15, change_fee + random.randint(0, 20) - 10, seats, 0, ID])
        Connection.commit()
        Date = Date + datetime.timedelta(days=1)
    print('Success')
    
    cabin_class = 'Business'
    price = 1500
    point = 1500
    cancel_fee = 100
    change_fee = 50
    seats = 20
    date_b = datetime.datetime.strptime(date_begin, '%Y-%m-%d').date()
    date_e = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()
    d_time = datetime.datetime.strptime(depart_time, '%H:%M').time()
    a_time = datetime.datetime.strptime(arrival_time, '%H:%M').time()
    Date = date_b
    while Date <= date_e:
        print Date
        cursor = Connection.cursor()
        cursor.execute('INSERT INTO flight VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [flight_id, Date, cabin_class, From, to, d_time, a_time, price + random.randint(0, 400) - 200, point + random.randint(0, 400) - 200, cancel_fee + random.randint(0, 30) - 15, change_fee + random.randint(0, 20) - 10, seats, 0, ID])
        Connection.commit()
        Date = Date + datetime.timedelta(days=1)
    print('Success')
    
    cabin_class = 'First Class'
    price = 3000
    point = 3000
    cancel_fee = 100
    change_fee = 50
    seats = 8
    date_b = datetime.datetime.strptime(date_begin, '%Y-%m-%d').date()
    date_e = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()
    d_time = datetime.datetime.strptime(depart_time, '%H:%M').time()
    a_time = datetime.datetime.strptime(arrival_time, '%H:%M').time()
    Date = date_b
    while Date <= date_e:
        print Date
        cursor = Connection.cursor()
        cursor.execute('INSERT INTO flight VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [flight_id, Date, cabin_class, From, to, d_time, a_time, price + random.randint(0, 400) - 200, point + random.randint(0, 400) - 200, cancel_fee + random.randint(0, 30) - 15, change_fee + random.randint(0, 20) - 10, seats, 0, ID])
        Connection.commit()
        Date = Date + datetime.timedelta(days=1)
    print('Success')

if __name__ == '__main__':
    add_flights()
