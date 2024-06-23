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
    # def test_computer(self, preferences: Preferences):
        
    #     total_budget = float(preferences.budget)

    #     # TODO: Optimize budget distribution and tune to different preferences such as gaming, streaming, workstation, etc.
    #     budget_distribution = {
    #         "cpu": 0.25,
    #         "cpu_cooler": 0.05,
    #         "gpu": 0.35,
    #         "motherboard": 0.15,
    #         "ram": 0.05,
    #         "psu": 0.05,
    #         "storage": 0.075,
    #         "case": 0.075,
    #     }

    #     component_budgets = {key: total_budget * value for key, value in budget_distribution.items()}

    #     def get_best_component(part_name: str, budget, additional_budget=0) -> Part:
    #         parts = pcpp.part_search(part_name, limit = 20)
    #         best_part = None
    #         max_price = 0
    #         for part in parts:
    #             if part.price and part.url:
    #                 price = float(part.price.replace("$", "").replace("+", "").strip())
    #                 if price <= budget + additional_budget and price > max_price:
    #                     max_price = price
    #                     best_part = part
    #         return best_part


    #     best_cpu = get_best_component("processor", component_budgets["cpu"], 20)
    #     cpu_image = best_cpu.image
    #     pcpp_cpu = pcpp.fetch_product(best_cpu.url)

    #     cpu = Component(
    #         name=pcpp_cpu.name,
    #         price=float(pcpp_cpu.price.replace("$", "").replace("+", "").strip()),
    #         pcpp_url=pcpp_cpu.url,
    #         specs=pcpp_cpu.specs,
    #         image_url=cpu_image,
    #     )
    #     cpu.save()

    #     best_cpu_cooler = get_best_component("cpu cooler", component_budgets["cpu_cooler"], 10)
    #     cooler_image = best_cpu_cooler.image
    #     pcpp_cpu_cooler = pcpp.fetch_product(best_cpu_cooler.url)

    #     cpu_cooler = Component(
    #         name=pcpp_cpu_cooler.name,
    #         price=float(pcpp_cpu_cooler.price.replace("$", "").replace("+", "").strip()),
    #         pcpp_url=pcpp_cpu_cooler.url,
    #         specs=pcpp_cpu_cooler.specs,
    #         image_url=cooler_image,
    #     )
    #     cpu_cooler.save()

    #     best_gpu = get_best_component("video card", component_budgets["gpu"], 50)
    #     gpu_image = best_gpu.image
    #     pcpp_gpu = pcpp.fetch_product(best_gpu.url)

    #     gpu = Component(
    #         name=pcpp_gpu.name,
    #         price=float(pcpp_gpu.price.replace("$", "").replace("+", "").strip()),
    #         pcpp_url=pcpp_gpu.url,
    #         specs=pcpp_gpu.specs,
    #         image_url=gpu_image,
    #     )
    #     gpu.save()

    #     best_motherboard = get_best_component("motherboard", component_budgets["motherboard"])
    #     mobo_image = best_motherboard.image
    #     pcpp_mobo = pcpp.fetch_product(best_motherboard.url)

    #     motherboard = Component(
    #         name=pcpp_mobo.name,
    #         price=float(pcpp_mobo.price.replace("$", "").replace("+", "").strip()),
    #         pcpp_url=pcpp_mobo.url,
    #         specs=pcpp_mobo.specs,
    #         image_url=mobo_image,
    #     )
    #     motherboard.save()

    #     best_ram = get_best_component("memory", component_budgets["ram"])
    #     ram_image = best_ram.image
    #     pcpp_ram = pcpp.fetch_product(best_ram.url)

    #     ram = Component(
    #         name=pcpp_ram.name,
    #         price=float(pcpp_ram.price.replace("$", "").replace("+", "").strip()),
    #         pcpp_url=pcpp_ram.url,
    #         specs=pcpp_ram.specs,
    #         image_url=ram_image,
    #     )
    #     ram.save()

    #     best_psu = get_best_component("power supply", component_budgets["psu"])
    #     psu_image = best_psu.image
    #     pcpp_psu = pcpp.fetch_product(best_psu.url)

    #     psu = Component(
    #         name=pcpp_psu.name,
    #         price=float(pcpp_psu.price.replace("$", "").replace("+", "").strip()),
    #         pcpp_url=pcpp_psu.url,
    #         specs=pcpp_psu.specs,
    #         image_url=psu_image,
    #     )
    #     psu.save()

    #     best_storage = get_best_component("ssd", component_budgets["storage"])
    #     storage_image = best_storage.image
    #     pcpp_storage = pcpp.fetch_product(best_storage.url)

    #     storage = Component(
    #         name=pcpp_storage.name,
    #         price=float(pcpp_storage.price.replace("$", "").replace("+", "").strip()),
    #         pcpp_url=pcpp_storage.url,
    #         specs=pcpp_storage.specs,
    #         image_url=storage_image,
    #     )
    #     storage.save()


    #     best_case = get_best_component("case", component_budgets["case"])
    #     case_image = best_case.image
    #     pcpp_case = pcpp.fetch_product(best_case.url)

    #     case = Component(
    #         name=pcpp_case.name,
    #         price=float(pcpp_case.price.replace("$", "").replace("+", "").strip()),
    #         pcpp_url=pcpp_case.url,
    #         specs=pcpp_case.specs,
    #         image_url=case_image,
    #     )
    #     case.save()

    #     computer = Computer(
    #         name="test computer",
    #         cpu=cpu,
    #         cpu_cooler=cpu_cooler,
    #         gpu=gpu,
    #         motherboard=motherboard,
    #         ram=ram,
    #         psu=psu,
    #         storage=storage,
    #         case=case,
    #     )

    #     computer.save()

    #     return computer
    
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
