import time
import random
import requests
from flask import Flask, json, request
import sqlite3
import pika
from shop.settings import TABLE_NAME, DB_NAME

app = Flask(__name__)
connection = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = connection.cursor()


@app.route('/')
def index():
    statement = f"SELECT * FROM {TABLE_NAME}"
    cursor.execute(statement)
    result = cursor.fetchall()
    print(result)
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/sale/', methods=['POST'])
def sale():
    data = request.form
    phone = data['phone']
    price = data['price']
    is_sale = True
    status = 'DONE'
    statement = f"INSERT INTO {TABLE_NAME}(phone,price,is_sale,status) values (?,?,?,?)"
    cursor.execute(statement, (phone, price, is_sale, status))
    response = app.response_class(
        response=json.dumps({'STATUS': 'OK'}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/repair/', methods=['POST'])
def repair():
    data = request.form
    phone = data['phone']
    price = data['price']
    is_sale = False
    status = 'IN PROCESS'
    statement = f"INSERT INTO {TABLE_NAME}(phone,price,is_sale,status) values (?,?,?,?)"
    cursor.execute(statement, (phone, price, is_sale, status))
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='repair')
    channel.basic_publish(exchange='', routing_key='repair', body=phone)
    connection.close()
    response = app.response_class(
        response=json.dumps({'STATUS': 'OK'}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/change/', methods=['POST'])
def change_status():
    data = request.form
    phone = data['phone']
    status = data['status']
    print(status)
    statement = f"UPDATE {TABLE_NAME} set status = ? where phone = ?"
    cursor.execute(statement, (status, phone))

    response = app.response_class(
        response=json.dumps({'STATUS': 'OK'}),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=True)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='repair')


def callback(ch, method, properties, body):
    phone = body
    repair_time = random.randint(3, 40)
    time.sleep(repair_time)
    requests.post('http://127.0.0.1:5000/change/', data={'phone': phone, 'status': 'DONE'})


channel.basic_consume(queue='repair', on_message_callback=callback)

print('start')
channel.start_consuming()

