from flask import Flask

def create_app():
    #Create Flask Application
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_conext():
        #Import parts of our application
        from .auth import routes
        from .geo import routes
        from .identifying import routes

        #Register Blueprints
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(geo.geo_bp)
        app.register_blueprint(identifying.identifying_bp)


        return app