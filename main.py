
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
# import psycopg2
import json

app = FastAPI()

class Payload(BaseModel):
    data: Dict[str, Any]

def get_db_connection():
        import sqlite3
        return sqlite3.connect('database.db')

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS payloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.on_event("startup")
async def startup():
    init_db()

@app.post("/payload")
async def receive_payload(payload: Payload):
    conn = get_db_connection()
    cur = conn.cursor()
    print(payload.data)
    cur.execute(
        "INSERT INTO payloads (data) VALUES (?)",
        (json.dumps(payload.data),)
    )
    
    conn.commit()
    print("Received payload:", payload.data)

     # Print all rows in the payloads table
    cur.execute("SELECT * FROM payloads")
    rows = cur.fetchall()
    print("\nCurrent database contents:")
    print("ID | Data | Created At")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]}")
    print("-" * 50)
    
    cur.close()
    conn.close()
    
    return {"status": "success", "message": "Payload saved to database"}


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}


@app.get("/payloads")
async def get_payloads():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, data, created_at FROM payloads")
    rows = cur.fetchall()
    
    # Convert rows to list of dictionaries
    payloads = []
    for row in rows:
        payloads.append({
            "id": row[0],
            "data": json.loads(row[1]),
            "created_at": row[2]
        })
    
    cur.close()
    conn.close()
    
    return {"payloads": payloads}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
