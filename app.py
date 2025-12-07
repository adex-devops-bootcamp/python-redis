from flask import Flask
import psycopg2
import redis
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = Flask(__name__)

# Redis client
r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT"))
)

# PostgreSQL credentials
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT"))
}

@app.route("/")
def check_services():
    redis_status = "UP"
    db_status = "UP"

    # Check Redis
    try:
        r.ping()
    except:
        redis_status = "DOWN"

    # Check PostgreSQL
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        cursor.close()
        conn.close()
    except:
        db_status = "DOWN"

    return f"Redis: {redis_status} | PostgreSQL: {db_status}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
