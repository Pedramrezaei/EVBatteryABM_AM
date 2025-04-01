# EV Battery Recycling Model - Constants

# Simulation time range
START_YEAR = 2024
END_YEAR = 2100

# Initial agent counts
INITIAL_EV_OWNERS = 1000
INITIAL_BATTERY_MANUFACTURERS = 3
INITIAL_RECYCLING_COMPANIES = 1

# Recycling parameters
RECYCLING_EFFICIENCY_START = 0.6  # Initial recycling efficiency (60%)
RECYCLING_EFFICIENCY_GROWTH = 0.025  # Annual growth in recycling efficiency (2.5%)
OWNER_RECYCLING_PROBABILITY = 0.5  # Base probability that an owner recycles
MAX_RECYCLING_EFFICIENCY = 0.98  # Maximum possible recycling efficiency (98%)

# EV market growth rates
EV_GROWTH_RATES = {
    "2024-2030": 0.1,  # 10% average annual growth
    "2031-2035": 0.15,  # 15% average annual growth
    "2036-2050": 0.075,  # 7.5% average annual growth
}

# Battery specifications
LITHIUM_PER_BATTERY = 2.5  # kg of lithium per battery
COBALT_PER_BATTERY = 6.0  # kg of cobalt per battery
BATTERY_LIFESPAN_YEARS = 8  # average years until battery reaches 80% capacity

# Network influence parameters
NETWORK_INFLUENCE_ANNUAL_INCREASE = 0.01  # Annual increase in network influence
MAX_NETWORK_INFLUENCE = 0.5  # Maximum network influence cap

# Scenario definitions
SCENARIOS = [
    ("baseline", {}),
    ("no_recycling", {
        "owner_recycling_probability": 0.0,
        "recycling_efficiency_start": 0.0,
        "recycling_efficiency_growth": 0.0
    }),
    ("high_efficiency", {
        "recycling_efficiency_start": 0.8,
        "recycling_efficiency_growth": 0.04,
        "owner_recycling_probability": 0.8
    })
]

# Simulation parameters
MAX_SIMULATION_STEPS = 100  # Maximum steps to prevent infinite loops
PROGRESS_REPORT_INTERVAL = 5  # Report progress every 5 years 