# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy.exceptions import DropItem
import re
import csv
import time

class LeboncoinSpiderPipeline(object):

    quartiers = [
        'Monta',
        'Rocheplaine',
        'Moutonnée',
        'Fiancey',
        'Cuvilleux',
        'Champaviotte',
        'Prédieu',
        'Pont de Vence',
        'Barnave',
        'Saint Robert',
        'Champy',
        'Vinoux',
    ]
    
    def __init__(self):
        self.urls_seen = set()

        data = []
        fn = 'url_seen.csv';
        try:
            file = open(fn, 'r')
            with file as f:
                reader = csv.DictReader(f, delimiter=',')
                for line in reader:
                    #TODO: utiliser le dict directement plutôt que le transformer en liste
                    value = list(line.items())[0][1]
                    self.urls_seen.add(value)
        except IOError:
            file = open(fn, 'w')
            with open('url_seen.csv', 'a') as fp:
                writer = csv.writer(fp, delimiter=',')
                writer.writerow(['url','timestamp_added'])

    def write_url_seen(self,url):
        self.urls_seen.add(url)
        with open('url_seen.csv', 'a') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerow([url,datetime.now().timestamp()])
    
    def process_item(self, item, spider):
        #remove duplicates
        if item['url'][0] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item['url'])
        else:
            self.write_url_seen(item['url'][0])
            item['zipcode'] = item['city'][2]
            item['city'] = item['city'][0]
            if not re.match("^38", item['zipcode']):
                raise DropItem("Item not in correct area: %s" % item)
            item['last_updated']=datetime.now().timestamp()
            item['posted_on'] = datetime.strptime(item['posted_on'][0].replace(' à ',' '), '%d/%m/%Y %Hh%M').timestamp()
            item['price']=item['price'][0].replace(' ','')
            item['time_online']=(float(item['last_updated'])-float(item['posted_on']))/(24*60*60)
            if item.get('surface'):
                item['surface']=item['surface'][0].replace(' m²','')
                item['price_surface']= int(item['price'])/int(item['surface'])
            for q in self.quartiers):
                if item['description'].find(q) >= 0:
                    item['quartier'] = q
                    break
            return item
