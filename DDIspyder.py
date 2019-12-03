#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:11:43 2019

@author: isegura
"""



# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import csv

#fout=open('drugs.csv',mode='w')
#fcsv=csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#fcsv.writerow(['aspirin'])
#fcsv.writerow(['alprazolam'])
#fcsv.writerow(['diazepam'])
#fcsv.writerow(['donepezil'])
#fcsv.writerow(['metronidazole'])
#fout.close()


with open('drugs.csv', 'r') as f:
  reader = csv.reader(f)
  list_drugs = list(reader)


LIST_URLS=[]
for drug in list_drugs:
    url='https://www.drugs.com/drug-interactions/'+drug[0]+'-index.html'
    LIST_URLS.append(url)
    print(url)
    


class DDISpider(scrapy.Spider):
    name = 'DDISpider'
    start_urls = LIST_URLS
    #start_urls = ['https://www.drugs.com/drug_information.html']
    

    def parse(self, response):
        sel = Selector(response)
        
        
    
        
        fout=open('ddis.csv',mode='w')
        columns=['drug1','drug2','severity','link']
        
        fcsv=csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fcsv.writerow(columns)
        
        severities={'int_1':'minor','int_2':'moderate','int_3':'major'}
        for s in severities.keys():
            
            #items=sel.css('li[class*='+s+'] a::text').getall()
            items=sel.css('li[class*='+s+'] a').extract()
            for item in items:
                try:
                    #print(item)
                    severity=severities[s]
                    link='https://www.drugs.com'+item[item.index('href="')+6:item.index('.html"')+5]+'?professional=1'
                    drug1=item[item.index('/drug-interactions/')+19:]
                    #print(drug1)
                    drug1=drug1[0:drug1.index('-')]
                    #print(drug1)
                    #print(link)
                    drug2=item[item.index('">')+2:]
                    drug2=drug2[0:drug2.index('</')]
                    #print('drug2',drug2)
    
                    print(drug1,drug2,severity,link)
                    fcsv.writerow([drug1,drug2,severity,link])
                except:
                    pass
        
        fout.close()
        print('file created')
        
        
        
# the wrapper to make it run more times
#def run_spider(spider):
#    def f(q):
#        try:
#            runner = crawler.CrawlerRunner()
#            deferred = runner.crawl(spider)
#            deferred.addBoth(lambda _: reactor.stop())
#            reactor.run()
#            q.put(None)
#        except Exception as e:
#            q.put(e)
#
#    q = Queue()
#    p = Process(target=f, args=(q,))
#    p.start()
#    result = q.get()
#    p.join()
#
#    if result is not None:
#        raise result
        
#$ scrapy runspider drugsspyder.py
        
#        
#print('first run:')
#run_spider(DrugsSpider)
#
#print('\nsecond run:')
#run_spider(DrugsSpider)