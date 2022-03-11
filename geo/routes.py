from flask import Blueprint
from flask import current_app as app


# Blueprint Configuration
auth_bp = Blueprint(
    'map_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route('/', methods = ['POST', 'GET'])