from service.loader import LoadFiles
from service.save import Save
from core.simulation import Simulate
from service.loader import LoadFiles
from interface.flight_simulation import FlightSimulation
from interface.graphics import Interface
from interface.flight_simulation import FlightSimulation




data_ac = LoadFiles._read_jsonc("configs/aircrafts/aircraft.jsonc")
ac_params = LoadFiles.ac_parameters(data_ac)
m_save = ac_params.m
# Configuration sim
data_sim = LoadFiles._read_jsonc("configs/simulation/simulation.jsonc")
simulation_config = LoadFiles.simulation_parameters(data_sim)
# m equas
simulation_1 = Simulate(ac_params,simulation_config)
states_1 = simulation_1.simulate()
# 2 times m
ac_params.m = m_save*2
simulation_2 = Simulate(ac_params,simulation_config)
states_2 = simulation_2.simulate()
# 0.5 times m
ac_params.m = m_save*0.5
simulation_3 = Simulate(ac_params,simulation_config)
states_3 = simulation_3.simulate()


### Normal states
# Interface.plotter(states_1)

### Deflect simulation
data_ac = LoadFiles._read_jsonc("configs/aircrafts/aircraft.jsonc")
ac_params = LoadFiles.ac_parameters(data_ac)
data_conf2 = LoadFiles._read_jsonc("configs/simulation/sim_da.jsonc")
sim_conf2 = LoadFiles.simulation_parameters(data_conf2)
sim_da = Simulate(ac_params,sim_conf2)
states_da = sim_da.simulate()
# Interface.plotter(states_da)

### No eg
data_config3 = LoadFiles._read_jsonc("configs/simulation/sim_no_eg.jsonc")
sim_conf3 = LoadFiles.simulation_parameters(data_config3)
sim_eg = Simulate(ac_params,sim_conf3)
states_eg = sim_eg.simulate()
# Interface.plotter(states_eg)

dt = sim_conf2.dt

mesh = LoadFiles._load_mesh('data/meshes/example.obj')

sim1 = states_1
sim2 = states_da
sim3 = states_eg

fs = FlightSimulation(mesh,dt)

## 
""" # time vector
time = states_1[:,-1]

# plots
u = [states_1[:,0],states_2[:,0],states_3[:,0]]
labels = [f'm1 = {m_save}, kg',f'm2 = {m_save*2}, kg', f'm3 ={m_save/2} ,kg']
theta = [states_1[:,7],states_2[:,7],states_3[:,7]]
y_labels = ['u, m/s','theta, rad']
data = [u,theta]

plt.figure()
for j in range(len(u)):
    plt.plot(time,data[0][j],label=labels[j])
plt.ylabel(y_labels[0])
plt.grid()   
plt.legend()
plt.ylabel(y_labels[0])
plt.xlabel('Time, s')
plt.show(block=False)

plt.figure()
for j in range(len(u)):
    plt.plot(time,data[1][j],label=labels[j])
plt.ylabel(y_labels[1])
plt.xlabe('Time, s')
plt.grid()   
plt.legend()
plt.show() """


