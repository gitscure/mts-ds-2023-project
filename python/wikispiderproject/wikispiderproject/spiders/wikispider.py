import scrapy
import re


class WikispiderSpider(scrapy.Spider):
    name = "wikispider"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"]

    # def parse(self, response):
    #     films = response.css('div#mw-pages ul li a::text').extract()
    #     for film in films:
    #         yield {'title': film}

    def parse(self, response):
        films = response.css('div#mw-pages ul li a::attr(href)').extract()
        for film in films:
            url = response.urljoin(film)
            yield scrapy.Request(url, callback=self.parse_film_page)
        next_url = response.xpath('//a[contains(text(), "Следующая страница")]/@href').get()
        film_list_url = response.urljoin(next_url)
        if next_url:
            yield scrapy.Request(film_list_url, callback=self.parse)
        
    def parse_film_page(self, response):        
        title = response.css('h1#firstHeading > *::text').get()

        genre = response.css('span[data-wikidata-property-id="P136"] > a::text').getall() or \
            response.css('span[data-wikidata-property-id="P136"]::text').get() or \
            response.css('span[data-wikidata-property-id="P136"] > span > a::text').get() or \
            response.css('span[data-wikidata-property-id="P136"] > span > span > a > span::text').get()
        
        director = response.css('span[data-wikidata-property-id="P57"] > a::text').getall() or \
            response.css('span[data-wikidata-property-id="P57"]::text').get() or \
            response.css('span[data-wikidata-property-id="P57"] > span > a::text').get() or \
            response.css('span[data-wikidata-property-id="P57"] > span > span > a > span::text').get() or \
            response.css('span[data-wikidata-property-id="P57"] > a > span::text').get()
        
        country = response.css('span[data-wikidata-property-id="P495"] span.wrap::text').getall() or \
            response.css('span[data-wikidata-property-id="P495"] > a::text').getall() or \
            response.css('span[data-wikidata-property-id="P495"] span.country-name > span > a::text').getall() or \
            response.css('span[data-wikidata-property-id="P495"]::text').get() or \
            response.css('div[data-wikidata-property-id="P495"] span.wrap::text').getall()
        
        year_pattern = '[0-9]{4}$'

        year = response.xpath('//th[contains(text(), "Год")]/following-sibling::td/a/span/text()').getall() or \
            response.xpath('//th[contains(text(), "Год")]/following-sibling::td/span[@data-wikidata-property-id="P577"]/span/span/a/text()').getall() or \
            response.xpath('//th[contains(text(), "Год")]/following-sibling::td/a/text()').getall() or \
            response.xpath('//th[contains(text(), "Год")]/following-sibling::td/text()').getall() or \
            response.xpath('//th[contains(text(), "Дата выхода")]/following-sibling::td/a/text()').getall() or \
            response.xpath('//th[contains(text(), "Первый показ")]/following-sibling::td/span/text()').getall()
        
        year = list(set([re.search(year_pattern, y)[0] for y in year if re.search(year_pattern, y)]))

        imdb_url = response.css('span[data-wikidata-property-id="P345"] > span > a::attr(href)').extract() or \
            response.css('span[data-wikidata-property-id="P345"] > a::attr(href)').extract()

        yield {
            'title': title,
            'genre': genre,
            'director': director,
            'country': country,
            'year': year,
            'imdb': imdb_url
        }
