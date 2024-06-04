from time import sleep
from pypartpicker import Scraper, Product
import requests, os
from dotenv import load_dotenv


load_dotenv()
scraperAPI = os.environ["SCRAPER_API_KEY"]


def scraperapi_response_retriever(url, **kwargs):
    scraperapi_url = f"http://api.scraperapi.com/?api_key={scraperAPI}&url={url}"
    response = requests.get(scraperapi_url, **kwargs)
    response.raise_for_status()
    return response


pcpp = Scraper(response_retriever=scraperapi_response_retriever)

# creates the scraper object
# returns a list of Part objects we can iterate through
cpu = pcpp.part_search("processor")
cpu_cooler = pcpp.part_search("cpu cooler", limit=100)
gpu = pcpp.part_search("video card", limit=100)
mobo = pcpp.part_search("motherboard", limit=100)
ram = pcpp.part_search("memory", limit=100)
psu = pcpp.part_search("power supply", limit=100)
ssd = pcpp.part_search("ssd", limit=100)
case = pcpp.part_search("case", limit=100)

print("")
print("----------------")
print("PROCESSORS")
print("----------------")
print("")
for processor in cpu:
    if processor.price:
        if float(processor.price.strip("$")) <= 270:
            print(processor.name + " - " + processor.price)

print("")
print("----------------")
print("CPU COOLERS")
print("----------------")
print("")
for cooler in cpu_cooler:
    if cooler.price:
        if float(cooler.price.strip("$")) <= 60:
            print(cooler.name + " - " + cooler.price)

print("")
print("----------------")
print("GRAPHICS CARDS")
print("----------------")
print("")
for card in gpu:
    if card.price:
        if float(card.price.strip("$")) <= 575:
            print(card.name + " - " + card.price + " URL " + card.url)
            

print("")
print("----------------")
print("MOTHERBOARDS")
print("----------------")
print("")
for board in mobo:
    if board.price:
        if float(board.price.strip("$")) <= 180:
            print(board.name + " - " + board.price)

print("")
print("----------------")
print("RAM")
print("----------------")
print("")
for stick in ram:
    if stick.price:
        if float(stick.price.strip("$")) <= 60:
            print(stick.name + " - " + stick.price)

print("")
print("----------------")
print("POWER SUPPLIES")
print("----------------")
print("")
for supply in psu:
    if supply.price:
        if float(supply.price.strip("$")) <= 60:
            print(supply.name + " - " + supply.price)

print("")
print("----------------")
print("STORAGE")
print("----------------")
print("")
for storage in ssd:
    if storage.price:
        if float(storage.price.strip("$")) <= 60:
            print(storage.name + " - " + storage.price)

print("")
print("----------------")
print("CASES")
print("----------------")
print("")
for case in case:
    if case.price:
        if float(case.price.strip("$")) <= 60:
            print(case.name + " - " + case.price)

# print(cpu[0].image)
# print(cpu_cooler[0].image)

# # gets the first product and fetches its URL
# first_product_url = cpu[0].url
# first_product_url_mobo = gpu[0].url
# # gets the Product object for the item
# product1 = pcpp.fetch_product(cpu[0].url)
# product2 = pcpp.fetch_product(cpu_cooler[0].url)
# product3 = pcpp.fetch_product(gpu[0].url)
# product4 = pcpp.fetch_product(mobo[0].url)
# product5 = pcpp.fetch_product(ram[0].url)
# product6 = pcpp.fetch_product(psu[0].url)
# product7 = pcpp.fetch_product(ssd[0].url)
# product8 = pcpp.fetch_product(case[0].url)


# print(product1.specs)
# print(product2.image)
# print(product3.image)
# print(product4.image)
# print(product5.image)
# print(product6.image)
# print(product7.image)
# print(product8.image)

# print(product.compatible_parts)
# print(product.image)
# print(product.price_list)
# print(product.type)
# print(product.url)
