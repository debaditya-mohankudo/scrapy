import scrapy
from scrapy.shell import inspect_response
import time

#manuaully extracted from browser
cookie_str = {"AMCV_9A343704532966210A490D44@AdobeOrg":"1585540135|MCIDTS|18509|MCMID|09054645748687079524638636162147602525|MCOPTOUT-1599202482s|NONE|vVersion|4.4.0","AMCVS_9A343704532966210A490D44@AdobeOrg":"1","check":"true","event69":"event69","incap_ses_710_1323850":"bh0IWvRhOUXq5LHwWG3aCelyUV8AAAAAPjj9AdsabMUBQkc2NZjnEg==","liveagent_oref":"https://localhost.digicert.com/account/login.php","liveagent_ptid":"87019a1e-87e8-4914-bdd8-620d6d0d4ab8","liveagent_sid":"87019a1e-87e8-4914-bdd8-620d6d0d4ab8","liveagent_vc":"2","mbox":"session#6049d5391afa4292a20adeddcc905460#1599197127","OptanonAlertBoxClosed":"2020-09-01T01:47:01.328Z","OptanonConsent":"isIABGlobal=false&datestamp=Fri+Sep+04+2020+10:24:42+GMT+0530+(India+Standard+Time)&version=6.2.0&consentId=22c3aa66-48b4-483e-8b13-241f37815b30&interactionCount=1&landingPath=NotLandingPage&groups=C0003:1,C0001:1,C0004:1,C0002:1,BG3:1&hosts=&legInt=&geolocation=IN;KA&AwaitingReconsent=false","PHPSESSID":"sCBSC71Lgf5lpOUwExI18CuiNUQuPQnp--FQrfg52AQ1NInV","s_cc":"true","s_gpv":"no value","s_nr":"1599195295653-Repeat","s_sq":"[[B]]","uAuthId":"9a8c65f1-0a7a-4410-ad72-fc0173791ba2","visid_incap_1323850":"JNZCUgCoTOyfhEVMGn+CS+hyUV8AAAAAQUIPAAAAAAC3e6lc/kmFhWz3oJKGXClm"}

class MySpider(scrapy.Spider):
    name = 'certcentral'
    allowed_domains = ['localhost.digicert.com']
  

    # https://stackoverflow.com/questions/39776377/cant-get-scrapy-to-parse-and-follow-301-302-redirects

    handle_httpstatus_list = [301, 302]
    
    def start_requests(self):
        yield scrapy.http.FormRequest('https://localhost.digicert.com/account/login.php', callback=self.login)
        
    def login(self, response):
        #print(response.text)
        yield scrapy.http.FormRequest.from_response(response, 
                formdata={'username': 'cc.admin', 
                'password': 'nothing', 
                'csrf_token': response.xpath('//input[@name="csrf_token"]/@value').get()},
                formid='login-form',
                callback=self.redirect_one)

    def redirect_one(self, response):
        yield scrapy.http.Request('https://localhost.digicert.com/account/', callback=self.redirect_two)
    
    def redirect_two(self, response):
        yield scrapy.http.Request('https://localhost.digicert.com/account/index-entry.php', callback=self.get_home)
    
    def get_home(self, response):
        yield scrapy.http.Request('https://localhost.digicert.com/secure/', callback=self.parse)

    def parse(self, response):
        #print(response.text)
        for href in response.xpath('//a[starts-with(@href, "/secure")]/@href').getall():         
            yield scrapy.Request(response.urljoin(href), callback=self.collect_data)
    
    def collect_data(self, response):
        yield {
            'url': response.url, 
            'status': response.status, 
            'input_fields': response.xpath('//input/@name').getall(),
            'has_csrf' : "csrf_token" in response.xpath('//input/@name').getall()
        } 
        self.parse(response)
       


            



            

