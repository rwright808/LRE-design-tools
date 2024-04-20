from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel

import matplotlib
matplotlib.use('Qt5Agg')  # Use the TkAgg backend

import numpy as np
import matplotlib.pyplot as plt

fuel_name = 'Ethanol'
ox_name = 'N2O'

expratio = 12
OF_ratio = 4
m_dot = 2 
chamber_pressures = [10, 20, 30, 40, 50]

###END USER INPUT

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

throat_diam_min = 0.75 #in
throat_diam_max = 1.75 #in
throat_diam_step = 0.125 #in
throat_diam_current = throat_diam_min

while(throat_diam_current<=throat_diam_max):
    mdot_arr = []
    p_cc_arr = []
    #solve throat area
    Athroat = (np.pi/4)*((0.0254*throat_diam_current)**2)

    while(P_cc_current<=P_cc_max):
        #call cea object - solve cstar
        cstar = (Athroat*P_cc_current*1e5)/m_dot

        #add to arrays
        mdot_arr.append(cstar)
        p_cc_arr.append(P_cc_current)

        P_cc_current+=P_cc_step
        #print(cstar)
    plt.plot(p_cc_arr, mdot_arr, label=f'throat_diam (in) {throat_diam_current}')
    P_cc_current=P_cc_min
    throat_diam_current+=throat_diam_step

mdot_arr = []
p_cc_arr = []
while(P_cc_current<=P_cc_max):
    #call cea object - solve cstar
    cstar = ceaObj.get_Cstar(P_cc_current, OF_ratio)
    mdot_arr.append(cstar)
    p_cc_arr.append(P_cc_current)

    P_cc_current+=P_cc_step
    print(cstar)
plt.plot(p_cc_arr, mdot_arr, label=f'theoretical max')

plt.title(label=f'cstar vs Chamber Pressure for '+ ox_name + ' ' + fuel_name + f' at O/F Ratio {OF_ratio} and mdot {m_dot} kg/s')
plt.xlabel('Chamber Pressure (Bar)')
plt.ylabel('cstar')
plt.legend()
plt.grid(True)
plt.show()