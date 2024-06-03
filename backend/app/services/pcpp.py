import os, requests
from dotenv import load_dotenv
from decimal import Decimal
from pypartpicker import Scraper, Part, Product
from ..models.preferences import Preferences
from ..models.computer import Computer, Component

load_dotenv()
scraperAPI = os.environ["SCRAPER_API_KEY"]


def scraperapi_response_retriever(url, **kwargs):
    scraperapi_url = f"http://api.scraperapi.com/?api_key={scraperAPI}&url={url}"
    response = requests.get(scraperapi_url, **kwargs)
    response.raise_for_status()
    return response


pcpp = Scraper(response_retriever=scraperapi_response_retriever)


class ScraperService:
    def test_computer(self, preferences: Preferences):
        
        total_budget = float(preferences.budget)

        # TODO: Optimize budget distribution and tune to different preferences such as gaming, streaming, workstation, etc.
        budget_distribution = {
            "cpu": 0.25,
            "cpu_cooler": 0.05,
            "gpu": 0.35,
            "motherboard": 0.15,
            "ram": 0.05,
            "psu": 0.05,
            "storage": 0.075,
            "case": 0.075,
        }

        component_budgets = {key: total_budget * value for key, value in budget_distribution.items()}

        def get_best_component(part_name: str, budget, additional_budget=0) -> Part:
            parts = pcpp.part_search(part_name, limit = 20)
            best_part = None
            max_price = 0
            for part in parts:
                if part.price and part.url:
                    price = float(part.price.replace("$", "").replace("+", "").strip())
                    if price <= budget + additional_budget and price > max_price:
                        max_price = price
                        best_part = part
            return best_part


        best_cpu = get_best_component("processor", component_budgets["cpu"], 20)
        cpu_image = best_cpu.image
        pcpp_cpu = pcpp.fetch_product(best_cpu.url)

        cpu = Component(
            name=pcpp_cpu.name,
            price=float(pcpp_cpu.price.replace("$", "").replace("+", "").strip()),
            pcpp_url=pcpp_cpu.url,
            specs=pcpp_cpu.specs,
            image_url=cpu_image,
        )
        cpu.save()

        best_cpu_cooler = get_best_component("cpu cooler", component_budgets["cpu_cooler"], 10)
        cooler_image = best_cpu_cooler.image
        pcpp_cpu_cooler = pcpp.fetch_product(best_cpu_cooler.url)

        cpu_cooler = Component(
            name=pcpp_cpu_cooler.name,
            price=float(pcpp_cpu_cooler.price.replace("$", "").replace("+", "").strip()),
            pcpp_url=pcpp_cpu_cooler.url,
            specs=pcpp_cpu_cooler.specs,
            image_url=cooler_image,
        )
        cpu_cooler.save()

        best_gpu = get_best_component("video card", component_budgets["gpu"], 50)
        gpu_image = best_gpu.image
        pcpp_gpu = pcpp.fetch_product(best_gpu.url)

        gpu = Component(
            name=pcpp_gpu.name,
            price=float(pcpp_gpu.price.replace("$", "").replace("+", "").strip()),
            pcpp_url=pcpp_gpu.url,
            specs=pcpp_gpu.specs,
            image_url=gpu_image,
        )
        gpu.save()

        best_motherboard = get_best_component("motherboard", component_budgets["motherboard"])
        mobo_image = best_motherboard.image
        pcpp_mobo = pcpp.fetch_product(best_motherboard.url)

        motherboard = Component(
            name=pcpp_mobo.name,
            price=float(pcpp_mobo.price.replace("$", "").replace("+", "").strip()),
            pcpp_url=pcpp_mobo.url,
            specs=pcpp_mobo.specs,
            image_url=mobo_image,
        )
        motherboard.save()

        best_ram = get_best_component("memory", component_budgets["ram"])
        ram_image = best_ram.image
        pcpp_ram = pcpp.fetch_product(best_ram.url)

        ram = Component(
            name=pcpp_ram.name,
            price=float(pcpp_ram.price.replace("$", "").replace("+", "").strip()),
            pcpp_url=pcpp_ram.url,
            specs=pcpp_ram.specs,
            image_url=ram_image,
        )
        ram.save()

        best_psu = get_best_component("power supply", component_budgets["psu"])
        psu_image = best_psu.image
        pcpp_psu = pcpp.fetch_product(best_psu.url)

        psu = Component(
            name=pcpp_psu.name,
            price=float(pcpp_psu.price.replace("$", "").replace("+", "").strip()),
            pcpp_url=pcpp_psu.url,
            specs=pcpp_psu.specs,
            image_url=psu_image,
        )
        psu.save()

        best_storage = get_best_component("ssd", component_budgets["storage"])
        storage_image = best_storage.image
        pcpp_storage = pcpp.fetch_product(best_storage.url)

        storage = Component(
            name=pcpp_storage.name,
            price=float(pcpp_storage.price.replace("$", "").replace("+", "").strip()),
            pcpp_url=pcpp_storage.url,
            specs=pcpp_storage.specs,
            image_url=storage_image,
        )
        storage.save()


        best_case = get_best_component("case", component_budgets["case"])
        case_image = best_case.image
        pcpp_case = pcpp.fetch_product(best_case.url)

        case = Component(
            name=pcpp_case.name,
            price=float(pcpp_case.price.replace("$", "").replace("+", "").strip()),
            pcpp_url=pcpp_case.url,
            specs=pcpp_case.specs,
            image_url=case_image,
        )
        case.save()

        computer = Computer(
            name="test computer",
            cpu=cpu,
            cpu_cooler=cpu_cooler,
            gpu=gpu,
            motherboard=motherboard,
            ram=ram,
            psu=psu,
            storage=storage,
            case=case,
        )

        computer.save()

        return computer
