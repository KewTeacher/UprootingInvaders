from flask import Blueprint
from flask import current_app as app


# Blueprint Configuration
geo = Blueprint(
    'geo', __name__,
    template_folder='templates',
    static_folder='static'
)


@geo.route('/', methods = ['POST', 'GET'])
