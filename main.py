from service.loader import LoadFiles
from service.save import Save
from core.simulation import Simulate
from service.loader import LoadFiles
from interface.flight_simulation import FlightSimulation
from interface.graphics import Interface



data_ac = LoadFiles._read_jsonc("configs/aircraft.jsonc")
ac_params = LoadFiles.ac_parameters(data_ac)


data_sim = LoadFiles._read_jsonc("configs/simulation.jsonc")
sim_params = LoadFiles.simulation_parameters(data_sim)


sim = Simulate(ac_params, sim_params)  
mesh = LoadFiles._load_mesh('data/meshes/ultimo2.stl')
states = sim.simulate()     
flight_sim = FlightSimulation(mesh,sim_params.dt)
flight_sim.animation(states)
Interface.plotter(states)

