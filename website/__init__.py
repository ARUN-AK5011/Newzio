from flask import Flask
import sqlite3


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'devkey123'

    # Create SQLite connection
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            email TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()

    # Attach DB to app instance
    app.conn = conn

    # Register blueprints
    from .views import news
    from .auth import auth
    from .categories import category

    app.register_blueprint(news)
    app.register_blueprint(auth)
    app.register_blueprint(category,url_prefix='/')

    return app