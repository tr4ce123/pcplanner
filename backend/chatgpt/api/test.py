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
parts = pcpp.part_search("i9")
parts2 = pcpp.part_search("motherboard")

# iterates through every part object
for part in parts:
    # prints the name of the part
    print(part.name)

for part in parts2:
    print(part.name)

# gets the first product and fetches its URL
first_product_url = parts[0].url
first_product_url_mobo = parts2[0].url
# gets the Product object for the item
product = pcpp.fetch_product(first_product_url)
product2 = pcpp.fetch_product(first_product_url_mobo)

# prints the product's specs using the specs attribute
print(f"Product 1: {product.specs} ")
print(f"Product 2: {product2.specs} ")


def check_compatible_cpu(cpu: Product, mobo: Product) -> bool:
    if cpu.specs["Socket"] == mobo.specs["Socket / CPU"]:
        print("Parts are compatible")
    else:
        print("Parts are not compatible")


check_compatible_cpu(product, product2)

print(product.price)
print(product2.price)


print(product.compatible_parts)
print(product.image)
print(product.price_list)
print(product.type)
print(product.url)
