from flask import Flask
from extensions import db
import os
import sqlalchemy as sa


def _run_migrations(db):
    """Apply any missing schema changes to an existing database."""
    inspector = sa.inspect(db.engine)
    if not inspector.has_table('taller'):
        return
    taller_columns = [col['name'] for col in inspector.get_columns('taller')]
    if 'forma_pago' not in taller_columns:
        with db.engine.begin() as conn:
            conn.execute(sa.text(
                "ALTER TABLE taller ADD COLUMN forma_pago VARCHAR(50) DEFAULT 'efectivo'"
            ))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes.clientes import clientes_bp
    from routes.productos import productos_bp
    from routes.stock import stock_bp
    from routes.taller import taller_bp
    from routes.caja import caja_bp
    from routes.contabilidad import contabilidad_bp
    from routes.ventas import ventas_bp
    from routes.dashboard import dashboard_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    app.register_blueprint(productos_bp, url_prefix='/productos')
    app.register_blueprint(stock_bp, url_prefix='/stock')
    app.register_blueprint(taller_bp, url_prefix='/taller')
    app.register_blueprint(caja_bp, url_prefix='/caja')
    app.register_blueprint(contabilidad_bp, url_prefix='/contabilidad')
    app.register_blueprint(ventas_bp, url_prefix='/ventas')

    with app.app_context():
        db.create_all()
        _run_migrations(db)

    return app

app = create_app()

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=5000)
