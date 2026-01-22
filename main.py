from aircraft_model import AircraftModel as amodel
from simulation import Simulate as sim
from save_load_files import SaveLoadFiles as slf

if __name__ == "__main__":
    # Initial state variables
    X = [85,0,0,0,0,0,0,0.1,0]  # u,v,w,p,q,r,phi,theta,psi

    # Initial control variables
    U = [0,-0.1,0,0.8,0.8]  # delta_aleron, delta_elevator, delta_rudder, thurst1, thurst2

    # Simulation parameters
    time = 180  # seconds
    dt = 0.01   # time step in seconds

    simulator = sim(model=amodel, x=X, u=U, time=time, dt=dt)
    sim.simulate(self=simulator, da=None, eg=None)  # Simulate with 15 deg aleron deflection and engine 1 failure



