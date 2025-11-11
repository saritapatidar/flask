from flask import Flask
from .database import db
from .routes.employee_routes import employee_bp
from flask_migrate import Migrate
def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False

    db.init_app(app)
    migrate = Migrate(app, db) 
    app.register_blueprint(employee_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app
