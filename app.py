from flask import Flask, jsonify
import psycopg2
import redis
import json
import os

app = Flask(__name__)

# Redis connection
cache = redis.Redis(host="redis", port=6379)

# PostgreSQL connection
def get_db():
    return psycopg2.connect(
        host="postgres",
        database="studentsdb",
        user="admin",
        password="password"
    )

@app.route("/students")
def get_students():
    # Check Redis cache first
    cached = cache.get("students")
    if cached:
        return jsonify({"source": "cache 🚀", "data": json.loads(cached)})

    # Not in cache, fetch from PostgreSQL
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, grade FROM students;")
    rows = cur.fetchall()
    conn.close()

    # Store in Redis for next time
    students = [{"id": r[0], "name": r[1], "grade": r[2]} for r in rows]
    cache.set("students", json.dumps(students), ex=30)

    return jsonify({"source": "database 🗄️", "data": students})

@app.route("/add/<name>/<grade>")
def add_student(name, grade):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, grade) VALUES (%s, %s);", (name, grade))
    conn.commit()
    conn.close()

    # Clear cache so fresh data is fetched next time
    cache.delete("students")
    return f"Student {name} with grade {grade} added! 🎓"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
