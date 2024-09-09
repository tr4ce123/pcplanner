from decimal import Decimal

from django.forms import IntegerField
from ..models.computer import Computer, Component, FailedURL
from ..models.preferences import Preferences
from decimal import Decimal
from django.db.models import Q, F, Func, Value
from django.db.models.functions import Cast

class ComputerService:

    def create_computer(self, preferences: Preferences):
        """
        Creates a custom computer build based on user preferences.

        Parameters:
        - preferences: Preferences - User's preferences including budget, chipset, wifi requirement, and usage.

        Returns:
        - Computer: A Computer object containing the selected components.
        """
        total_budget = float(preferences.budget)
        chipset = preferences.chipset.lower() if preferences.chipset else None
        wifi = preferences.need_wifi
        usage = preferences.usage.lower() if preferences.usage else None

        # Distribution of the budget among components
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

        # Adjust motherboard budget if necessary
        component_budgets["motherboard"] = self._adjust_motherboard_budget(total_budget, component_budgets)

        try:
            # Retrieve the best components based on preferences and budget
            cpu = self._get_best_cpu("CPU", component_budgets["cpu"], chipset, usage)
            gpu = self._get_best_gpu("Video Card", component_budgets["gpu"])
            cpu_cooler = self._get_best_cpu_cooler("CPU Cooler", component_budgets["cpu_cooler"])
            motherboard = self._get_best_mobo("Motherboard", component_budgets["motherboard"], cpu, wifi)
            ram = self._get_best_ram("Memory", component_budgets["ram"])
            psu = self._get_best_component("Power Supply", component_budgets["psu"])
            storage = self._get_best_storage("Storage", component_budgets["storage"])
            case = self._get_best_component("Case", component_budgets["case"])
        except ValueError as e:
            raise ValueError(f"Component selection failed: {str(e)}")

        if None in [cpu, gpu, cpu_cooler, motherboard, ram, psu, storage, case]:
            raise ValueError("Not all components could be found within the budget")

        # Create and save the computer object with selected components
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

    def _adjust_motherboard_budget(self, total_budget: float, component_budgets: dict) -> float:
        """
        Adjusts the motherboard budget based on the total budget and component budget distribution.

        Parameters:
        - total_budget: float - The total budget for the build.
        - component_budgets: dict - The distribution of the budget among different components.

        Returns:
        - float: Adjusted motherboard budget.
        """
        motherboard_budget = component_budgets["motherboard"]

        # Cap the motherboard budget at $200 if the total budget is below $2000
        if total_budget < 2000:
            motherboard_budget = min(motherboard_budget, 200)

        # Redistribute surplus to GPU if motherboard budget exceeds $200
        if component_budgets["motherboard"] > 200:
            surplus = component_budgets["motherboard"] - 200
            component_budgets["gpu"] += surplus

        return motherboard_budget

    def _get_best_component(self, component_type: str, budget: float) -> Component:
        """
        General function to retrieve the component that is the closest in price to its percentage of the budget.

        Parameters:
        - component_type: str - The type of component (e.g., 'Power Supply', 'Case').
        - budget: float - The budget allocated for this component.

        Returns:
        - Component: The best component found within the specified budget.
        """
        queryset = Component.objects.filter(type=component_type, price__lte=budget)
        component = queryset.order_by('-price').first()
        if not component:
            raise ValueError(f"No {component_type} found within budget {budget}")
        return component

    def _get_best_cpu(self, component_type: str, budget: float, chipset: str, usage: str) -> Component:
        """
        Retrieves the best CPU that matches the user's usage and budget distribution.

        Parameters: 
        - component_type: str - The type of component, typically 'CPU'.
        - budget: float - The budget allocated for the CPU.
        - chipset: str - Specifies Intel or AMD chipset, defaults to Intel if not specified.
        - usage: str - Specifies whether the PC is intended for productivity or gaming.

        Returns:
        - Component: The best CPU component found within the specified budget and requirements.
        """
        queryset = Component.objects.filter(type=component_type, price__lte=budget)

        # Chipset Specifications
        if chipset == "intel" or chipset is None:
            if budget >= 800:
                queryset = queryset.filter(specs__contains={"Socket": ["LGA1700"]}).filter(name__contains="K")
            else:
                queryset = queryset.filter(specs__contains={"Socket": ["LGA1200"]})
        elif chipset == "amd":
            queryset = queryset.filter(specs__contains={"Socket": ["AM5"]})

        # Usage Specifications
        if usage == "productivity":
            component = queryset.order_by('-specs__Core Count', '-price').first()
        else:
            component = queryset.order_by('-price').first()

        if not component:
            raise ValueError(f"No {component_type} found within budget {budget} for chipset {chipset}")
        return component

    def _get_best_mobo(self, component_type: str, budget: float, cpu: Component, wifi: bool) -> Component:
        """
        Retrieves the best motherboard that is compatible with the selected CPU, fits within the budget, and meets additional requirements.

        Parameters:
        - component_type: str - The type of component, typically 'Motherboard'.
        - budget: float - The budget allocated for the motherboard.
        - cpu: Component - The selected CPU, used to determine socket compatibility.
        - wifi: bool - Whether the motherboard should include wireless internet capability.

        Returns:
        - Component: The best motherboard found within the specified budget and requirements.
        """
        queryset = Component.objects.filter(type=component_type, price__lte=budget)
        cpu_socket = cpu.specs.get("Socket")
        if not cpu_socket:
            raise ValueError(f"CPU specs do not contain 'Socket' key: {cpu.specs}")

        if budget > 900:
            queryset = queryset.filter(specs__contains={"Form Factor": ["ATX"]})

        queryset = queryset.filter(specs__contains={"Socket / CPU": cpu_socket})

        if budget >= 800:
            queryset = queryset.filter(specs__contains={"Memory Type": ["DDR5"]})
        else:
            queryset = queryset.filter(specs__contains={"Memory Type": ["DDR4"]})

        if wifi:
            queryset = queryset.filter(~Q(specs__contains={"Wireless Networking": "None"}))

        component = queryset.order_by('-price').first()
        if not component:
            raise ValueError(f"No {component_type} found within budget {budget} for CPU {cpu}")
        return component

    def _get_best_ram(self, component_type: str, budget: float) -> Component:
        """
        Retrieves the best RAM module that fits within the budget and matches the form factor and speed requirements.

        Parameters:
        - component_type: str - The type of component, typically 'Memory'.
        - budget: float - The budget allocated for the RAM.

        Returns:
        - Component: The best RAM component found within the specified budget and requirements.
        """
        queryset = Component.objects.filter(type=component_type, price__lte=budget)

        if budget > 900:
            queryset = queryset.filter(specs__contains={"Form Factor": ["288-pin DIMM (DDR5)"]})
        else:
            queryset = queryset.filter(specs__contains={"Form Factor": ["288-pin DIMM (DDR4)"]})

        queryset = queryset.filter(specs__contains={"Modules": ["2 x 8GB"]})

        component = queryset.order_by('-price').first()
        if not component:
            raise ValueError(f"No {component_type} found within budget {budget}")
        return component

    def _get_best_gpu(self, component_type: str, budget: float) -> Component:
        """
        Retrieves the best GPU based on memory, core clock speed, and price within the specified budget.

        Parameters:
        - component_type: str - The type of component, typically 'Video Card'.
        - budget: float - The budget allocated for the GPU.

        Returns:
        - Component: The best GPU component found within the specified budget and requirements.
        """
        budget = Decimal(budget)
        queryset = Component.objects.filter(type=component_type, price__lte=budget)

        if not queryset.exists():
            raise ValueError(f"No {component_type} found within budget {budget}")

        sorted_components = []
        for component in queryset:
            try:
                chipset = component.specs.get('Chipset', [])[0].lower()
                if 'geforce' in chipset:
                    core_clock_speed = component.specs.get('Core_Clock', ['0 MHz'])[0]
                    memory_size = component.specs.get('Memory', ['0 GB'])[0]
                    core_clock_value = int(core_clock_speed.replace(' MHz', ''))
                    memory_value = int(memory_size.replace(' GB', ''))
                    price = component.price  
                    sorted_components.append((memory_value, core_clock_value, price, component))
            except (IndexError, ValueError, TypeError):
                continue

        sorted_components.sort(reverse=True, key=lambda x: (x[0], x[1], x[2]))

        if not sorted_components:
            raise ValueError(f"No {component_type} found within budget {budget}")

        return sorted_components[0][3]

    def _get_best_cpu_cooler(self, component_type: str, budget: float) -> Component:
        """
        Retrieves the best CPU cooler that fits within the budget.

        Parameters:
        - component_type: str - The type of component, typically 'CPU Cooler'.
        - budget: float - The budget allocated for the CPU cooler.

        Returns:
        - Component: The best CPU cooler found within the specified budget.
        """
        queryset = Component.objects.filter(type=component_type, price__lte=budget)
        component = queryset.order_by('-price').first()
        if not component:
            raise ValueError(f"No {component_type} found within budget {budget}")
        return component

    def _get_best_storage(self, component_type: str, budget: float) -> Component:
        """
        Retrieves the best storage component (e.g., SSD) that fits within the budget and meets specific requirements.

        Parameters:
        - component_type: str - The type of component, typically 'Storage'.
        - budget: float - The budget allocated for the storage component.

        Returns:
        - Component: The best storage component found within the specified budget and requirements.
        """
        queryset = Component.objects.filter(type=component_type, price__lte=budget)
        queryset = queryset.filter(specs__contains={"NVME": ["Yes"]})
        component = queryset.order_by('-price').first()
        if not component:
            raise ValueError(f"No {component_type} found within budget {budget}")
        return component