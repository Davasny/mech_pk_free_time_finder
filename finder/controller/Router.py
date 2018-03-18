from finder import app, logger
from . import MainHandler, APIHandler


app.add_url_rule('/', endpoint="index")

""" MainHandler """
app.add_url_rule('/index', view_func=MainHandler.IndexView.as_view('index'))


""" API Handler """
app.add_url_rule('/api/timetable/hours', view_func=APIHandler.TimetableHours.as_view('timetable_hours'))
app.add_url_rule('/api/timetable/teachers', view_func=APIHandler.TimetableTeachers.as_view('timetable_teachers'))
app.add_url_rule('/api/timetable/groups', view_func=APIHandler.TimetableGroups.as_view('timetable_groups'))
app.add_url_rule('/api/timetable/subjects', view_func=APIHandler.TimetableSubjects.as_view('timetable_subjects'))
app.add_url_rule('/api/timetable/classrooms', view_func=APIHandler.TimetableClassrooms.as_view('timetable_classrooms'))
