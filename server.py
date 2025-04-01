import mesa
from model import EVBatteryModel

def get_lithium_savings(model):
    """Calculate percent of lithium saved through recycling."""
    if model.calculate_lithium_demand() == 0:
        return 0
    
    recycled = model.recycled_lithium
    total_needed = model.recycled_lithium + model.new_lithium_required
    
    if total_needed == 0:
        return 0
    
    return (recycled / total_needed) * 100

def get_cobalt_savings(model):
    """Calculate percent of cobalt saved through recycling."""
    if model.calculate_cobalt_demand() == 0:
        return 0
    
    recycled = model.recycled_cobalt
    total_needed = model.recycled_cobalt + model.new_cobalt_required
    
    if total_needed == 0:
        return 0
    
    return (recycled / total_needed) * 100

model_params = {
    "initial_ev_owners": mesa.visualization.Slider(
        "Initial EV Owners", 1000, 100, 5000, 100,
        description="Initial number of electric vehicle owners"
    ),
    "initial_battery_manufacturers": mesa.visualization.Slider(
        "Battery Manufacturers", 10, 1, 50, 1,
        description="Number of battery manufacturing companies"
    ),
    "initial_recycling_companies": mesa.visualization.Slider(
        "Recycling Companies", 5, 1, 20, 1,
        description="Number of battery recycling companies"
    ),
    "recycling_efficiency_start": mesa.visualization.Slider(
        "Initial Recycling Efficiency", 0.6, 0.3, 0.9, 0.05,
        description="Starting efficiency of recycling processes (60% = 0.6)"
    ),
    "recycling_efficiency_growth": mesa.visualization.Slider(
        "Annual Recycling Efficiency Growth", 0.025, 0.01, 0.05, 0.005,
        description="Annual percentage improvement in recycling efficiency"
    ),
    "owner_recycling_probability": mesa.visualization.Slider(
        "Base Recycling Probability", 0.5, 0.1, 0.9, 0.1,
        description="Base probability that an EV owner chooses to recycle"
    ),
    "battery_lifespan_years": mesa.visualization.Slider(
        "Battery Lifespan (years)", 8, 5, 15, 1,
        description="Years until battery reaches 80% capacity"
    ),
    "start_year": 2024,
    "end_year": mesa.visualization.Slider(
        "End Year", 2050, 2030, 2070, 5,
        description="Year to end simulation"
    )
}

# Create charts for the visualization
lithium_demand_chart = mesa.visualization.ChartModule([
    {"Label": "New Lithium Required", "Color": "Red"},
    {"Label": "Recycled Lithium", "Color": "Green"}
])

cobalt_demand_chart = mesa.visualization.ChartModule([
    {"Label": "New Cobalt Required", "Color": "Blue"},
    {"Label": "Recycled Cobalt", "Color": "Purple"}
])

ev_growth_chart = mesa.visualization.ChartModule([
    {"Label": "Number of EVs", "Color": "Black"}
])

efficiency_chart = mesa.visualization.ChartModule([
    {"Label": "Recycling Efficiency", "Color": "Orange"}
])

# Create the server
server = mesa.visualization.ModularServer(
    EVBatteryModel,
    [lithium_demand_chart, cobalt_demand_chart, ev_growth_chart, efficiency_chart],
    "EV Battery Recycling Model",
    model_params
) 