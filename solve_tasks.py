import psycopg2
import time

name = 'd3c650q3aoqcg6'
user = 'qghnnmdmuizgsr'
password = '9ac4fe7b2c294dc8a8a5d8ed42aca61e1ed790d1b5a3e62a2c869d5f8f0a3380'
host = 'ec2-174-129-254-220.compute-1.amazonaws.com'
port = '5432'

conn = psycopg2.connect(host=host, dbname=name, user=user, password=password)
cur = conn.cursor()
cur.execute("SELECT * FROM main_task WHERE status='Solving'")
tasks = cur.fetchall()
for task in tasks:
    time.sleep(10)
    cur.execute("UPDATE main_task SET status='Solved', solution='Fraud' WHERE id=%s", (task[0],))
    conn.commit()

conn.close()
