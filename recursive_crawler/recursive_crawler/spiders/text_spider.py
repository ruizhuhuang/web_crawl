import re
import os
import sys
import json
import scrapy
from urlparse import urlparse
import time, random

 
from scrapy.spiders import Spider
from scrapy.selector import Selector
import html2text
from scrapy.selector import HtmlXPathSelector
 
#sys.setrecursionlimit(30)

class RecursiveSpider(Spider):
    #set the search result here
    name = 'RecursiveSpider'
    #allowed_domains = ['www.google.com']
    def __init__(self, url,out_dir,file_name_prefix, *args, **kwargs):
        super(RecursiveSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['%s' % url]
        #dir_name = url
        #dir_name = dir_name.replace("http://","")
        #dir_name = dir_name.replace("https://","")
        #dir_name = dir_name.replace("www.", "")
        self.dir_name = out_dir
        self.prefix = file_name_prefix
        #if not os.path.exists(dir_name):
        #    os.makedirs(dir_name)
        #print ("making dir: " + dir_name)
        self.i=0     

    def getDomain(self, response):
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return domain
 
    def getSameDomainURL(self, domain, response):
        try:
            sel = Selector(response)
            urls = set([response.urljoin(href.extract()) for href in sel.xpath('//@href')])
            urls_same_domain = [url for url in urls if url.startswith(domain)]
            return urls_same_domain
        except AttributeError:
            pass

    def parse(self, response):
	yield scrapy.Request(response.url, callback=self.parse_links_follow_next_page)
            
    def parse_links_follow_next_page(self, response):
        try:
            sel = scrapy.Selector(response)
            sample = sel.xpath("/*").extract()[0]
            converter = html2text.HTML2Text()
            converter.ignore_links = True
            wt = random.uniform(1, 2)
            time.sleep(wt)
            filename = self.prefix+ '.' + str(self.i)
            index_filename = self.prefix + '.' + "index" 
            print("Save file: %s"% filename)
            print(response.url)
            with open(self.dir_name + '/'+filename, 'wb') as f:
                f.write(converter.handle(sample).encode('utf-8'))
	    with open(self.dir_name + '/'+ index_filename, "a") as f:
                f.write(filename + "," + response.url + "\n")
            self.i = self.i + 1
        except AttributeError:
            print("AttributeError")
        
        #domain = self.getDomain(response)
        if response.meta.get('domain'):
            domain= response.meta.get('domain')
        else:            
            domain=self.getDomain(response)
        next_page_urls = self.getSameDomainURL(domain, response)
        if next_page_urls:
            for url in next_page_urls:
                 yield scrapy.Request(url, self.parse_links_follow_next_page,meta = {'domain':self.getDomain(response)})


