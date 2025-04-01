import mesa
import numpy as np
import random
from constants import (
    INITIAL_EV_OWNERS,
    INITIAL_BATTERY_MANUFACTURERS,
    INITIAL_RECYCLING_COMPANIES,
    RECYCLING_EFFICIENCY_START,
    RECYCLING_EFFICIENCY_GROWTH,
    OWNER_RECYCLING_PROBABILITY,
    EV_GROWTH_RATES,
    LITHIUM_PER_BATTERY,
    COBALT_PER_BATTERY,
    BATTERY_LIFESPAN_YEARS,
    START_YEAR,
    END_YEAR,
    MAX_RECYCLING_EFFICIENCY
)

class EVBatteryModel(mesa.Model):
    """Model for simulating EV battery recycling and its effect on lithium and cobalt demand."""
    
    def __init__(
        self,
        initial_ev_owners=INITIAL_EV_OWNERS,
        initial_battery_manufacturers=INITIAL_BATTERY_MANUFACTURERS,
        initial_recycling_companies=INITIAL_RECYCLING_COMPANIES,
        recycling_efficiency_start=RECYCLING_EFFICIENCY_START,
        recycling_efficiency_growth=RECYCLING_EFFICIENCY_GROWTH,
        owner_recycling_probability=OWNER_RECYCLING_PROBABILITY,
        ev_growth_rates=EV_GROWTH_RATES,
        lithium_per_battery=LITHIUM_PER_BATTERY,
        cobalt_per_battery=COBALT_PER_BATTERY,
        battery_lifespan_years=BATTERY_LIFESPAN_YEARS,
        start_year=START_YEAR,
        end_year=END_YEAR
    ):
        super().__init__()
        self.num_ev_owners = initial_ev_owners
        self.num_battery_manufacturers = initial_battery_manufacturers
        self.num_recycling_companies = initial_recycling_companies
        self.recycling_efficiency = recycling_efficiency_start
        self.recycling_efficiency_growth = recycling_efficiency_growth
        self.owner_recycling_probability = owner_recycling_probability
        self.ev_growth_rates = ev_growth_rates
        self.lithium_per_battery = lithium_per_battery
        self.cobalt_per_battery = cobalt_per_battery
        self.battery_lifespan = battery_lifespan_years
        
        # Time tracking
        self.start_year = start_year
        self.end_year = end_year
        self.current_year = start_year
        self.schedule = mesa.time.RandomActivation(self)
        
        # Set running flag explicitly
        self.running = True
        
        # Track next unique ID
        self.next_id = 0
        
        # Data collection
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Year": lambda m: m.current_year,
                "Number of EVs": lambda m: m.num_ev_owners,
                "Recycling Efficiency": lambda m: m.recycling_efficiency,
                "Total Lithium Demand": lambda m: m.calculate_lithium_demand(),
                "Total Cobalt Demand": lambda m: m.calculate_cobalt_demand(),
                "Recycled Lithium": lambda m: m.recycled_lithium,
                "Recycled Cobalt": lambda m: m.recycled_cobalt,
                "New Lithium Required": lambda m: m.new_lithium_required,
                "New Cobalt Required": lambda m: m.new_cobalt_required,
            }
        )
        
        # Track materials
        self.recycled_lithium = 0
        self.recycled_cobalt = 0 
        self.new_lithium_required = 0
        self.new_cobalt_required = 0
        
        # Store references to agent types for faster lookup
        self.ev_owners = []
        self.manufacturers = []
        self.recyclers = []
        
        # Create agents
        self.create_agents()
        
        # Initial data collection
        self.datacollector.collect(self)
    
    def get_next_id(self):
        """Get the next unique ID and increment counter."""
        current_id = self.next_id
        self.next_id += 1
        return current_id
    
    def create_agents(self):
        """Create initial population of agents."""
        from ev_owner import EVOwner
        from battery_manufacturer import BatteryManufacturer
        from recycling_company import RecyclingCompany
        
        # Create EV owners
        for i in range(self.num_ev_owners):
            battery_age = random.randint(0, self.battery_lifespan)  # Random initial battery age
            ev_owner = EVOwner(self.get_next_id(), self, battery_age)
            self.schedule.add(ev_owner)
            self.ev_owners.append(ev_owner)
            
        # Create battery manufacturers
        for i in range(self.num_battery_manufacturers):
            manufacturer = BatteryManufacturer(self.get_next_id(), self)
            self.schedule.add(manufacturer)
            self.manufacturers.append(manufacturer)
            
        # Create recycling companies
        for i in range(self.num_recycling_companies):
            recycler = RecyclingCompany(self.get_next_id(), self)
            self.schedule.add(recycler)
            self.recyclers.append(recycler)
    
    def get_current_growth_rate(self):
        """Return the appropriate growth rate based on current year."""
        if self.current_year <= 2030:
            return self.ev_growth_rates["2024-2030"]
        elif self.current_year <= 2035:
            return self.ev_growth_rates["2031-2035"]
        else:
            return self.ev_growth_rates["2036-2050"]
    
    def step(self):
        """Advance the model by one step (one year)."""
        # Reset tracking variables for this step
        self.new_lithium_required = 0
        self.new_cobalt_required = 0
        
        # Step all agents
        self.schedule.step()
        
        # Update recycling efficiency
        self.recycling_efficiency = min(MAX_RECYCLING_EFFICIENCY, self.recycling_efficiency * (1 + self.recycling_efficiency_growth))
        
        # Grow EV market
        growth_rate = self.get_current_growth_rate()
        new_evs = int(self.num_ev_owners * growth_rate)
        
        # Add new EV owners more efficiently
        from ev_owner import EVOwner
        for i in range(new_evs):
            ev_owner = EVOwner(self.get_next_id(), self, 0)  # New cars with new batteries
            self.schedule.add(ev_owner)
            self.ev_owners.append(ev_owner)
        
        self.num_ev_owners += new_evs
        
        # Advance year
        self.current_year += 1
        
        # Collect data
        self.datacollector.collect(self)
        
        # Check if simulation should end
        if self.current_year > self.end_year:
            self.running = False
    
    def calculate_lithium_demand(self):
        """Calculate the total lithium demand for the current year."""
        return self.new_lithium_required
    
    def calculate_cobalt_demand(self):
        """Calculate the total cobalt demand for the current year."""
        return self.new_cobalt_required 