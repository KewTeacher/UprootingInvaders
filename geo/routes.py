from flask import Blueprint
from flask import current_app as app


# Blueprint Configuration
geo_bp = Blueprint(
    'geo_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@geo_bp.route('/', methods = ['POST', 'GET'])