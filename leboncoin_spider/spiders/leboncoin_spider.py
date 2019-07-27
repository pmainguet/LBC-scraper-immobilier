from __future__ import absolute_import
import json
import urllib

import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from leboncoin_spider.items import Offer

class OfferSpider(scrapy.Spider):
    name = "leboncoin_spider"
    allowed_domains = ['leboncoin.fr']

    def __init__(self,*args, **kwargs):
        self.start_urls = self.load_url()

    def parse(self, response):
        urls = LinkExtractor(allow=r'\/ventes_immobilieres\/\d+\.htm').extract_links(response)
        for url in urls:
            yield scrapy.Request(url.url, callback=self.parse_item)

    def parse_item(self,response):
        l = ItemLoader(item=Offer(),response=response)
        l.add_value('url', response.request.url)
        l.add_xpath('title', '//h1/text()')
        l.add_xpath('city', '//div[@data-qa-id="adview_location_informations"]/span/text()')
        l.add_xpath('price','//div[@data-qa-id="adview_price"]/div/span/text()[1]')
        l.add_xpath('posted_on','//div[@data-qa-id="adview_date"]/text()')
        l.add_xpath('type','//div[@data-qa-id="criteria_item_real_estate_type"]/div/div[position()=2]/text()')
        l.add_xpath('rooms','//div[@data-qa-id="criteria_item_rooms"]/div/div[position()=2]/text()')
        l.add_xpath('surface','//div[@data-qa-id="criteria_item_square"]/div/div[position()=2]/text()')
        l.add_xpath('ges','//div[@data-qa-id="criteria_item_ges"]/div/div[position()=2]/div/div[has-class("_1sd0z")]/text()')
        l.add_xpath('classe_energie','//div[@data-qa-id="criteria_item_energy_rate"]/div/div[position()=2]/div/div[has-class("_1sd0z")]/text()')
        l.add_xpath('description','//div[@data-qa-id="adview_description_container"]/div/span/text()')
        l.add_xpath('siret_agence','//li[@data-qa-id="storebox_siret"]/div/text()[2]')
        yield l.load_item()


    def load_url(self):
        
        cities = {
            'Saint-Egrève': 38120,
            'Proveysieux':38120,
            'Quaix-en-Chartreuse':38950,
            'Saint-Martin-le-Vinoux':38950,
            'Vaulnaveys-le-Haut':38410,
            'Vaulnaveys-le-Bas':38410,
            'Herbeys':38320,
            'Fontaine':38600,
            'Sassenage':38360,
            'Le Sappey-en-Chartreuse':38700,
            'Sarcenas':38700,
            'Seyssinet-Pariset':38170,
            'Seyssins':38180,
            'Bresson':38320,
            'Brié-et-Angonnes':38320,
            'Champagnier':38800,
            'Champ-sur-Drac':38560,
            'Claix':38640,
            'Corenc':38700,
            'Domène':38420,
            'Echirolles':38130,
            'Eybens':38320,
            'Fontaine':38600,
            'Fontanil-Cornillon':38120,
            'Gières':38610,
            'Le Gua':38450,
            'Herbeys':38320,
            'Jarrie':38560,
            'Meylan':38240,
            'Miribel-Lanchâtre':38450,
            'Montchaboud':38220,
            'Mont-Saint-Martin':38120,
            'Murianette':38420,
            'Notre-Dame-de-Commiers':38450,
            'Notre-Dame-de-Mésage':38220,
            'Noyarey':38360,
            'Poisat':38320,
            'Le Pont-de-Claix':38800,
            'Proveysieux':38120,
            'Quaix-en-Chartreuse':38950,
            'Saint-Barthélemy-de-Séchilienne':38220,
            'Saint-Egrève':38120,
            'Saint-Georges-de-Commiers':38450,
            'Saint-Martin-d\'Hères':38400,
            'Saint-Martin-le-Vinoux':38950,
            'Saint-Paul-de-Varces':38760,
            'Saint-Pierre-de-Mésage':38220,
            'Le Sappey-en-Chartreuse':38700,
            'Sarcenas':38700,
            'Sassenage':38360,
            'Séchilienne':38220,
            'Seyssinet-Pariset':38170,
            'Seyssins':38180,
            'La Tronche':38700,
            'Varces-Allières-et-Risset':38760,
            'Venon':38610,
            'Veurey-Voroize':38113,
            'Vif':38450,
            'Vizille':38220,
            'Grenoble':38000,
            'Voreppe':38340,
        }
        
        urls=[]

        for city in cities.items():
            urls.append("https://www.leboncoin.fr/recherche/?category=9&locations="+str(city[1])+"&real_estate_type=1")
            urls.append("https://www.leboncoin.fr/recherche/?category=9&locations="+str(city[1])+"&real_estate_type=2")
            urls.append("https://www.leboncoin.fr/recherche/?category=9&locations="+str(city[1])+"&real_estate_type=3")
        
        return urls