# EV Battery Recycling Agent-Based Model

This Agent-Based Model (ABM) simulates the recycling of electric vehicle batteries and its effect on the demand for lithium and cobalt. The model addresses the research question: "How much can the demand for lithium and cobalt decrease if we recycle electric vehicle batteries?"

## Model Overview

The model simulates three types of agents:

1. **EV Owners**: These agents own electric vehicles and make decisions about whether to recycle or discard their batteries when they reach 80% capacity.

2. **Battery Manufacturers**: These agents produce new batteries and can use recycled materials in their production process.

3. **Recycling Companies**: These agents receive old batteries and extract lithium and cobalt for reuse.

The simulation tracks the flow of materials (lithium and cobalt in kilograms) through the system, measuring how recycling affects the demand for new materials over time.

## Key Parameters

- **EV Market Growth**: Growth rates vary by time period (8-12% for 2024-2030, 12-18% for 2030-2035, 5-10% for 2035-2050)
- **Recycling Efficiency**: Starts at a base level and increases annually by 2-3%
- **Owner Recycling Probability**: Likelihood that an EV owner chooses to recycle their battery
- **Battery Lifespan**: Years until a battery reaches 80% capacity
- **Network Effects**: Influence of other EV owners on recycling decisions
- **Battery Material Content**: Each battery contains approximately 2.5 kg of lithium and 6.0 kg of cobalt

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Model

### Interactive Visualization

To run the model with an interactive web interface:

```bash
python -m mesa runserver
```

This will start a local server at http://127.0.0.1:8521/ where you can adjust parameters and see real-time visualizations.

### Batch Analysis

To run multiple scenarios and generate comparison charts:

```bash
python run.py
```

This will run the model with different parameter sets and save the results as a figure named `recycling_analysis_results.png`.

## Files in this Project

- `model.py`: The main model class that integrates all agents and processes
- `ev_owner.py`: Implementation of the EV Owner agent
- `battery_manufacturer.py`: Implementation of the Battery Manufacturer agent
- `recycling_company.py`: Implementation of the Recycling Company agent
- `server.py`: Mesa server configuration for web visualization
- `run.py`: Script for batch running and analysis
- `constants.py`: Central configuration file for all model parameters
- `requirements.txt`: Required Python packages

## Expected Outputs

The model produces several key metrics:

1. **Total demand for lithium and cobalt** (in kg) over time
2. **Percentage reduction** in new material demand due to recycling
3. **Recycling efficiency** improvements over time
4. **Total EV growth** throughout the simulation period

## Limitations and Future Work

This model is a simplified representation and has several limitations:

- Does not account for policy interventions that might incentivize recycling
- Uses simplified estimates for battery material composition
- Does not model the economic costs of recycling vs. new material extraction
- Network effects are modeled in a simplified manner

Future work could enhance the model by incorporating:

- Geographic variations in recycling infrastructure
- Economic factors including material price fluctuations
- Technological innovations in battery chemistry
- Policy interventions and regulations
