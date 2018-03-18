from flask import request
from .BaseHandler import BaseView
from finder.models import TimetableData
import json


class TimetableHours(BaseView):
    def get(self, *args, **kwargs):
        timetable = TimetableData.TimetableData()
        return json.dumps(timetable.get_hours(), ensure_ascii=False)


class TimetableTeachers(BaseView):
    def get(self, *args, **kwargs):
        timetable = TimetableData.TimetableData()
        return json.dumps(timetable.get_teachers(), ensure_ascii=False)


class TimetableGroups(BaseView):
    def get(self, *args, **kwargs):
        timetable = TimetableData.TimetableData()
        return json.dumps(timetable.get_groups(), ensure_ascii=False)


class TimetableSubjects(BaseView):
    def get(self, *args, **kwargs):
        timetable = TimetableData.TimetableData()
        return json.dumps(timetable.get_subjects(), ensure_ascii=False)


class TimetableClassrooms(BaseView):
    def get(self, *args, **kwargs):
        timetable = TimetableData.TimetableData()
        return json.dumps(timetable.get_classrooms(), ensure_ascii=False)


class TimetableWeekDays(BaseView):
    def get(self, *args, **kwargs):
        timetable = TimetableData.TimetableData()
        return json.dumps(timetable.get_week_days(), ensure_ascii=False)
