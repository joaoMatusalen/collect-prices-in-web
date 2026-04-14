from flask import Flask
from flask_cors import CORS

from api.routes.analytics import analytics_bp
from api.routes.products import products_bp
from api.routes.stores import stores_bp
from api.routes.urls import urls_bp


def create_app():
    app = Flask(__name__)
    CORS(app, origins="http://localhost:5173")
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB max request body

    app.register_blueprint(products_bp)
    app.register_blueprint(urls_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(stores_bp)

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
