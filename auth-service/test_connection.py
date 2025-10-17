import os
import time
import psycopg2
import redis

# Toma variables del entorno (usa defaults si no existen)
PG_USER = os.getenv("POSTGRES_USER", "devuser")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "devpass")
PG_DB = os.getenv("POSTGRES_DB", "main_db")
PG_HOST = os.getenv("POSTGRES_HOST", "postgres")
PG_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

def wait_for(service_name, fn, retries=10, delay=2):
    for attempt in range(1, retries+1):
        try:
            return fn()
        except Exception as e:
            print(f"[{service_name}] intento {attempt}/{retries} falló: {e}")
            time.sleep(delay)
    raise RuntimeError(f"{service_name} no disponible después de {retries} intentos.")

def test_postgres():
    def connect():
        conn = psycopg2.connect(
            dbname=PG_DB, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT
        )
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
        conn.close()
        return version

    version = wait_for("PostgreSQL", connect)
    print(f"✅ PostgreSQL OK → {version}")

def test_redis():
    def ping():
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        return r.ping()
    ok = wait_for("Redis", ping)
    print(f"✅ Redis OK → ping={ok}")

if __name__ == "__main__":
    print("Iniciando pruebas de conexión...")
    test_postgres()
    test_redis()
    print("🎉 Todo listo: conexiones OK.")
