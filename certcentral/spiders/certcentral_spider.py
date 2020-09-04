from urllib.parse import urljoin

import scrapy
from scrapy.utils.python import to_unicode
from scrapy.shell import inspect_response

class MySpider(scrapy.Spider):
    name = 'certcentral'
    base_url = 'https://localhost.digicert.com'
    allowed_domains = ['localhost.digicert.com']     # Restrict to the following domain only
    handle_httpstatus_list = [301, 302, 500]
    urls = set()

    '''starts here Yay '''
    def start_requests(self):
        # https://stackoverflow.com/questions/39776377/cant-get-scrapy-to-parse-and-follow-301-302-redirects
        yield scrapy.http.FormRequest('https://localhost.digicert.com/account/login.php', callback=self.login)

    ''' pass login paramters here ''' 
    def login(self, response):
        yield scrapy.http.FormRequest.from_response(response, formdata={'username': 'cc.admin', 'password': 'nothing'}, formid='login-form', callback=self.redirect)

    ''' redirect after login '''
    def redirect(self, response):
        print(response.status)
        if response.status in [301, 302]:
            if '/secure' in to_unicode(response.headers['Location']):
                yield scrapy.http.Request(urljoin(response.request.url, to_unicode(response.headers['Location'])), callback=self.parse)
            else:
                yield scrapy.http.Request(urljoin(response.request.url, to_unicode(response.headers['Location'])), callback=self.redirect)
            
    ''' process urls from the response '''
    def yield_urls_from_response(self, response):
        for href in response.xpath('//a[starts-with(@href, "/secure")]/@href').getall():
            yield response.urljoin(href)

    ''' crawl the urls in recursion '''
    def parse(self, response):
        self.urls.add(response.url)
        yield {'url': response.url, 'status': response.status}
        for url in self.yield_urls_from_response(response):
            if  not url in self.urls:
                yield scrapy.Request(url, callback=self.parse)
 
