import os

import psycopg
import redis
from flask import Flask, jsonify, request

app = Flask(__name__)


def check_postgres():
    try:
        with psycopg.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ.get("POSTGRES_PORT", "5432"),
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            connect_timeout=2,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return "ok"
    except Exception:
        return "error"


def check_redis():
    try:
        client = redis.Redis(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ.get("REDIS_PORT", "6379")),
            password=os.environ["REDIS_PASSWORD"],
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        return "ok" if client.ping() else "error"
    except Exception:
        return "error"


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.get("/")
def index():
    return jsonify(
        service="backend",
        postgres=check_postgres(),
        redis=check_redis(),
        forwarded={
            "host": request.headers.get("Host"),
            "x-forwarded-for": request.headers.get("X-Forwarded-For"),
            "x-forwarded-proto": request.headers.get("X-Forwarded-Proto"),
            "x-forwarded-host": request.headers.get("X-Forwarded-Host"),
        },
    )
