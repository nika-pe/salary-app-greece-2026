import os
from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__)
    
    # Указываем путь к базе данных в папке instance
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'salary_agent.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # Создаем папку instance, если её нет
        instance_path = os.path.join(basedir, '..', 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
            
        from app.routes import main_bp
        app.register_blueprint(main_bp)
        
        # Создаем таблицы, если их еще нет
        db.create_all()

    return app