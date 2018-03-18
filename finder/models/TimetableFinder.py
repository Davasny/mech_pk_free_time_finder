from finder import app, logger
from mongoquery import Query, QueryError
import json


class TimetableFinder():
    def __init__(self, **kwargs):
        self.json_query = "{}"

        if "query" in kwargs:
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
