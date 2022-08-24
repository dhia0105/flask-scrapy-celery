from twisted.internet import reactor
import tools
from scrapy.crawler import CrawlerRunner
from celery import Celery

#creates a celery object named tasks and connected to rabbitmq service 
celery = Celery('tasks', broker='rmq')
#puts the output in a csv file 
runner = CrawlerRunner(settings={
    "FEEDS": {
        "movies.csv": {"format": "csv"},
    },
})

@celery.task(name="create_task")
def create_task(genre):
    #gets genre from the flask api and creates a scrapy spider to search for movies having this genre in the top 100 movies imdb
    if not isinstance(genre, str):
        raise TypeError("The input must be string")
    d = runner.crawl(tools.MoviesSpider, genre = genre)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    return True

