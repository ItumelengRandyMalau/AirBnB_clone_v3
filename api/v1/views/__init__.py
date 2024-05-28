1  # !/usr/bin/python3
2 """
  3 creates a blueprint of a Flask app
  4 """
5 from Flask import Blueprint
6
7 app_views = Blueprint('appViews, __name__', url_prefix='/api/v1')
8
9 from api.v1.views.index import *
