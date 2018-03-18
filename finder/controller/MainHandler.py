from flask import request
from .BaseHandler import BaseView
from finder.models.TimetableFinder import TimetableFinder


class IndexView(BaseView):
    def get(self, *args, **kwargs):
        finder = TimetableFinder()
        return BaseView.render('index.html', taken_time=finder.find_taken_time())
