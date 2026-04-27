from service.loader import LoadFiles
from core.simulation import Simulate
from service.loader import LoadFiles
from core.simulation import Simulate

# Cargar parámetros del avión
data_ac = LoadFiles._read_jsonc("configs/aircraft.jsonc")
ac_params = LoadFiles.ac_parameters(data_ac)

# Cargar parámetros de simulación
data_sim = LoadFiles._read_jsonc("configs/simulation.jsonc")
sim_params = LoadFiles.simulation_parameters(data_sim)

# Crear simulación y ejecutar
sim = Simulate(ac_params, sim_params)  # ← guardarlo en una variable
states = sim.simulate()                # ← llamarlo desde la variable
print(states)