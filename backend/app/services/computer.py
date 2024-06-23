from ..models.computer import Computer, Component, FailedURL
from ..models.preferences import Preferences

class ComputerService:
    def create_computer(self, preferences: Preferences):
        total_budget = float(preferences.budget)
        chipset = preferences.chipset.lower()

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

        def get_best_component(component_type: str, budget: float, chipset: str = None) -> Component:
            queryset = Component.objects.filter(type=component_type, price__lte=budget)
            if component_type == "CPU" and chipset is not None:
                queryset = queryset.filter(specs__Manufacturer__icontains=chipset)
            component = queryset.order_by('-price').first()
            if not component:
                raise ValueError(f"No {component_type} found within budget {budget} for chipset {chipset}")
            return component

        try:
            cpu = get_best_component("CPU", component_budgets["cpu"], chipset)
            gpu = get_best_component("Video Card", component_budgets["gpu"])
            cpu_cooler = get_best_component("CPU Cooler", component_budgets["cpu_cooler"])
            motherboard = get_best_component("Motherboard", component_budgets["motherboard"])
            ram = get_best_component("Memory", component_budgets["ram"])
            psu = get_best_component("Power Supply", component_budgets["psu"])
            storage = get_best_component("Storage", component_budgets["storage"])
            case = get_best_component("Case", component_budgets["case"])
        except ValueError as e:
            raise ValueError(f"Component selection failed: {str(e)}")

        if None in [cpu, gpu, cpu_cooler, motherboard, ram, psu, storage, case]:
            raise ValueError("Not all components could be found within the budget")

        computer = Computer(
            name="Custom Build",
            cpu=cpu,
            gpu=gpu,
            cpu_cooler=cpu_cooler,
            motherboard=motherboard,
            ram=ram,
            psu=psu,
            storage=storage,
            case=case,
        )

        computer.save()
        return computer
