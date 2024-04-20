import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
import numpy as np

def plot_density_vs_pressure(substance, temperatures, pressures):
    plt.figure(figsize=(10, 6))

    for temperature in temperatures:
        densities = [CP.PropsSI('D', 'P', p, 'T', temperature, substance) for p in pressures]
        label = f'{substance} at {temperature} K'
        plt.plot(pressures, densities, label=label)

    # Set labels and title
    plt.xlabel('Pressure (Pa)')
    plt.ylabel('Density (kg/m^3)')
    plt.title(f'Density vs Pressure for {substance}')
    plt.legend()
    plt.grid(True)
    # plt.yscale('log')  # Use logarithmic scale for better visualization

    # Show the plot
    plt.show()

# Constants
pressures = np.linspace(1e5, 2e6, 100)  # Pressure range from 100 kPa to 1 MPa
temperatures = [273.15, 283.15, 288.15, 293.15, 298.15]  # Example temperatures in Kelvin

# Single Substance
substance = 'Propane'

# Plotting
plot_density_vs_pressure(substance, temperatures, pressures)
