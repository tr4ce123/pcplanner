from ..models.computer import Computer, Component, FailedURL
from ..models.preferences import Preferences
from django.db.models import Q

class ComputerService:
    def create_computer(self, preferences: Preferences):
        total_budget = float(preferences.budget)

        chipset = wifi = usage = None

        if preferences.chipset and preferences.need_wifi and preferences.usage:
            chipset = preferences.chipset.lower()
            wifi = preferences.need_wifi
            usage = preferences.usage.lower()

        budget_distribution = {
            "cpu": 0.20,
            "cpu_cooler": 0.05,
            "gpu": 0.40,
            "motherboard": 0.15,
            "ram": 0.05,
            "psu": 0.05,
            "storage": 0.075,
            "case": 0.075,
        }

        component_budgets = {key: total_budget * value for key, value in budget_distribution.items()}

        def get_best_component(component_type: str, budget: float) -> Component:
            queryset = Component.objects.filter(type=component_type, price__lte=budget)
            
            component = queryset.order_by('-price').first()
            if not component:
                raise ValueError(f"No {component_type} found within budget {budget}")
            return component
        
        def get_best_cpu(component_type: str, budget: float, chipset: str, usage: str) -> Component:
            queryset = Component.objects.filter(type=component_type, price__lte=budget)

            # Chipset Specifications
            if chipset == "intel" or chipset == "" or chipset is None:
                # LGA1700 is most relevant
                queryset = queryset.filter(specs__contains={"Socket": ["LGA1700"]})
                queryset = queryset.filter(name__contains="K")
            elif chipset == "amd":
                # AM5 is most relevant
                queryset = queryset.filter(specs__contains={"Socket": ["AM5"]})
            # elif chipset == "amd" and budget < 1000:
            #     # AM4 is most relevant
            #     queryset = queryset.filter(specs__contains={"Socket": ["AM4"]})

            # Usage Specifications
            
            if usage == "productivity":
                component = queryset.order_by('-specs__Core Count', '-price')
            
            component = queryset.order_by('-price').first()


            if not component:
                raise ValueError(f"No {component_type} found within budget {budget} for chipset {chipset}")
            return component


        def get_best_mobo(component_type: str, budget: float, cpu: Component, wifi: bool) -> Component:
            queryset = Component.objects.filter(type=component_type, price__lte=budget)

            cpu_socket = cpu.specs.get("Socket")
            if not cpu_socket:
                raise ValueError(f"CPU specs do not contain 'Socket' key: {cpu.specs}")
            
            # ATX Mobos if enough budget
            if total_budget > 800:
                queryset = queryset.filter(specs__contains={"Form Factor": ["ATX"]})
            
            # Return a mobo that has the same socket as the CPU
            queryset = queryset.filter(specs__contains={"Socket / CPU": cpu_socket})

            # Return a mobo that supports DDR5
            if total_budget >= 800:
                queryset = queryset.filter(specs__contains={"Memory Type": ["DDR5"]})
            else:
                queryset = queryset.filter(specs__contains={"Memory Type": ["DDR4"]}) 

            # Return a mobo with wireless internet if needed
            if wifi or wifi is None:
                queryset = queryset.filter(~Q(specs__contains={"Wireless Networking": "None"}))

            component = queryset.order_by('-price').first()

            if not component:
                raise ValueError(f"No {component_type} found within budget {budget} for CPU {cpu}")
            return component
        
        def get_best_ram(component_type: str, budget: float) -> Component:
            queryset = Component.objects.filter(type=component_type, price__lte=budget)

            if total_budget > 900:
                queryset = queryset.filter(specs__contains={"Form Factor": ["288-pin DIMM (DDR5)"]})
            else:
                queryset = queryset.filter(specs__contains={"Form Factor": ["288-pin DIMM (DDR4)"]})

            queryset = queryset.filter(specs__contains={"Modules": ["2 x 8GB"]})

            component = queryset.order_by('-price').first()
            if not component:
                raise ValueError(f"No {component_type} found within budget {budget}")
            return component

        try:
            cpu = get_best_cpu("CPU", component_budgets["cpu"], chipset, usage)
            gpu = get_best_component("Video Card", component_budgets["gpu"])
            cpu_cooler = get_best_component("CPU Cooler", component_budgets["cpu_cooler"])
            motherboard = get_best_mobo("Motherboard", component_budgets["motherboard"], cpu, wifi)
            ram = get_best_ram("Memory", component_budgets["ram"])
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
