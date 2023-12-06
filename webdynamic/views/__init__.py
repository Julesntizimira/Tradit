from flask import Blueprint

app_pages = Blueprint('app_pages', __name__, url_prefix='')

from webdynamic.views.login import *
from webdynamic.views.room import *
from webdynamic.views.dashboard import *
from webdynamic.views.book import *