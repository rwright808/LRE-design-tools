from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel

import matplotlib
matplotlib.use('Qt5Agg')  # Use the TkAgg backend

import numpy as np
import matplotlib.pyplot as plt


###want to graph chamber pressure with respect to flame temperature

#input propellants

#fuel_name = 'paraffin'
#fuel_properties = f"""fuel paraffin  C 32   H 66    wt%=100.00
#h,KJ/Kgmol=-1860600     t(k)=298.15   rho,kg/m3={900}
#"""

#add_new_fuel(fuel_name, fuel_properties)

fuel_name = 'Ethanol'
ox_name = 'N2O'

OF_ratio = 4

expratios = [4,5,6,7,8]
chamber_pressures = [10, 20, 30, 40, 50]

# Create CEA object for the first graph (Flame Temp/mw vs. Chamber Pressure)
ceaObj = CEA_Obj(
    oxName=ox_name, fuelName=fuel_name, pressure_units='Bar', isp_units='sec', cstar_units='m/s',
    temperature_units='K', sonic_velocity_units='m/s', enthalpy_units='kJ/kg', density_units='kg/m^3',
    specific_heat_units='kJ/kg-K'
)

P_cc_min = chamber_pressures[0] #Bar
P_cc_max = chamber_pressures[-1] #Bar
P_cc_step = 2 #Bar
P_cc_current = P_cc_min

#loop for different expansion ratios
for expratio in expratios:

    #create graph arrays
    exit_vel_arr = []
    p_cc_arr = []

    #loop for different pressures
    while(P_cc_current <= P_cc_max):
        cea=ceaObj.get_IvacCstrTc_ChmMwGam(P_cc_current,OF_ratio,expratio)
        current_exit_vel = np.sqrt( ( (2*cea[4]*8134/cea[3])/(cea[4]-1) )*(cea[2]/cea[3])*(1-ceaObj.get_PcOvPe(P_cc_current,OF_ratio,expratio,0)**-1)**((cea[4]-1)/cea[4]) )
        exit_vel_arr.append(current_exit_vel)
        p_cc_arr.append(P_cc_current)
        P_cc_current+=P_cc_step;

    P_cc_current=P_cc_min
    plt.plot(p_cc_arr, exit_vel_arr, label=f'expratio {expratio}')

plt.title(label=f'Exit Velocity vs Chamber Pressure for '+ ox_name + ' ' + fuel_name)
plt.xlabel('Chamber Pressure (Bar)')
plt.ylabel('Exit Velocity (m/s)')
plt.legend()
plt.grid(True)
plt.show()
