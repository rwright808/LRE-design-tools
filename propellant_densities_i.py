import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
import numpy as np

def plot_density_vs_pressure(substance, temperature):
    pressures = np.linspace(1e5, 1e7, 100)  # Pressure range from 100 kPa to 1 MPa
    densities = [CP.PropsSI('D', 'P', p, 'T', temperature, substance) for p in pressures]

    plt.plot(pressures, densities, label=substance)

# Constants
temperature = 298.15  # Constant temperature in Kelvin

# Substances
substances = ['Dodecane', 'Methane', 'Propane', 'Ethanol']

# Plotting
plt.figure(figsize=(10, 6))
for substance in substances:
    plot_density_vs_pressure(substance, temperature)

# Set labels and title
plt.xlabel('Pressure (Pa)')
plt.ylabel('Density (kg/m^3)')
plt.title(f'Density vs Pressure at {temperature} K')
plt.legend()
plt.grid(True)
#plt.yscale('log')  # Use logarithmic scale for better visualization

# Show the plot
plt.show()
