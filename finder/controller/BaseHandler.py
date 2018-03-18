from flask.views import MethodView
from flask import render_template, redirect


class BaseView(MethodView):
    def get(self, *args, **kwargs):
        return self.redirect("/")

    def post(self, *args, **kwargs):
        return self.redirect("/")

    @staticmethod
    def render(tpl, **render_data):
        return render_template(tpl, **render_data)

    @staticmethod
    def redirect(target):
        return redirect(target)
