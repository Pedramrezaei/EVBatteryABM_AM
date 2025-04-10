import mesa

class BatteryManufacturer(mesa.Agent):
    """An agent representing a battery manufacturer."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.batteries_produced = 0
        self.recycled_materials_used = 0
        
    def produce_battery(self):
        """Produce a new battery."""
        # Increment batteries produced count
        self.batteries_produced += 1
        
        # Check availability of recycled materials
        available_recycled_lithium = self.model.recycled_lithium
        available_recycled_cobalt = self.model.recycled_cobalt
        
        # Calculate how much material is needed
        lithium_needed = self.model.lithium_per_battery
        cobalt_needed = self.model.cobalt_per_battery
        
        # Use recycled materials first, then virgin materials
        recycled_lithium_used = min(available_recycled_lithium, lithium_needed)
        recycled_cobalt_used = min(available_recycled_cobalt, cobalt_needed)
        
        # Update model's recycled materials tracking (current available pool)
        self.model.recycled_lithium -= recycled_lithium_used
        self.model.recycled_cobalt -= recycled_cobalt_used
        
        # Update model's cumulative tracking of recycled materials used
        self.model.total_lithium_used_from_recycled += recycled_lithium_used
        self.model.total_cobalt_used_from_recycled += recycled_cobalt_used
        
        # Calculate new materials needed
        new_lithium_needed = lithium_needed - recycled_lithium_used
        new_cobalt_needed = cobalt_needed - recycled_cobalt_used
        
        # Update model's new materials tracking
        self.model.new_lithium_required += new_lithium_needed
        self.model.new_cobalt_required += new_cobalt_needed
        
        # Track recycled materials used
        self.recycled_materials_used += (recycled_lithium_used + recycled_cobalt_used)
    
    def step(self):
        """Actions during each step (year)."""
        # Reset counters for the new year
        self.batteries_produced = 0
        self.recycled_materials_used = 0 