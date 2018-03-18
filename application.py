from finder import application
import optparse
from finder.models.optivum_scraper import OptivumScraper
from flask_apscheduler import APScheduler
import os.path


class Config(object):
    JOBS = [
        {
            'id': 'scraper_job',
            'func': 'application:scraper_job',
            'trigger': 'interval',
            'seconds': 3600
        }
    ]
    SCHEDULER_API_ENABLED = True


def scraper_job():
    OptivumScraper("http://aslan.mech.pk.edu.pl/~podzial/stacjonarne/html/")


def flask_run(default_host="localhost",
                  default_port="5000"):

    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname/IP of system " + \
                           "[default %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Port for the system " + \
                           "[default %s]" % default_port,
                      default=default_port)
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    application.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(application)
    scheduler.start()

    if not os.path.isfile("timetable.json"):
        scheduler.run_job("scraper_job")

    application.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port),
        threaded=True,
    )


if __name__ == '__main__':
    flask_run()
