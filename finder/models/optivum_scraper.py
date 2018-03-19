"""
    Forked from not7cd
    Compatible with VULCAN using <div> and <p> instead of <ul> and <li> in lista.html
"""
import json
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import random
import re
from finder import app, logger


class OptivumScraper:
    def __init__(self, base_url):
        logger.info("Updating timetable")
        self.s = requests.Session()
        self.base_url = base_url

        new_timetable = self.get_timetable()
        if len(new_timetable) > 0:
            app.timetable = new_timetable

        with open('timetable.json', 'w', encoding="utf-8") as file:
            json.dump(new_timetable, file, ensure_ascii=False)

        logger.info("Timetable updated")

    def get_soup(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/64.0.3282.168 '
                          'Safari/537.36 '
                          'OPR/51.0.2830.40'
        }
        sleep(random.uniform(0, 0.2))
        logger.debug("Getting:\t{}".format(url))
        response = self.s.get(url, headers=headers)
        response.encoding = "utf-8"

        return bs(response.text, 'html.parser')

    def parse_sitemap(self, sitemap):
        return (
            {
                link['href'].replace("plany/", ""): link.string for link in div.find_all('a')
            } for div in sitemap.find_all(("div", {"class": ["blk", "nblk"]}))
        )

    def get_sitemap_date(self, first_classroom):
        td_right = self.get_soup("{}plany/{}".format(self.base_url, first_classroom)).findAll("td", {"align" : "right"})
        for td in td_right:
            text = td.get_text().strip()
            if "wygenerowano" in text:
                return re.search("(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d", text).group()
        return "01.01.1900"

    def get_lessons_from_table(self, table, classroom):
        rows = table.find_all('tr')
        classroom_lessons = []

        for row in rows[1:]:
            hours = row.find(class_='g').get_text().strip().replace(" ", "")

            for weekday, cell in enumerate(row.find_all(class_='l')):
                teacher = cell.find_all('a', class_='n')  # naucyciel
                if len(teacher) > 0:
                    teacher = self.teachers[teacher[0]['href']]
                else:
                    teacher = None

                subject = cell.find_all('span', class_='p')  # przedmiot
                if len(subject) > 0:
                    subject = subject[0].string
                else:
                    subject = None

                groups = []
                if cell.find_all('a', class_='o') is not None:
                    groups = [group.string for group in cell.find_all('a', class_='o')]  # oddział

                lesson_dict = {
                    "day": weekday+1,
                    "hour": hours,
                    "teacher": teacher,
                    "group": groups,
                    "subject": subject,
                    "classroom": classroom
                }
                if teacher is not None or len(groups) > 0 or subject is not None:
                    classroom_lessons.append(lesson_dict)
        return classroom_lessons

    def get_lessons(self, objects):
        lessons = []
        for key, val in objects.items():
            table = self.get_soup("{}plany/{}".format(self.base_url, key)).find('table', class_='tabela')
            classroom_lessons = self.get_lessons_from_table(table, val)

            if len(classroom_lessons) > 0:
                lessons = lessons + classroom_lessons
            else:
                logger.debug("Empty class:\t{}\t{}".format(key, val))
        return lessons

    def get_timetable(self):
        sitemap = self.get_soup(self.base_url + 'lista.html')
        units, self.teachers, classrooms = self.parse_sitemap(sitemap)

        date_valid = self.get_sitemap_date(list(classrooms.keys())[0])

        return {'valid_from': date_valid, 'lessons': self.get_lessons(classrooms)}
