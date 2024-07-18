from decimal import Decimal

from django.forms import IntegerField
from ..models.computer import Computer, Component, FailedURL
from ..models.preferences import Preferences
from decimal import Decimal
from django.db.models import Q, F, Func, Value
from django.db.models.functions import Cast

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

        motherboard_budget = component_budgets["motherboard"]

        # Cap the mobo budget at $200 if the budget is below $2000
        if total_budget < 2000:
            motherboard_budget = min(component_budgets["motherboard"], 200)

        if component_budgets["motherboard"] > 200:
            surplus = component_budgets["motherboard"] - 200
            component_budgets["gpu"] += surplus

        component_budgets["motherboard"] = motherboard_budget


        def get_best_component(component_type: str, budget: float) -> Component:
            queryset = Component.objects.filter(type=component_type, price__lte=budget)
            
            component = queryset.order_by('-price').first()
            if not component:
                raise ValueError(f"No {component_type} found within budget {budget}")
            return component
        
        def get_best_cpu(component_type: str, budget: float, chipset: str, usage: str) -> Component:
            queryset = Component.objects.filter(type=component_type, price__lte=budget)

            # Chipset Specifications
            if chipset == "intel" or chipset is None:
                # LGA1700 is most relevant
                if total_budget >= 800:
                    queryset = queryset.filter(specs__contains={"Socket": ["LGA1700"]})
                    queryset = queryset.filter(name__contains="K")
                else:
                    queryset = queryset.filter(specs__contains={"Socket": ["LGA1200"]})
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
            if total_budget > 900:
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
                # queryset = queryset.filter(specs__contains={"Speed": ["DDR5-6000"]})

            else:
                queryset = queryset.filter(specs__contains={"Form Factor": ["288-pin DIMM (DDR4)"]})
                # queryset = queryset.filter(specs__contains={"Speed": ["DDR4-3200"]})

            queryset = queryset.filter(specs__contains={"Modules": ["2 x 8GB"]})

            component = queryset.order_by('-price').first()
            if not component:
                raise ValueError(f"No {component_type} found within budget {budget}")
            return component
        
        def get_best_gpu(component_type: str, budget: float) -> Component:
            budget = Decimal(budget)

            queryset = Component.objects.filter(type=component_type, price__lte=budget)

            if not queryset.exists():
                raise ValueError(f"No {component_type} found within budget {budget}")
            

            sorted_components = []
            # for component in queryset:
            #     try:
            #         # Extract core clock speed, assume it's the first element in a list and ends with ' MHz'
            #         core_clock_speed = component.specs.get('Core_Clock', ['0 MHz'])[0]
            #         core_clock_value = int(core_clock_speed.replace(' MHz', ''))
            #         sorted_components.append((core_clock_value, component))
            #     except (IndexError, ValueError, TypeError):
            #         # Handle cases where Core_Clock is not properly formatted or missing
            #         continue

            for component in queryset:
                try:
                    chipset = component.specs.get('Chipset', [])
                    chipset = chipset[0].lower()
                    # Check if the chipset contains 'radeon' or 'geforce'
                    if 'geforce' in chipset:

                        # Extract core clock speed and memory, assuming they end with ' MHz' and ' GB' respectively
                        core_clock_speed = component.specs.get('Core_Clock', ['0 MHz'])[0]
                        memory_size = component.specs.get('Memory', ['0 GB'])[0]

                        # Convert the extracted values to integers
                        core_clock_value = int(core_clock_speed.replace(' MHz', ''))
                        memory_value = int(memory_size.replace(' GB', ''))
                        price = component.price  # Directly use the price of the component


                        # Append a tuple with memory and core clock values for sorting
                        sorted_components.append((memory_value, core_clock_value, price, component))
                    else:
                        continue
                except (IndexError, ValueError, TypeError):
                    # Handle cases where Core_Clock or Memory is not properly formatted or missing
                    continue

            # sorted_components.sort(reverse=True, key=lambda x: x[0])
            sorted_components.sort(reverse=True, key=lambda x: (x[0], x[1], x[2]))



            if not sorted_components:
                raise ValueError(f"No {component_type} found within budget {budget}")
            
            # return sorted_components[0][1]
            return sorted_components[0][3]



            # if not component:
            #     raise ValueError(f"No {component_type} found within budget {budget}")
            # return component

        def get_best_cpu_cooler(component_type: str, budget: float) -> Component:
            queryset = Component.objects.filter(type=component_type, price__lte=budget)

            component = queryset.order_by('-price').first()
            if not component:
                raise ValueError(f"No {component_type} found within budget {budget}")
            return component
        
        def get_best_storage(component_type: str, budget: float) -> Component:
            queryset = Component.objects.filter(type=component_type, price__lte=budget)

            queryset = queryset.filter(specs__contains={"NVME": ["Yes"]})

            component = queryset.order_by('-price').first()
            if not component:
                raise ValueError(f"No {component_type} found within budget {budget}")
            return component

        try:
            cpu = get_best_cpu("CPU", component_budgets["cpu"], chipset, usage)
            gpu = get_best_gpu("Video Card", component_budgets["gpu"])
            cpu_cooler = get_best_cpu_cooler("CPU Cooler", component_budgets["cpu_cooler"])
            motherboard = get_best_mobo("Motherboard", component_budgets["motherboard"], cpu, wifi)
            ram = get_best_ram("Memory", component_budgets["ram"])
            psu = get_best_component("Power Supply", component_budgets["psu"])
            storage = get_best_storage("Storage", component_budgets["storage"])
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
