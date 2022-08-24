import scrapy
from scrapy.crawler import CrawlerProcess

class MoviesSpider(scrapy.Spider):
    name = 'movies'
    start_urls = [
        'https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc',
    ]
    def __init__(self, genre, **kwargs): 
        #returns the genre sent by the celery worker 
        self.genre = genre
        super().__init__(**kwargs)

    def delete_space(self, string_item):
        #deletes the spaces existing in a string
        if not isinstance(string_item, str):
            raise TypeError("The input must be string")
        result = "" 
        for i in range(len(string_item) - 1):
            if string_item[i] == " ":
                result = string_item.replace(string_item[i], "")
        return result

    def parse_genre(self, genre_string):
        #splits genre_string in one list
        if not isinstance(genre_string, str):
            raise TypeError("The input must be string")

        genre_string_without_space = self.delete_space(genre_string).upper()
        genre_list = genre_string_without_space.split(",")
        return genre_list

    def parse(self, response):
        #returns the scrapped data
        for movie in response.css('div.lister-item-content'):
            title = movie.xpath('h3/a/text()').get()
            rank = movie.css('span.lister-item-index::text').get()
            year = movie.css('span.lister-item-year::text').get()[1:-1]
            runtime = movie.css('span.runtime::text').get()
            genre = movie.css('span.genre::text').get()[1:]
            genre_list = self.parse_genre(genre)
            if self.genre.upper() in genre_list:
                yield {
                        'Title': title,
                        'Rank': rank,
                        'Year' : year,
                        'Runtime' : runtime,
                        'Genre' : self.delete_space(genre),
                       }

        next_page = response.css('a.lister-page-next::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

