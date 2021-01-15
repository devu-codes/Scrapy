
#     LOGGING IN WITH SCRAPY FORMREQUEST


import scrapy
from scrapy.http import FormRequest # used to store login info
from scrapy.utils.response import open_in_browser # create local scraped page in web browser
from ..items import QuotetutorialItem

class QuoteSpider(scrapy.Spider):
   name = "quotes"
   page_number = 1
   start_urls = [
       'https://quotes.toscrape.com/login'  # change the Url
   ]

   def parse(self, response, **kwargs):
      token = response.css('form input::attr(value)').extract_first() # this is for the csrf_token via inspect as its changes everytime we logged in
      return FormRequest.from_response(response, formdata={  # we have to store response & value of all the credentials in Form Data.
         'csrf_token': token,
         'username': 'ankitpan38@gmail.com',
         'password': 'dnfinfin'
      },callback=self.start_scraping)

   def start_scraping(self, response):
      open_in_browser(response)
      items = QuotetutorialItem()

      all_div_quotes = response.css('div.quote')

      for quotes in all_div_quotes:
         title = quotes.css('span.text::text').extract()
         author = quotes.css('.author::text').extract()
         tag = quotes.css('.tag::text').extract()

         items['title'] = title
         items['author'] = author
         items['tag'] = tag

         yield items
