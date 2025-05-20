# app/states.py

import sqlite3
import os

DB_PATH = "data/usuarios.db"

def inicializar_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            numero TEXT PRIMARY KEY,
            estado TEXT NOT NULL,
            ultima_rota TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_state(numero):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT estado FROM usuarios WHERE numero = ?", (numero,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "menu"

def set_state(numero, estado):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (numero, estado)
        VALUES (?, ?)
        ON CONFLICT(numero) DO UPDATE SET estado=excluded.estado
    """, (numero, estado))
    conn.commit()
    conn.close()

def set_rota(numero, rota):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios SET ultima_rota = ?
        WHERE numero = ?
    """, (rota, numero))
    conn.commit()
    conn.close()
