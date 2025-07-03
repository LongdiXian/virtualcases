import os
from flask import Flask,jsonify,render_template
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
def all():
    try:
        conn1 = get_db_connection()
        curse1 = conn1.cursor()
        sql = f"""
                SELECT chapter,content from public.chapter
            """
        curse1.execute(sql)
        allda = curse1.fetchall()
        data = [{'chapter': row[0], 'content': row[1]} for row in allda]
        return jsonify(data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn1:
            release_db_connection(conn1)

@app.route("/case/<content>", methods=["GET"])
def case(content):
    try:
        cont=content
        print(cont)
        conn1 = get_db_connection()
        curse1 = conn1.cursor()
        sql = f"""
                SELECT chapter_content,content from public.abstract where chapter_content='{cont}'
            """
        print(sql)
        curse1.execute(sql)
        allda = curse1.fetchall()
        data = [{'chapter': row[0], 'content': row[1]} for row in allda]
        return jsonify(data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn1:
            release_db_connection(conn1)

@app.route('/index')
def home():
    return render_template('index_test.html')

@app.route('/case')
def case_page():
    return render_template('case_test.html')

@app.route('/content')
def content_page():
    return render_template('content_test.html')


@app.route("/casenumber/<chapter>", methods=["GET"])
def casenumber(chapter):
    try:
        cont=chapter
        print(cont)
        conn1 = get_db_connection()
        curse1 = conn1.cursor()
        sql = f"""
                select DISTINCT case_number from public.content where  chapter_content='{cont}'
            """
        print(sql)
        curse1.execute(sql)
        allda = curse1.fetchall()
        data = [{'number': row[0]} for row in allda]
        return jsonify(data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn1:
            release_db_connection(conn1)

@app.route("/content/<casenumber>", methods=["GET"])
def content(casenumber):
    try:
        cont=casenumber
        print(cont)
        conn1 = get_db_connection()
        curse1 = conn1.cursor()
        sql = f"""
                select name,content from public.content where case_number={cont}
            """
        print(sql)
        curse1.execute(sql)
        allda = curse1.fetchall()
        data = [{'name': row[0],'conent':row[1]} for row in allda]
        return jsonify(data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn1:
            release_db_connection(conn1)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, ssl_context=('cert.pem', 'key.pem'))
    app.config['JSON_AS_ASCII'] = False
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)