"""
    Forked from not7cd
    Compatible with VULCAN using <div> and <p> instead of <ul> and <li> in lista.html
"""
import os
import json
import requests
from urllib.parse import urlparse
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

    def extract_id(self, path):
        whole_link = urlparse(path)
        html_filename = os.path.basename(whole_link.path)
        filename_without_extension = os.path.splitext(html_filename)[0]

        return filename_without_extension

    def get_url_id(self, soup, class_):
        return self.extract_id(soup.find('a', class_=class_)['href'])

    def get_url_ids(self, soup, class_):
        return [self.extract_id(elt['href']) for elt in soup.find_all('a', class_=class_)]

    def dict_from_list(self, div):
        return {self.get_url_id(p, None): p.a.string for p in div.find_all('p')}

    def get_lesson(self, soup):
        teacher = self.get_url_id(soup, 'n')  # nauczyciel
        group = self.get_url_ids(soup, 'o')  # odział, klasa
        subject = soup.find('span', class_='p').string  # przedmiot

        return {'teacher': teacher, 'group': group, 'subject': subject}

    def get_classroom_lessons(self, table):
        rows = table.find_all('tr')
        for row in rows[1:]:
            hours = row.find(class_='g').get_text().strip().replace(" ", "")
            for weekday, lesson in enumerate(row.find_all(class_='l')):
                try:
                    yield {'day': weekday+1, 'hour': hours, **self.get_lesson(lesson)}
                except TypeError:
                    pass

    def get_all_lessons(self, classrooms):
        for classroom in classrooms:
            table = self.get_soup(self.base_url + 'plany/' + classroom + '.html').find('table', class_='tabela')
            for lesson in self.get_classroom_lessons(table):
                yield {'classroom': classroom.encode().decode(), **lesson}

    def translate_internal_id(self, lesson, units, teachers, classrooms):
        lesson['group'] = list(map(lambda elt: units[elt], lesson['group']))
        lesson['teacher'] = teachers[lesson['teacher']]
        lesson['classroom'] = classrooms[lesson['classroom']]

        return lesson

    def parse_sitemap(self, sitemap):
        return (self.dict_from_list(div) for div in sitemap.find_all(("div", {"class": ["blk", "nblk"]})))

    def get_sitemap_date(self, first_classroom):
        td_right = self.get_soup(self.base_url + 'plany/' + first_classroom + '.html').findAll("td", {"align" : "right"})
        for td in td_right:
            text = td.get_text().strip()
            if "wygenerowano" in text:
                return re.search("(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d", text).group()
        return "01.01.1900"

    def get_timetable(self):
        sitemap = self.get_soup(self.base_url + 'lista.html')

        units, teachers, classrooms = self.parse_sitemap(sitemap)
        date_valid = self.get_sitemap_date(list(classrooms.keys())[0])
        result = {'valid_from': date_valid, 'lessons': []}

        for lesson in self.get_all_lessons(classrooms):
            lesson = self.translate_internal_id(lesson, units, teachers, classrooms)
            result['lessons'].append(lesson)

        return result
