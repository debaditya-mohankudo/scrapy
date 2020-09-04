

import scrapy
from scrapy.shell import inspect_response


#manuaully collected
cookie_str = {"AMCV_9A343704532966210A490D44@AdobeOrg":"1585540135|MCIDTS|18509|MCMID|09054645748687079524638636162147602525|MCOPTOUT-1599112500s|NONE|vVersion|4.4.0","AMCVS_9A343704532966210A490D44@AdobeOrg":"1","check":"true","event69":"event69","liveagent_oref":"https://localhost.digicert.com/account/login.php","liveagent_ptid":"87019a1e-87e8-4914-bdd8-620d6d0d4ab8","liveagent_sid":"87019a1e-87e8-4914-bdd8-620d6d0d4ab8","liveagent_vc":"2","mbox":"session#512ca166f7554b91995a2f7b63f760f7#1599107160","OptanonAlertBoxClosed":"2020-09-01T01:47:01.328Z","OptanonConsent":"isIABGlobal=false&datestamp=Thu+Sep+03+2020+09:25:00+GMT+0530+(India+Standard+Time)&version=6.2.0&consentId=22c3aa66-48b4-483e-8b13-241f37815b30&interactionCount=1&landingPath=NotLandingPage&groups=C0003:1,C0001:1,C0004:1,C0002:1,BG3:1&hosts=&legInt=&geolocation=IN;KA&AwaitingReconsent=false","PHPSESSID":"UQwHRcLpBkCcsjHG90h4uiDC-W5UmvVO5GWax51t6pdQ0OBR","s_cc":"true","s_gpv":"digicert:us:account:login","s_nr":"1599105300001-Repeat","s_sq":"[[B]]","uAuthId":"aad1235f-87ee-4789-a750-f560c23b010b"}



class MySpider(scrapy.Spider):
    name = 'adminarea'
    allowed_domains = ['localhost.digicert.com']


    def start_requests(self):
        yield scrapy.http.Request('https://localhost.digicert.com/adminarea/', cookies=cookie_str)

    def parse(self, response):
        for href in response.xpath('//a[starts-with(@href, "/adminarea")]/@href').getall():
            if not 'logout' in href:

                print(response.urljoin(href))
                yield {'url': response.urljoin(href), 'input_fields': response.xpath('//input').getall()}
                yield scrapy.Request(response.urljoin(href), cookies=cookie_str, callback=self.parse)
            


            



            

