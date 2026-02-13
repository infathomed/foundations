import os
from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL", "")

# Create the DB engine once at startup (simple v1 approach)
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-check")
def db_check():
    if engine is None:
        return {"ok": False, "error": "DATABASE_URL not set"}

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1;")).scalar_one()
        return {"ok": True, "result": result}
    except Exception as e:
        return {"ok": False, "error": str(e)}
