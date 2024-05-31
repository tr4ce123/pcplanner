from time import sleep
from pypartpicker import Scraper, Product
import requests

SCRAPER_API_KEY = "118f04485ac165809d11be198742cc47"


def scraperapi_response_retriever(url, **kwargs):
    scraperapi_url = f"http://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url={url}"
    response = requests.get(scraperapi_url, **kwargs)
    response.raise_for_status()
    return response


pcpp = Scraper(response_retriever=scraperapi_response_retriever)

# creates the scraper object
# returns a list of Part objects we can iterate through
cpu = pcpp.part_search("AMD Ryzen 7 5800X")
cpu_cooler = pcpp.part_search("Noctua NH-D15")
gpu = pcpp.part_search("NVIDIA GeForce GTX 1660 Super")
mobo = pcpp.part_search("MSI B450 TOMAHAWK MAX ATX AM4")
ram = pcpp.part_search("Corsair Vengeance LPX 16GB (2 x 8GB) DDR4 3200")
psu = pcpp.part_search("EVGA 600 W1, 80+ WHITE 600W")
ssd = pcpp.part_search("Samsung 970 EVO Plus 500GB")
case = pcpp.part_search("NZXT H510")


# gets the first product and fetches its URL
first_product_url = cpu[0].url
first_product_url_mobo = gpu[0].url
# gets the Product object for the item
product1 = pcpp.fetch_product(cpu[0].url)
product2 = pcpp.fetch_product(cpu_cooler[0].url)
product3 = pcpp.fetch_product(gpu[0].url)
product4 = pcpp.fetch_product(mobo[0].url)
product5 = pcpp.fetch_product(ram[0].url)
product6 = pcpp.fetch_product(psu[0].url)
product7 = pcpp.fetch_product(ssd[0].url)
product8 = pcpp.fetch_product(case[0].url)


print(product1.price)
print(product2.price)
print(product3.price)
print(product4.price)
print(product5.price)
print(product6.price)
print(product7.price)
print(product8.price)

# print(product.compatible_parts)
# print(product.image)
# print(product.price_list)
# print(product.type)
# print(product.url)
