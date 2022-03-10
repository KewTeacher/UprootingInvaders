from flask import Flask

def creat_app():
    #Create Flask Application
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_conext():
        #Import parts of our application
        from .auth import routes
        from .data import routes
        from .identifying import routes

        #Register Blueprints
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(data.data_bp)
        app.register_blueprint(identifying.identifying_bp)


        return app