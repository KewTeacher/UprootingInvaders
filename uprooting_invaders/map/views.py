from flask import Blueprint



# Blueprint Configuration
map = Blueprint(
    'map', __name__,
    template_folder='templates',
    static_folder='static'
)


@geo.route('/', methods = ['POST', 'GET'])
