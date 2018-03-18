from finder import app, logger
from . import MainHandler, APIHandler


app.add_url_rule('/', endpoint="index")

""" MainHandler """
app.add_url_rule('/index', view_func=MainHandler.IndexView.as_view('index'))
app.add_url_rule('/filter', view_func=MainHandler.FilterView.as_view('filter'))


""" API Handler """
app.add_url_rule('/api/timetable/hours', view_func=APIHandler.TimetableHours.as_view('api_timetable_hours'))
app.add_url_rule('/api/timetable/teachers', view_func=APIHandler.TimetableTeachers.as_view('api_timetable_teachers'))
app.add_url_rule('/api/timetable/groups', view_func=APIHandler.TimetableGroups.as_view('api_timetable_groups'))
app.add_url_rule('/api/timetable/subjects', view_func=APIHandler.TimetableSubjects.as_view('api_timetable_subjects'))
app.add_url_rule('/api/timetable/classrooms', view_func=APIHandler.TimetableClassrooms.as_view('api_timetable_classrooms'))
app.add_url_rule('/api/timetable/weekdays', view_func=APIHandler.TimetableWeekDays.as_view('api_timetable_weekdays'))
