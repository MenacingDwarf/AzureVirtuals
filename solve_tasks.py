import psycopg2
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

name = 'd3c650q3aoqcg6'
user = 'qghnnmdmuizgsr'
password = '9ac4fe7b2c294dc8a8a5d8ed42aca61e1ed790d1b5a3e62a2c869d5f8f0a3380'
host = 'ec2-174-129-254-220.compute-1.amazonaws.com'
port = '5432'

conn = psycopg2.connect(host=host, dbname=name, user=user, password=password)
cur = conn.cursor()
cur.execute("SELECT id, operation_type, amount FROM main_task WHERE status='Solving' OR status='Waiting'")
tasks = cur.fetchall()

data = pd.read_csv('dataset.csv')

lab_encoder = LabelEncoder().fit(data["type"])
data["type"] = lab_encoder.transform(data["type"])

X, y = data[["type", "amount"]], data["isFraud"]
algorithm = RandomForestClassifier(n_estimators=100, max_depth=3)
algorithm.fit(X, y)

for task in tasks:
    prediction = algorithm.predict([[lab_encoder.transform([task[1]])[0], task[2]]])[0]
    result = "Fraud" if prediction == 1 else "Not fraud"
    cur.execute("UPDATE main_task SET status='Solved', solution=%s WHERE id=%s", (result, task[0],))
    conn.commit()

conn.close()
