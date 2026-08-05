from service.loader import LoadFiles
from service.save import Save
from core.simulation import Simulate
from service.loader import LoadFiles
from interface.flight_simulation import FlightSimulation
from interface.graphics import Interface
from interface.flight_simulation import FlightSimulation


ac_pars = LoadFiles._read_jsonc('configs/aircrafts/aircraft.jsonc')
sim_pars = LoadFiles._read_jsonc('configs/simulation/sim_da.jsonc')

ac_params = LoadFiles.ac_parameters(ac_pars)
states_input = LoadFiles.simulation_parameters(sim_pars)

sim = Simulate(ac_params,states_input)
states = sim.simulate()

Interface.plotter(states)
path_mesh = 'data/meshes/example.obj'
mesh = LoadFiles._load_mesh(path_mesh)
fs = FlightSimulation(mesh,states_input.dt)
fs.animation(states)
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
for j in range(len(u))Sources:
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


