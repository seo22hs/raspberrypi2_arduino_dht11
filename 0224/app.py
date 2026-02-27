import pymysql #mysql.connector

from flask import Flask, render_template, request
#from datetime import datetime

app = Flask(__name__)

# ── MySQL 연결 ──────────────────────────────

def get_connection():

    return pymysql.connect(

        host="localhost",
        user="sensor",
        password="1234",
        database="sensor_db",
        cursorclass=pymysql.cursors.DictCursor

    # return mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="test1234",
    #     database="sensor_db"
    )


# ── 데이터 저장 ─────────────────────────────

def save_to_db(temperature, humidity):

    conn   = get_connection()
    cursor = conn.cursor()

    sql    = "INSERT INTO sensor_data (temperature, humidity) VALUES (%s, %s)"

    cursor.execute(sql, (temperature, humidity))
    conn.commit()
    cursor.close()
    conn.close()

# ── 데이터 조회 ─────────────────────────────

def get_records(limit=10):

    conn   = get_connection()
    cursor = conn.cursor() #(dictionary=True)

    cursor.execute(

        "SELECT * FROM sensor_data ORDER BY recorded_at DESC LIMIT %s",

        (limit,)

    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return rows

# ── 라우트 ──────────────────────────────────

@app.route('/')

def index():

    records = get_records()

    return render_template("index.html", records=records)

@app.route('/collect')

def collect():

    temperature = request.args.get("temperature")
    humidity    = request.args.get("humidity")

    if temperature and humidity:

        save_to_db(float(temperature), float(humidity))
        return f"저장 완료: 온도 {temperature}°C, 습도 {humidity}%"

    else:
        return "데이터 없음", 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

