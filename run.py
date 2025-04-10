import mesa
import pandas as pd
import matplotlib.pyplot as plt
from model import EVBatteryModel
import time
from constants import (
    MAX_SIMULATION_STEPS,
    PROGRESS_REPORT_INTERVAL,
    SCENARIOS
)

def run_model(params=None, verbose=True, debug_efficiency=False):
    """Run a single instance of the model with given parameters."""
    if params is None:
        params = {}
    
    # Create model with default or specified parameters
    model = EVBatteryModel(**params)
    
    # Set a maximum number of steps to prevent infinite loops
    max_steps = MAX_SIMULATION_STEPS  # Should be enough for most simulations (2024-2124)
    step_count = 0
    
    # Debug initial efficiency value
    if debug_efficiency and verbose:
        print(f"Initial recycling efficiency: {model.recycling_efficiency:.4f}")
    
    # Run until the end year or max steps reached
    start_time = time.time()
    if verbose:
        print(f"Starting model run from year {model.current_year} to {model.end_year}")
    
    while model.running and step_count < max_steps:
        if verbose and step_count % PROGRESS_REPORT_INTERVAL == 0:  # Report progress every 5 years
            print(f"  - Simulating year {model.current_year}...")
            
        # Debug efficiency growth
        if debug_efficiency and step_count < 10 and verbose:
            old_efficiency = model.recycling_efficiency
            
        model.step()
        step_count += 1
        
        # Debug efficiency after step
        if debug_efficiency and step_count < 10 and verbose:
            print(f"    Year {model.current_year-1}->{model.current_year}: Efficiency {old_efficiency:.4f} -> {model.recycling_efficiency:.4f} (change: +{(model.recycling_efficiency - old_efficiency):.4f})")
    
    end_time = time.time()
    
    if step_count >= max_steps:
        print(f"WARNING: Model reached maximum step count ({max_steps}) - may have been an infinite loop")
    
    if verbose:
        print(f"Model run completed in {end_time - start_time:.2f} seconds ({step_count} steps)")
    
    # Get the DataCollector results
    results = model.datacollector.get_model_vars_dataframe()
    return results

def run_multiple_scenarios():
    """Run multiple scenarios with different parameters."""
    results = {}
    for name, params in SCENARIOS:
        print(f"Running {name} scenario...")
        # Use debug_efficiency=True for baseline scenario only
        results[name] = run_model(params, debug_efficiency=(name == "baseline"))
    
    return results

