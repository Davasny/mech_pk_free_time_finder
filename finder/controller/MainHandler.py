from flask import request
from .BaseHandler import BaseView
from finder.models.TimetableFinder import TimetableFinder
from finder.models.TimetableFinder import TimetableParser
from finder.models.TimetableData import TimetableData
import re


class IndexView(BaseView):
    def get(self, *args, **kwargs):
        return BaseView.render('index.html')


class FilterView(BaseView):
    def get(self, *args, **kwargs):
        if "filter" in request.args:
            if request.args['filter'] is not None:
                filter = request.args['filter']

                selected_keywords = re.findall('"(.*?)"', filter)
                for x in range(len(selected_keywords)):
                    if selected_keywords[x] == "teacher" or selected_keywords[x] == "classroom":
                        filter = filter.replace('"'+selected_keywords[x+1]+'"',
                                                '{"$regex": "/'+ selected_keywords[x+1] +'/"}')

                finder = TimetableFinder(json_query=filter)
                timetable_data = TimetableData()

                taken_time = finder.find_taken_time()

                timetable_parser = TimetableParser(taken_time)
                timetable_by_weeks = timetable_parser.timetable_by_weeks()

                return BaseView.render('week_view.html',
                                        taken_time=finder.find_taken_time(),
                                        hours=timetable_data.get_hours(),
                                        days=timetable_data.get_week_days(),
                                        timetable_by_weeks=timetable_by_weeks
                                        )
        return BaseView.redirect("/")
