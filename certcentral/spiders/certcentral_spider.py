import scrapy
from scrapy.shell import inspect_response

class MySpider(scrapy.Spider):
    name = 'certcentral'
    allowed_domains = ['localhost.digicert.com']     # Restrict to the following domain only
    handle_httpstatus_list = [301, 302, 500]
    urls = set()

    '''starts here Yay '''
    def start_requests(self):
        # https://stackoverflow.com/questions/39776377/cant-get-scrapy-to-parse-and-follow-301-302-redirects
        yield scrapy.http.FormRequest('https://localhost.digicert.com/account/login.php', callback=self.login)

    ''' pass login paramters here ''' 
    def login(self, response):
        yield scrapy.http.FormRequest.from_response(response, formdata={'username': 'cc.admin', 'password': 'nothing'}, formid='login-form', callback=self.redirect_one)

    ''' redirect after login '''
    def redirect_one(self, response):
        yield scrapy.http.Request('https://localhost.digicert.com/account/', 
        callback=self.redirect_two)
    
    ''' 2nd redirect after login '''
    def redirect_two(self, response):
        yield scrapy.http.Request('https://localhost.digicert.com/account/index-entry.php', 
        callback=self.get_home)

    ''' go to /secure page '''
    def get_home(self, response):
        yield scrapy.http.Request('https://localhost.digicert.com/secure/', 
        callback=self.parse)

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
 
