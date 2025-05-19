# run.py

from app import create_app
from app.states import inicializar_db

inicializar_db()
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
