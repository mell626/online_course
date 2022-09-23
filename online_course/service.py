from .imports import *
from .models import *


service = Blueprint('app_service', __name__, url_prefix = '/services', template_folder = 'templates')


@service.route('/')
def index():
    user = session.get('user', None)

    extesion_service = ExtensionService.query.all()
    
    return render_template('service.html', user = user, data = extesion_service)