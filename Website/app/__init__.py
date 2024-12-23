from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load the configuration from instance/config.py
    app.config.from_object('instance.config.Config')

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
