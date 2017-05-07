import scrapy

class ScheduleSpider(scrapy.Spider):
	download_delay = 0.5
	haveindex=None
	name = "schedule"
	allowed_domains = ["au.fctables.com"]
	start_urls = ["https://au.fctables.com"]
    
	def parse(self,response):
 		try:
 			myurl = response.css('div.alphabet >ul >li >ul >li >a::attr(href)').extract()
			for url in myurl:
				url = response.urljoin(url)
				yield scrapy.Request(url=url, callback=self.parselinks)
		except:
			print "not coming"

	def parselinks(self,response):
		try:
			leaguesUrl = response.css('div.detail >a::attr(href)').extract()
            		for urltwo in leaguesUrl:
            			urltwo = response.urljoin(urltwo+'schedule')
            			yield scrapy.Request(url=urltwo, callback=self.parsetwo)
        	except:
			leaguesUrl=None
    	def parsetwo(self,response):
 		try:
 			myurl = response.css('div.h2h > a::attr(href)').extract()
			for url in myurl:
				url = response.urljoin(url)
				yield scrapy.Request(url=url, callback=self.parseresults)
		except:
			print "not coming"

	def parseresults(self,response):
		try:
			haveindex = response.css('li strong::text').extract()[2]
		except:
			haveindex=None
		if(haveindex==None):
			print "fail"
		else:
			yield {
			'over25index':response.css('li strong::text').extract()[2],
			'teamnames':response.css('h1::text').extract_first(),
			'score':response.css('h3.game-score::text').extract_first(),
			'over25odd':response.css('div.col-xs-6.text-center::text').extract()[4],
			'under25odd':response.css('div.col-xs-6.text-center::text').extract()[5],
			}
