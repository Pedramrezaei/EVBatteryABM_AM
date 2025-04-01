import mesa

class RecyclingCompany(mesa.Agent):
    """An agent representing a battery recycling company."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.batteries_received = 0
        self.lithium_recycled = 0
        self.cobalt_recycled = 0
    
    def receive_battery(self):
        """Process a battery that has been sent for recycling."""
        # Increment battery counter
        self.batteries_received += 1
        
        # Calculate amount of materials that can be recycled based on efficiency
        efficiency = self.model.recycling_efficiency
        lithium_recovered = self.model.lithium_per_battery * efficiency
        cobalt_recovered = self.model.cobalt_per_battery * efficiency
        
        # Update counters
        self.lithium_recycled += lithium_recovered
        self.cobalt_recycled += cobalt_recovered
        
        # Add to model's recycled materials pool
        self.model.recycled_lithium += lithium_recovered
        self.model.recycled_cobalt += cobalt_recovered
    
    def step(self):
        """Actions during each step (year)."""
        # Reset counters for the new year
        self.batteries_received = 0
        self.lithium_recycled = 0
        self.cobalt_recycled = 0 