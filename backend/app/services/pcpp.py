import os, requests
import sys
import re
from dotenv import load_dotenv
from decimal import Decimal
from pypartpicker import Scraper, Part, Product
from ..models.preferences import Preferences
from ..models.computer import Computer, Component, FailedURL

load_dotenv()
scraperAPI = os.environ["SCRAPER_API_KEY"]

def scraperapi_response_retriever(url, **kwargs):
    scraperapi_url = f"http://api.scraperapi.com/?api_key={scraperAPI}&url={url}"
    response = requests.get(scraperapi_url, **kwargs)
    response.raise_for_status()
    return response


pcpp = Scraper(response_retriever=scraperapi_response_retriever)


class ScraperService:
    
    def load_cpus(self):
        cpus = pcpp.part_search("processor", limit = 1375)

        for cpu in cpus:
            if cpu.price and cpu.url:
                pcpp_url = cpu.url

                if Component.objects.filter(pcpp_url=pcpp_url).exists():
                    print(f"Skipping {pcpp_url} as it already exists in the database.")
                    continue

                image_url = cpu.image
                try:
                    product = pcpp.fetch_product(pcpp_url)
                except Exception as e:
                    print(f"Error fetching product details for {pcpp_url}: {e}")
                    if FailedURL.objects.filter(url=pcpp_url).exists():
                        print(f"Skipping FailedURL as it already exists in the database.")
                        continue
                    failed_url = FailedURL(url=pcpp_url)
                    failed_url.save()
                    continue

                price = float(cpu.price.replace("$", "").replace("+", "").strip())
                specs = product.specs
                rating = None
                if hasattr(product, 'rating') and product.rating:
                    rating_string = product.rating
                    rating = self.extract_average_rating(rating_string)

                cpu_entry = Component(
                    type = product.type,
                    name=product.name,
                    price=price,
                    pcpp_url=pcpp_url,
                    specs=specs,
                    image_url=image_url,
                    rating=rating,
                )
                cpu_entry.save()


    def load_gpus(self):
        gpus = pcpp.part_search("video card", limit = 6000)

        for gpu in gpus:
            if gpu.price and gpu.url:
                pcpp_url = gpu.url

                if Component.objects.filter(pcpp_url=pcpp_url).exists():
                    print(f"Skipping {pcpp_url} as it already exists in the database.")
                    continue

                image_url = gpu.image
                try:
                    product = pcpp.fetch_product(pcpp_url)
                except Exception as e:
                    print(f"Error fetching product details for {pcpp_url}: {e}")
                    if FailedURL.objects.filter(url=pcpp_url).exists():
                        print(f"Skipping FailedURL as it already exists in the database.")
                        continue
                    failed_url = FailedURL(url=pcpp_url)
                    failed_url.save()
                    continue

                price = float(gpu.price.replace("$", "").replace("+", "").strip())
                specs = product.specs
                rating = None
                if hasattr(product, 'rating') and product.rating:
                    rating_string = product.rating
                    rating = self.extract_average_rating(rating_string)

                gpu_entry = Component(
                    type = product.type,
                    name=product.name,
                    price=price,
                    pcpp_url=pcpp_url,
                    specs=specs,
                    image_url=image_url,
                    rating=rating,
                )
                gpu_entry.save()

    def load_motherboards(self):
        motherboards = pcpp.part_search("motherboard", limit = 4000)

        for motherboard in motherboards:
            if motherboard.price and motherboard.url:
                pcpp_url = motherboard.url

                if Component.objects.filter(pcpp_url=pcpp_url).exists():
                    print(f"Skipping {pcpp_url} as it already exists in the database.")
                    continue

                image_url = motherboard.image
                try:
                    product = pcpp.fetch_product(pcpp_url)
                except Exception as e:
                    print(f"Error fetching product details for {pcpp_url}: {e}")
                    if FailedURL.objects.filter(url=pcpp_url).exists():
                        print(f"Skipping FailedURL as it already exists in the database.")
                        continue
                    failed_url = FailedURL(url=pcpp_url)
                    failed_url.save()
                    continue

                price = float(motherboard.price.replace("$", "").replace("+", "").strip())
                specs = product.specs
                rating = None
                if hasattr(product, 'rating') and product.rating:
                    rating_string = product.rating
                    rating = self.extract_average_rating(rating_string)

                motherboard_entry = Component(
                    type = product.type,
                    name=product.name,
                    price=price,
                    pcpp_url=pcpp_url,
                    specs=specs,
                    image_url=image_url,
                    rating=rating,
                )
                motherboard_entry.save()

    def load_ram(self):
        rams = pcpp.part_search("memory", limit = 5000)

        for ram in rams:
            if ram.price and ram.url:
                pcpp_url = ram.url

                if Component.objects.filter(pcpp_url=pcpp_url).exists():
                    print(f"Skipping {pcpp_url} as it already exists in the database.")
                    continue

                image_url = ram.image
                try:
                    product = pcpp.fetch_product(pcpp_url)
                except Exception as e:
                    print(f"Error fetching product details for {pcpp_url}: {e}")
                    if FailedURL.objects.filter(url=pcpp_url).exists():
                        print(f"Skipping FailedURL as it already exists in the database.")
                        continue
                    failed_url = FailedURL(url=pcpp_url)
                    failed_url.save()
                    continue

                price = float(ram.price.replace("$", "").replace("+", "").strip())
                specs = product.specs
                rating = None
                if hasattr(product, 'rating') and product.rating:
                    rating_string = product.rating
                    rating = self.extract_average_rating(rating_string)

                ram_entry = Component(
                    type = product.type,
                    name=product.name,
                    price=price,
                    pcpp_url=pcpp_url,
                    specs=specs,
                    image_url=image_url,
                    rating=rating,
                )
                ram_entry.save()

    
    def load_cpu_cooler(self):
        cpu_coolers = pcpp.part_search("cpu cooler", limit = 200)

        for cpu_cooler in cpu_coolers:
            if cpu_cooler.price and cpu_cooler.url:
                pcpp_url = cpu_cooler.url

                if Component.objects.filter(pcpp_url=pcpp_url).exists():
                    print(f"Skipping {pcpp_url} as it already exists in the database.")
                    continue

                image_url = cpu_cooler.image
                try:
                    product = pcpp.fetch_product(pcpp_url)
                except Exception as e:
                    print(f"Error fetching product details for {pcpp_url}: {e}")
                    if FailedURL.objects.filter(url=pcpp_url).exists():
                        print(f"Skipping FailedURL as it already exists in the database.")
                        continue
                    failed_url = FailedURL(url=pcpp_url)
                    failed_url.save()
                    continue

                price = float(cpu_cooler.price.replace("$", "").replace("+", "").strip())
                specs = product.specs
                rating = None
                if hasattr(product, 'rating') and product.rating:
                    rating_string = product.rating
                    rating = self.extract_average_rating(rating_string)

                cpu_cooler_entry = Component(
                    type = product.type,
                    name=product.name,
                    price=price,
                    pcpp_url=pcpp_url,
                    specs=specs,
                    image_url=image_url,
                    rating=rating,
                )
                cpu_cooler_entry.save()

    def load_psu(self):
        psus = pcpp.part_search("power supply", limit = 1000)

        for psu in psus:
            if psu.price and psu.url:
                pcpp_url = psu.url

                if Component.objects.filter(pcpp_url=pcpp_url).exists():
                    print(f"Skipping {pcpp_url} as it already exists in the database.")
                    continue

                image_url = psu.image
                try:
                    product = pcpp.fetch_product(pcpp_url)
                except Exception as e:
                    print(f"Error fetching product details for {pcpp_url}: {e}")
                    if FailedURL.objects.filter(url=pcpp_url).exists():
                        print(f"Skipping FailedURL as it already exists in the database.")
                        continue
                    failed_url = FailedURL(url=pcpp_url)
                    failed_url.save()
                    continue

                price = float(psu.price.replace("$", "").replace("+", "").strip())
                specs = product.specs
                rating = None
                if hasattr(product, 'rating') and product.rating:
                    rating_string = product.rating
                    rating = self.extract_average_rating(rating_string)

                psu_entry = Component(
                    type = product.type,
                    name=product.name,
                    price=price,
                    pcpp_url=pcpp_url,
                    specs=specs,
                    image_url=image_url,
                    rating=rating,
                )
                psu_entry.save()

    def load_storage(self):
        storages = pcpp.part_search("ssd", limit = 1000)

        for storage in storages:
            if storage.price and storage.url:
                pcpp_url = storage.url

                if Component.objects.filter(pcpp_url=pcpp_url).exists():
                    print(f"Skipping {pcpp_url} as it already exists in the database.")
                    continue

                image_url = storage.image
                try:
                    product = pcpp.fetch_product(pcpp_url)
                except Exception as e:
                    print(f"Error fetching product details for {pcpp_url}: {e}")
                    if FailedURL.objects.filter(url=pcpp_url).exists():
                        print(f"Skipping FailedURL as it already exists in the database.")
                        continue
                    failed_url = FailedURL(url=pcpp_url)
                    failed_url.save()
                    continue

                price = float(storage.price.replace("$", "").replace("+", "").strip())
                specs = product.specs
                rating = None
                if hasattr(product, 'rating') and product.rating:
                    rating_string = product.rating
                    rating = self.extract_average_rating(rating_string)

                storage_entry = Component(
                    type = product.type,
                    name=product.name,
                    price=price,
                    pcpp_url=pcpp_url,
                    specs=specs,
                    image_url=image_url,
                    rating=rating,
                )
                storage_entry.save()

    def load_cases(self):
        cases = pcpp.part_search("case", limit = 1000)

        for case in cases:
            if case.price and case.url:
                pcpp_url = case.url

                if Component.objects.filter(pcpp_url=pcpp_url).exists():
                    print(f"Skipping {pcpp_url} as it already exists in the database.")
                    continue

                image_url = case.image
                try:
                    product = pcpp.fetch_product(pcpp_url)
                except Exception as e:
                    print(f"Error fetching product details for {pcpp_url}: {e}")
                    if FailedURL.objects.filter(url=pcpp_url).exists():
                        print(f"Skipping FailedURL as it already exists in the database.")
                        continue
                    failed_url = FailedURL(url=pcpp_url)
                    failed_url.save()
                    continue

                price = float(case.price.replace("$", "").replace("+", "").strip())
                specs = product.specs
                rating = None
                if hasattr(product, 'rating') and product.rating:
                    rating_string = product.rating
                    rating = self.extract_average_rating(rating_string)

                case_entry = Component(
                    type = product.type,
                    name=product.name,
                    price=price,
                    pcpp_url=pcpp_url,
                    specs=specs,
                    image_url=image_url,
                    rating=rating,
                )
                case_entry.save()


    def extract_average_rating(self, rating_string):
        match = re.search(r'(\d+\.\d+)', rating_string)
        if match:
            return Decimal(match.group(1))
        return None