def analyze_results(results):
    """Analyze and visualize results from different scenarios."""
    print("Creating visualization plots...")
    try:
        # Create plots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Lithium demand comparison
        print("  - Plotting lithium demand comparison...")
        ax1 = axes[0, 0]
        results["baseline"]["New Lithium Required"].plot(ax=ax1, label="Baseline")
        results["no_recycling"]["New Lithium Required"].plot(ax=ax1, label="No Recycling")
        results["high_efficiency"]["New Lithium Required"].plot(ax=ax1, label="High Efficiency")
        ax1.set_title("New Lithium Demand Over Time")
        ax1.set_xlabel("Time Step (Years)")
        ax1.set_ylabel("Lithium (kg)")
        ax1.legend()
        
        # Plot 2: Cobalt demand comparison
        print("  - Plotting cobalt demand comparison...")
        ax2 = axes[0, 1]
        results["baseline"]["New Cobalt Required"].plot(ax=ax2, label="Baseline")
        results["no_recycling"]["New Cobalt Required"].plot(ax=ax2, label="No Recycling")
        results["high_efficiency"]["New Cobalt Required"].plot(ax=ax2, label="High Efficiency")
        ax2.set_title("New Cobalt Demand Over Time")
        ax2.set_xlabel("Time Step (Years)")
        ax2.set_ylabel("Cobalt (kg)")
        ax2.legend()
        
        # Plot 3: Recycled materials in baseline
        print("  - Plotting recycled materials...")
        ax3 = axes[1, 0]
        results["baseline"]["Recycled Lithium"].plot(ax=ax3, label="Recycled Lithium")
        results["baseline"]["Recycled Cobalt"].plot(ax=ax3, label="Recycled Cobalt")
        ax3.set_title("Recycled Materials (Baseline Scenario)")
        ax3.set_xlabel("Time Step (Years)")
        ax3.set_ylabel("Material (kg)")
        ax3.legend()
        
        # Plot 4: Recycling Efficiency
        print("  - Plotting recycling efficiency...")
        ax4 = axes[1, 1]
        results["baseline"]["Recycling Efficiency"].plot(ax=ax4, label="Baseline")
        results["high_efficiency"]["Recycling Efficiency"].plot(ax=ax4, label="High Efficiency")
        ax4.set_title("Recycling Efficiency Over Time")
        ax4.set_xlabel("Time Step (Years)")
        ax4.set_ylabel("Efficiency (%)")
        ax4.legend()
        
        plt.tight_layout()
        print("Saving visualization to recycling_analysis_results.png...")
        plt.savefig("recycling_analysis_results.png")
        
        # Don't use plt.show() in non-interactive environments, it can block execution
        # Only try to show the plot if in an interactive environment
        import os
        if os.environ.get('DISPLAY') or os.name == 'nt':
            plt.close()  # Close the plot to prevent memory leaks
        
        print("Visualization completed and saved.")
    except Exception as e:
        print(f"Error during visualization: {e}")
        print("Continuing with numerical analysis...")
    
    # Calculate percentage reduction in demand due to recycling
    print("Calculating reduction percentages...")
    try:
        baseline = results["baseline"]
        no_recycling = results["no_recycling"]
        
        final_year = baseline.index[-1]
        print(f"Final year of simulation: {final_year}")
        
        lithium_baseline = baseline.loc[final_year, "New Lithium Required"]
        lithium_no_recycling = no_recycling.loc[final_year, "New Lithium Required"]
        lithium_reduction = (1 - (lithium_baseline / lithium_no_recycling)) * 100
        
        cobalt_baseline = baseline.loc[final_year, "New Cobalt Required"]
        cobalt_no_recycling = no_recycling.loc[final_year, "New Cobalt Required"]
        cobalt_reduction = (1 - (cobalt_baseline / cobalt_no_recycling)) * 100
        
        print(f"By {final_year}, recycling reduces lithium demand by {lithium_reduction:.2f}%")
        print(f"By {final_year}, recycling reduces cobalt demand by {cobalt_reduction:.2f}%")
        
        # Add absolute values for clarity
        print(f"Lithium demand with recycling: {lithium_baseline:.2f} kg")
        print(f"Lithium demand without recycling: {lithium_no_recycling:.2f} kg")
        print(f"Cobalt demand with recycling: {cobalt_baseline:.2f} kg")
        print(f"Cobalt demand without recycling: {cobalt_no_recycling:.2f} kg")
        
        return {
            "lithium_reduction": lithium_reduction,
            "cobalt_reduction": cobalt_reduction
        }
    except Exception as e:
        print(f"Error during calculation: {e}")
        # Return default values if calculation fails
        return {
            "lithium_reduction": 0,
            "cobalt_reduction": 0
        }

if __name__ == "__main__":
    # Run multiple scenarios
    print("Running model scenarios...")
    try:
        # Run with a smaller end year for faster testing if needed
        # Uncomment the line below to use a shorter simulation period
        # EVBatteryModel.end_year = 2030  # This will make the simulation run much faster
        
        scenario_results = run_multiple_scenarios()
        
        # Analyze the results
        print("Analyzing results...")
        reduction_percentages = analyze_results(scenario_results)
        
        # Print a summary
        print("\nSummary of Findings:")
        print(f"- With the baseline recycling scenario, lithium demand decreased by {reduction_percentages['lithium_reduction']:.2f}%")
        print(f"- With the baseline recycling scenario, cobalt demand decreased by {reduction_percentages['cobalt_reduction']:.2f}%")
        print("- See the generated figure for detailed comparisons between scenarios.")
    except Exception as e:
        print(f"An error occurred during model execution: {e}") 