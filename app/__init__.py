from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salary_agent.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from app.routes import main_bp
        app.register_blueprint(main_bp)
        db.create_all()

    return app