import os
from flask import Flask,jsonify
from flask_cors import CORS
from psycopg2.pool import SimpleConnectionPool

app = Flask(__name__)
CORS(app)

pool = SimpleConnectionPool(
            1, 
            20,
            host="database-1.cluster-c76awkwek5e5.ap-southeast-2.rds.amazonaws.com",
            database="postgres",
            user="virtualcases",
            password="digitalteam7792",
            port=5432
        )

def get_db_connection():
    return pool.getconn()

def release_db_connection(conn):
    pool.putconn(conn)

@app.route("/all", methods=["GET"])
def aadata():
    try:
        conn1 = get_db_connection()
        curse1 = conn1.cursor()
        sql = f"""
                SELECT username,password,time from public.usertable
            """
        curse1.execute(sql)
        allda = curse1.fetchall()
        data = [{'userid': row[0], 'password': row[1], 'time': row[2]} for row in allda]
        return jsonify(data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn1:
            release_db_connection(conn1)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    port = int(os.environ.get('PORT', 443))
    app.run(host='0.0.0.0', port=port)