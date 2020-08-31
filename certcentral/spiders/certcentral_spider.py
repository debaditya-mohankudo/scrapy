import scrapy
from scrapy.shell import inspect_response


#manuaully collected
cookie_str ={"AMCV_9A343704532966210A490D44@AdobeOrg":"1585540135|MCIDTS|18505|MCMID|81353692662500079344226340519114315472|MCOPTOUT-1598868447s|NONE|vVersion|4.4.0","AMCVS_9A343704532966210A490D44@AdobeOrg":"1","check":"true","event69":"event69","incap_ses_706_1323850":"vo9yBAzEkVrP9X9VbDfMCd3jS18AAAAAHvWn73BYSBpdWRGc0HoxHQ==","liveagent_oref":"https://localhost.digicert.com/account/login.php","liveagent_ptid":"fde85430-ee3b-489d-9637-bebf183a7734","liveagent_sid":"fde85430-ee3b-489d-9637-bebf183a7734","liveagent_vc":"2","mbox":"session#13cfee3a3f8c4b0a9b30c24860b777b2#1598861878","OptanonAlertBoxClosed":"2020-08-30T16:15:17.080Z","OptanonConsent":"isIABGlobal=false&datestamp=Mon+Aug+31+2020+13:37:28+GMT+0530+(India+Standard+Time)&version=6.2.0&consentId=7255a34f-5498-41e2-8670-c3895c184b13&interactionCount=1&landingPath=NotLandingPage&groups=C0003:1,C0001:1,C0004:1,C0002:1,BG3:1&hosts=&legInt=&geolocation=IN;KA&AwaitingReconsent=false","PHPSESSID":"2sH62jScFVeF70bYVzdoorTwhJgeiv,XyleqGNYZ3PiN-BaS","s_cc":"true","s_gpv":"digicert:us:account:login","s_nr":"1598861288180-Repeat","s_sq":"veritassymantecwebsitesecurity=%26c.%26a.%26activitymap.%26page%3Ddigicert%253Aus%253Aaccount%253Alogin%26link%3DSign%2520in%26region%3Dlogin-form%26pageIDType%3D1%26.activitymap%26.a%26.c%26pid%3Ddigicert%253Aus%253Aaccount%253Alogin%26pidt%3D1%26oid%3DSign%2520in%26oidt%3D3%26ot%3DSUBMIT","uAuthId":"894b967a-cc79-442e-ae6c-dd80d6ac1276","visid_incap_1323850":"s5ntItKpTxmlfhiwEMqlZdzjS18AAAAAQUIPAAAAAAAgqvqvujjxQZsClhg0ooy7"}



class MySpider(scrapy.Spider):
    name = 'certcentral'
    allowed_domains = ['localhost.digicert.com']

    def start_requests(self):
        yield scrapy.http.Request('https://localhost.digicert.com/secure', cookies=cookie_str)

    def parse(self, response):
        for href in response.xpath('//a[starts-with(@href, "/secure")]/@href').getall():
            if '/private/' not in href:
                yield {'url': response.urljoin(href), 'status': response.status}
                yield scrapy.Request(response.urljoin(href), cookies=cookie_str, callback=self.parse)
            



            

