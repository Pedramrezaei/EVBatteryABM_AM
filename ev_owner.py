import mesa
import random
from constants import (
    NETWORK_INFLUENCE_ANNUAL_INCREASE,
    MAX_NETWORK_INFLUENCE
)

# Import at the top to avoid circular imports
from recycling_company import RecyclingCompany
from battery_manufacturer import BatteryManufacturer

class EVOwner(mesa.Agent):
    """An agent representing an electric vehicle owner."""
    
    def __init__(self, unique_id, model, battery_age=0):
        super().__init__(unique_id, model)
        self.battery_age = battery_age  # Age of battery in years
        self.has_recycled = False  # Track if the battery has been recycled
        self.battery_replaced = False  # Track if battery has been replaced this step
        self.network_influence = 0  # Influence from other EV owners about recycling
    
    def decide_to_recycle(self):
        """Decide whether to recycle battery or discard it."""
        base_probability = self.model.owner_recycling_probability
        
        # Increase probability based on network influence
        adjusted_probability = min(0.95, base_probability + self.network_influence)
        
        # Make decision
        if random.random() < adjusted_probability:
            return True  # Recycle
        else:
            return False  # Discard
    
    def step(self):
        """Actions during each step (year)."""
        # Reset battery replacement tracking for this step
        self.battery_replaced = False
        
        # Age the battery by one year
        self.battery_age += 1
        
        # Update network influence
        self.update_network_influence()
        
        # Check if battery has reached end of life (80% capacity)
        if self.battery_age >= self.model.battery_lifespan and not self.has_recycled:
            # Decision to recycle or discard
            if self.decide_to_recycle():
                # Recycle the battery
                self.recycle_battery()
            else:
                # Discard the battery (materials lost)
                self.discard_battery()
                
            # Get a new battery either way
            self.replace_battery()
    
    def recycle_battery(self):
        """Send battery to recycling."""
        # Find a recycling company - use the stored list for better performance
        if self.model.recyclers:
            recycler = self.random.choice(self.model.recyclers)
            recycler.receive_battery()
            
        self.has_recycled = True
    
    def discard_battery(self):
        """Discard the battery (materials are lost)."""
        # No recycling occurs, materials are lost
        self.has_recycled = True  # Mark as handled
    
    def replace_battery(self):
        """Get a new battery."""
        # Find a battery manufacturer - use the stored list for better performance
        if self.model.manufacturers:
            manufacturer = self.random.choice(self.model.manufacturers)
            manufacturer.produce_battery()
            
        # Reset battery age
        self.battery_age = 0
        self.has_recycled = False
        self.battery_replaced = True
    
    def update_network_influence(self):
        """Update network influence based on neighbors."""
        # This simulates word-of-mouth and awareness campaigns
        # In a more complex model, this would use a network structure
        
        # For simplicity, we'll increase influence slightly each year
        # representing growing awareness about recycling
        self.network_influence += NETWORK_INFLUENCE_ANNUAL_INCREASE
        
        # Cap the influence
        self.network_influence = min(MAX_NETWORK_INFLUENCE, self.network_influence) 