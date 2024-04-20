from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel

import matplotlib
matplotlib.use('Qt5Agg')  # Use the TkAgg backend

import numpy as np
import matplotlib.pyplot as plt


def bar_to_psi(x):
    return x * 14.5038

###START USER INPUT

fuel_name = 'paraffin'
#C32H66 from RPA Paraffin Wax Composition
fuel_properties = f"""
fuel paraffin  C 32   H 66    wt%=100.00
h,KJ/Kgmol=-1860600     t(k)=298.15   rho,kg/m3={900}
"""
add_new_fuel(fuel_name, fuel_properties)

ox_name = 'N2O'

expratio = 12
OF_ratio = [2, 4, 6, 8, 10, 12]
chamber_pressures = [10, 20, 30, 40, 50, 60]

###END USER INPUT

# Create CEA object for the first graph (Flame Temp/mw vs. Chamber Pressure)
ceaObj = CEA_Obj(
    oxName=ox_name, fuelName=fuel_name, pressure_units='Bar', isp_units='sec', cstar_units='m/s',
    temperature_units='K', sonic_velocity_units='m/s', enthalpy_units='kJ/kg', density_units='kg/m^3',
    specific_heat_units='kJ/kg-K'
)

# Create subplots
fig, axs = plt.subplots(1, 3, figsize=(15, 6))

# First subplot: Flame Temp/mw vs. Chamber Pressure
axs[0].set_title('Flame Temp/mw vs Chamber Pressure')
axs[0].set_xlabel('Chamber Pressure (Bar)')
axs[0].set_ylabel('Flame Temp/mw ((mol K)/kg)')

axs[1].set_title('Flame Temp vs Chamber Pressure')
axs[1].set_xlabel('Chamber Pressure (Bar)')
axs[1].set_ylabel('Flame Temp (K)')

for j in OF_ratio:
    flame_temp_mw_ratio_arr = []
    flame_temp_arr = []
    p_cc_arr = []

    for k in chamber_pressures:
        i = ceaObj.get_IvacCstrTc_ChmMwGam(Pc=k, MR=j, eps=expratio)
        flame_temp_mw_ratio_arr.append(i[2] / i[3])
        flame_temp_arr.append(i[2])
        p_cc_arr.append(k)

    print(f"O/F Ratio: {j}, gamma = {i[4]}, gas const = {8134 / i[3]}, mw = {i[3]}")
    
    #graph OF vs flame temp / mw
    axs[0].plot(p_cc_arr, flame_temp_mw_ratio_arr, label=f'O/F={j}')
    #graph OF vs flame temp
    axs[1].plot(p_cc_arr, flame_temp_arr, label=f'O/F={j}')

axs[0].legend()
axs[0].grid(True)
axs[1].legend()
axs[1].grid(True)

# Second subplot: ISP vs. O/F Ratio at Different Chamber Pressures


axs[2].set_title('ISP vs O/F Ratio at Different Chamber Pressures')
axs[2].set_xlabel('O/F Ratio')
axs[2].set_ylabel('ISP (s)')

for Pc in chamber_pressures:
    ispObj = CEA_Obj(
        oxName=ox_name, fuelName=fuel_name, pressure_units='Bar', isp_units='sec', cstar_units='m/s',
        temperature_units='K', sonic_velocity_units='m/s', enthalpy_units='kJ/kg', density_units='kg/m^3',
        specific_heat_units='kJ/kg-K'
    )

    of_arr = []
    isp_arr = []

    isp_prev = 0
    max_isp = 0
    of_store = 0
    i = 0.55

    while i < 16:
        isp = ispObj.get_Isp(Pc=Pc, MR=i, eps=expratio, frozen=0, frozenAtThroat=0)
        of_arr.append(i)
        isp_arr.append(isp)
        if isp > isp_prev:
            max_isp = isp
            of_store = i
        i = i + 0.5
        isp_prev = isp

    print(f"For Pc={Pc} bar, Max ISP: {max_isp}, O/F Ratio: {of_store}")
    #graph OF vs max theoretical ISP
    axs[2].plot(of_arr, isp_arr, label=f'Pc={Pc} bar  [{bar_to_psi(Pc)} PSI]')

axs[2].legend()
axs[2].grid(True)

#show graphs, and TODO: print out stoichiometric O/F, O/F at highest flame temp/mw
plt.show()

#let user input desired O/F ratio
input_of = 0
while(input_of ==0):
    input_of = input("Pick and Enter O/F ratio: ")

#now graph chamber pressure vs m dot / A throat selected O/F ratio
    


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
    p_cc_arr.clear()
    #solve throat area
    Athroat = (np.pi/4)*((0.0254*throat_diam_current)**2)

    while(P_cc_current<=P_cc_max):
                #call cea object - solve cstar
        cstar = ceaObj.get_Cstar(P_cc_current, input_of)

        #solve mdot / A throat
        j = P_cc_current/cstar
        #add to arrays
        mdot_arr.append(((P_cc_current*1e5)/cstar)*Athroat)
        p_cc_arr.append(P_cc_current)

        P_cc_current+=P_cc_step
        #print(cstar)
    plt.plot(p_cc_arr, mdot_arr, label=f'throat_diam (in) {throat_diam_current}')
    P_cc_current=P_cc_min
    throat_diam_current+=throat_diam_step


plt.title(label=f'mdot vs Chamber Pressure for '+ ox_name + ' ' + fuel_name + f' at O/F Ratio {input_of}')
plt.xlabel('Chamber Pressure (Bar)')
plt.ylabel('mdot (kg/s)')
plt.legend()
plt.grid(True)
plt.show()



    

