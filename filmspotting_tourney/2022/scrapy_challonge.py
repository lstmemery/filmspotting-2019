import scrapy
from scrapy.crawler import CrawlerProcess
import re


class ChallongeSpider(scrapy.Spider):
    name = "filmspotting"

    def start_requests(self):
        urls = [f"https://challonge.com/madness2023/predictions?page={i}" for i in range(1, 4)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for prediction_link in response.css('a::attr(href)').getall():
            if 'https://challonge.com/tournaments/12520571/predictions' in prediction_link:
                yield scrapy.Request(prediction_link, callback=self.parse_prediction)

    def parse_prediction(self, response):
        predictions = response.css('[data-react-class="PredictionController"]')
        parsed_predictions = re.findall('\d{9},\d,\d{9}', predictions.attrib['data-react-props'])
        with open('/home/deadhand/Documents/filmspotting-2019/results/2023_predictions.csv', 'a') as results:
            results.writelines([f'{line}\n' for line in parsed_predictions])
        return None


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(ChallongeSpider)
process.start()
