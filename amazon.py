import scrapy
from ..items import AmazoncrawlingItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = [
        'https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011%2Cp_n_feature_browse-bin%3A2656020011&dc&page=1&qid=1610635654&rnid=618072011&ref=sr_pg_1'
    ]
    page_number = 2

    def parse(self, response):
        items = AmazoncrawlingItem()

        product_name = response.css('.a-color-base.a-text-normal::text').extract()  # single class thats why ::text
        product_author = response.css(
            '.sg-col-12-of-16+ .sg-col-12-of-16 .a-color-secondary .a-size-base+ .a-size-base , .a-color-secondary .a-size-base+ .a-size-base:nth-child(4) , .a-color-secondary .a-size-base.a-link-normal').css(
            '::text').extract()  # multiple class hence, .css('::text")
        product_price = response.css(
            '.a-price-decimal , .a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole').css(
            '::text').extract()
        product_imagelink = response.css('.s-image::attr(src)').extract()

        # storing data
        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_imagelink'] = product_imagelink

        yield items

        next_page = 'https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011%2Cp_n_feature_browse-bin%3A2656020011&dc&page=' + str(AmazonSpider.page_number) + '&qid=1610635654&rnid=618072011&ref=sr_pg_2'
        if AmazonSpider.page_number <= 75:
            AmazonSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
