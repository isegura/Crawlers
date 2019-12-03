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
from itertools import permutations 
import string


abc=list(string.ascii_lowercase)
abc.append('0-9')

#for subset in itertools.combinations(abc, 2):

LIST_URLS=[]
#i=0
for subset in permutations(abc, 2):
    #print(subset)
    c=subset[0]+subset[1]
    url='https://www.drugs.com/alpha/'+c+'.html'
    #print(url)
    LIST_URLS.append(url)
#    i+=1
#    if i==100:
#        break
       

class DrugSpider(scrapy.Spider):
    name = 'DrugSpider'
    start_urls = LIST_URLS

    def parse(self, response):
        sel = Selector(response)
        fout=open('drugs.csv',mode='w')
        fcsv=csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        items=sel.css('ul[class=ddc-list-column-2] li a::text').extract()
        for item in items:
            try:
                #print(item)
                fcsv.writerow([item])
            except:
                pass
        
        fout.close()
        print('drugs file created')
    
 