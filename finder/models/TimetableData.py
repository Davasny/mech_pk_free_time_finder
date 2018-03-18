from finder import app, logger
import re


class TimetableData:
    def get_hours(self):
        if 'hours' not in app.timetable:
            logger.debug("Filling hours")
            app.timetable['hours'] = []
            for lesson in app.timetable['lessons']:
                if lesson['hour'] not in app.timetable['hours']:
                    app.timetable['hours'].append(lesson['hour'])
        sorted(app.timetable['hours'])
        return app.timetable['hours']

    def get_teachers(self):
        if 'teachers' not in app.timetable:
            logger.debug("Filling teachers")
            app.timetable['teachers'] = []
            for lesson in app.timetable['lessons']:
                if lesson['teacher'] is not None:
                    teacher = re.sub("(-p.*)|(-n.*)", "", lesson['teacher']) # remove -n and -p from name
                    if teacher not in app.timetable['teachers']:
                        app.timetable['teachers'].append(teacher)
        return app.timetable['teachers']

    def get_groups(self):
        if 'groups' not in app.timetable:
            logger.debug("Filling groups")
            app.timetable['groups'] = []
            for lesson in app.timetable['lessons']:
                for group in lesson['group']:
                    if group not in app.timetable['groups']:
                        app.timetable['groups'].append(group)
        return app.timetable['groups']

    def get_subjects(self):
        if 'subjects' not in app.timetable:
            logger.debug("Filling subjects")
            app.timetable['subjects'] = []
            for lesson in app.timetable['lessons']:
                if lesson['subject'] not in app.timetable['subjects']:
                    app.timetable['subjects'].append(lesson['subject'])
        return app.timetable['subjects']

    def get_classrooms(self):
        if 'classrooms' not in app.timetable:
            logger.debug("Filling classrooms")
            app.timetable['classrooms'] = []
            for lesson in app.timetable['lessons']:
                if lesson['classroom'] is not None:
                    classroom = re.sub("(-p.*)|(-n.*)", "", lesson['classroom']) # remove -n and -p from name
                    if classroom not in app.timetable['classrooms']:
                        app.timetable['classrooms'].append(classroom)
        return app.timetable['classrooms']

    def get_week_days(self):
        days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
        week = {}
        for x in range(1, 8):
            week[x] = days[x-1]
        return week
