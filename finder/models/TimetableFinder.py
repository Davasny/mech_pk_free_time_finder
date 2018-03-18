from finder import app, logger
from finder.models.TimetableData import TimetableData
from mongoquery import Query, QueryError
import json
import re


class TimetableFinder:
    def __init__(self, **kwargs):
        self.json_query = "{}"

        if "json_query" in kwargs:
            self.json_query = kwargs['json_query']

        self.timetable = app.timetable

    def load_query(self):
        self.query = json.loads(self.json_query)

    def validate_query(self):
        return True

    def find_taken_time(self):
        if not self.validate_query():
            return False
        else:
            self.load_query()
            query = Query(self.query)
            selected_lessons = filter(
                query.match,
                self.timetable['lessons']
            )
            return selected_lessons


class TimetableParser:
    def __init__(self, filtered_timetable):
        self.filtered_timetable = [{k: v for k, v in item.items()} for item in filtered_timetable ]

    def timetable_by_weeks(self):
        week_list = ["-p", "-n"]
        taken_time_by_week = {}
        for week in week_list:
            taken_time_by_week[week] = self.generate_timetable_by_day(week)
        return taken_time_by_week

    def generate_timetable_by_day(self, week):
        timetable_data = TimetableData()
        days = timetable_data.get_week_days()
        hours = timetable_data.get_hours()
        timetable_by_day = {}

        for day_num, val in days.items():
            timetable_by_day[day_num] = {}
            for hour in hours:
                query = Query(
                    {"$and": [{"day": day_num}, {"hour": hour}]}
                )

                lessons_to_append = filter(
                    query.match,
                    self.filtered_timetable
                )

                timetable_by_day[day_num][hour] = []

                for lesson in lessons_to_append:
                    if (
                            week in lesson['subject'] or
                            week in lesson['teacher'] or
                            week in lesson['classroom']
                    ):
                        lesson['subject'] = re.sub("(-p.*)|(-n.*)", "", lesson['subject'])
                        lesson['teacher'] = re.sub("(-p.*)|(-n.*)", "", lesson['teacher'])
                        lesson['classroom'] = re.sub("(-p.*)|(-n.*)", "", lesson['classroom'])

                        timetable_by_day[day_num][hour].append(lesson)

        return timetable_by_day
